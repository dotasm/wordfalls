#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(
	pika.ConnectionParameters(host = 'localhost')
)
channel = connection.channel()

channel.queue_declare(queue='pipe_level_1')

if len(sys.argv) == 1:
  text_body = '题目：林则徐虎门销烟'
else:
  text_body = sys.argv[1]


channel.basic_publish(
	exchange='',
	routing_key='pipe_level_1',
	body = text_body
)

print(" [x] Sent '%r'" % text_body)
connection.close()

