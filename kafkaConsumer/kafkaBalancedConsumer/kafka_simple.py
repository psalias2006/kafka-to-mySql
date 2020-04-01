from pykafka import KafkaClient
import pandas as pd
import datetime
import json

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import pandas as pd
import logging

import configparser
import time

config = configparser.ConfigParser()
config.read('consumer.conf')
#config.read('consumer_local.conf')

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


KAFKA_HOST 	= config['kafka']['Host']
KAFKA_TOPIC	= config['kafka']['Topic']
KAFKA_BATCH	= int(config['kafka']['Batch'])

ZOO_HOST	= config['zoo']['Host']
ZOO_GROUP	= config['zoo']['ConsumerGroup']


MYSQL_HOST      = config['mysql']['Host']
MYSQL_DATABASE  = config['mysql']['Schema']
MYSQL_USER      = config['mysql']['User']
MYSQL_PASS      = config['mysql']['Pass']
MYSQL_TABLE     = config['mysql']['Table']

class mySql:
	
	def __init__(self, name, sqlHost, sqlDB, sqlUser, sqlPass, sqlTable):
		self.name	= name
		self.sqlHost	= sqlHost
		self.sqlDB	= sqlDB
		self.sqlUser	= sqlUser
		self.sqlPass	= sqlPass
		self.sqlTable	= sqlTable

		self.sqlConn	= mysql.connector.connect(host = self.sqlHost,
							  database = self.sqlDB,
							  user = self.sqlUser,
							  password = self.sqlPass)


	def _sqlInsertBuilder(self, values):
		sqlInsertQuery	= '''INSERT INTO {} (id, 
						   customer_id, 
						   created_at, 
						   text, 
						   ad_type, 
						   price, 
						   currency, 
						   payment_type, 
						   payment_cost)'''.format(self.sqlTable)

		sqlValues	= '''VALUES ("{v[id]}", 
					   "{v[customer_id]}", 
					   "{v[created_at]}", 
					   "{v[text]}", 
					   "{v[ad_type]}", 
					    {v[price]}, 
					   "{v[currency]}", 
					   "{v[payment_type]}", 
					    {v[payment_cost]})'''.format(v=values)

		sqlQuery	= ' '.join([sqlInsertQuery, sqlValues])
		return sqlQuery


	def sqlBulkInsert(self, valueLst):
		connection      = self.sqlConn
		cursor          = connection.cursor()
		
		for values in valueLst:
			try:
				mySqlQuery =  self._sqlInsertBuilder(values)
				cursor.execute(mySqlQuery)
			except Exception as ex: logging.info(ex)
		
		connection.commit()
		
		#logging('{} Records inserted successfully into table'.format((cursor.rowcount)))
		cursor.close()
		return
			




class kafkaConsumer:

	def __init__(self, name, kafkaHost, kafkaTopic):
		self.name	= name
		self.kafkaHost	= kafkaHost
		self.kafkaTopic	= kafkaTopic
		self.mySql	= mySql('testSQL', 
					MYSQL_HOST, 
					MYSQL_DATABASE, 
					MYSQL_USER, 
					MYSQL_PASS, 
					MYSQL_TABLE)


	def _convertIsoDatetime(self, dt):
		if dt is not 'NULL': dt = dt.replace('T', ' ').replace('Z', '')
		return dt


	def _cleanJson(self, msgJson):
		msgDf	= pd.DataFrame(msgJson, columns = ['id', 
							   'customer_id', 
							   'created_at',
                                                           'text', 
							   'ad_type', 
							   'price', 
							   'currency',
                                                           'payment_type', 
							   'payment_cost'])

		msgDf			= msgDf.replace({pd.np.nan: 'NULL'})
		msgDf['created_at']	= msgDf['created_at'].apply(self._convertIsoDatetime)
		list_dict		= msgDf.T.to_dict().values()

		return list_dict


	def _insertMySql(self, msgList):
		msgJson = []
		mySql	= self.mySql
		
		for msg in msgList:
			try: msgJson.append(json.loads(msg.decode('utf-8')))
			except: 
				logging.info('Broken json from kafka ')
				logging.info(msg)
		
		list_dict = self._cleanJson(msgJson)
		mySql.sqlBulkInsert(list_dict)

		return


	def consume(self):
		client		= KafkaClient(hosts=self.kafkaHost)
		topic		= client.topics[self.kafkaTopic]

		balanced_cons	= topic.get_balanced_consumer(
					consumer_group=ZOO_GROUP, 
					auto_commit_enable=True, 
					zookeeper_connect=ZOO_HOST)

		msgList		= []


		for message in balanced_cons:
			if message is not None:
				if len(msgList) < KAFKA_BATCH :
					msgList.append(message.value)
				else:
					logging.info('{} kafka message offset consumed'.format(message.offset))
					self._insertMySql(msgList)
					msgList = []
		return



def main():
	kafkaStream = kafkaConsumer('testConsumer', KAFKA_HOST, KAFKA_TOPIC)

	while True:
		try: kafkaStream.consume()
		except Exception as ex: logging.info(ex)

	return


if __name__ == '__main__':
	main()
		
