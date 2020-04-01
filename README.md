# Kafka-to-MySQL Connector

Kafka-to-MySQL Connector is a Python application that consumes kafka events and
record them in a MySQL database

## Prepare the MySQL Database
MySql scripts directory
```bash
kafka-to-mySql/SqlScript/ 
```
- Create Classifieds Table with [Table_Classifieds.sql](https://github.com/psalias2006/kafka-to-mySql/blob/master/SqlScript/Table_Classifieds.sql)
- Create Margin Table with [Table_Margin.sql](https://github.com/psalias2006/kafka-to-mySql/blob/master/SqlScript/Table_Margin.sql)
- Create Store Procedure to calculate the Margin [Procedure_Margin.sql](https://github.com/psalias2006/kafka-to-mySql/blob/master/SqlScript/Procedure_Margin.sql)
- Enable Event Scheduler with [Scheduler_Enable.sql](https://github.com/psalias2006/kafka-to-mySql/blob/master/SqlScript/Scheduler_Enable.sql)
- Create the event with [Event_MarginLastHour.sql](https://github.com/psalias2006/kafka-to-mySql/blob/master/SqlScript/Event_MarginLastHour.sql)


## Installation

- Edit the Config file [consumer.conf](kafkaConsumer/kafkaBalancedConsumer/consumer.conf)
```bash
$ vim kafkaConsumer/kafkaBalancedConsumer/consumer.conf
```

```bash
[kafka]
Host = 1.1.1.1:9092
Topic = data
Batch = 10

[zoo]
Host = some-zoo:2181
ConsumerGroup = testgroup_11

[mysql]
Host = 1.1.1.1
Schema = some-schema
User = root
Pass = some-password
Table = some-table
```

- Start a [Zookeeper](https://hub.docker.com/_/zookeeper) server instance
```bash
$ docker run --name some-zookeeper --restart always -d zookeeper
```

- Build the kafka-to-MySQL container
```bash
$ cd kafka-to-mySql/Docker
$ ./buildme.sh 
```

- Start a kafka worker
```bash
$ docker run --name kafka-worker_1 -d kafka_to_sql_connector
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
