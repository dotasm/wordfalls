#!/usr/bin/env python3

import sys
import pika

connection = pika.BlockingConnection(
	pika.ConnectionParameters(host = 'localhost')
)
channel = connection.channel()

channel.queue_declare(queue='pipe_level_1')

if len(sys.argv) == 1:
  text_body = '航空制造技术：连续CF/PEEK预浸料制造技术研究进展'
else:
  text_body = sys.argv[1]


channel.basic_publish(
	exchange='',
	routing_key='pipe_base',
	body = text_body
)

print(" [x] Sent '%r'" % text_body)
connection.close()

