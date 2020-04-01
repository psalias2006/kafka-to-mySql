#!/bin/bash

cp -r ../kafkaConsumer/kafkaBalancedConsumer .
cp -r ../kafkaConsumer/startScript .

docker build --tag kafka_to_sql_connector .

rm -rf kafkaBalancedConsumer  
rm -rf startScript
