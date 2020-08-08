#!/usr/bin/env python3

import time
import pika
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# cassandra
cluster_data = Cluster(['10.0.0.5'])
session_data = cluster_data.connect('sea')

# rabbitmq
connection = pika.BlockingConnection(
  pika.ConnectionParameters(host = 'localhost')
)
channel = connection.channel()

channel.queue_declare(queue='pipe_query')
channel.queue_declare(queue='pipe_api')


div_begin = '<div style="width:500px">'
div_end = '</div>'

# 通过查询数据库获得非空词条图文内容
def do_query(word):
  query = "select * from v1_word_bing where word='{w}' and degree={d}".format(w=word, d=1)
  statement = SimpleStatement(query, fetch_size=1000)
  rows = session_data.execute(statement)

  explain = ''
  for item in rows:
    explain = item.snippet
    
  return explain


def callback(ch, method, properties, body):
  word = str(body, encoding="utf-8")
  print(" [x] Receive %r" % word)

  explain = do_query(word)

  if len(explain) > 0:
    channel.basic_publish(
      exchange='',
      routing_key='pipe_api',
      body = div_begin + explain + div_end
    )
    print("[API] pipe_api: " + word)
    #t = time.time()


#----------------------------------------------
channel.basic_consume(
  queue='pipe_query',
  on_message_callback=callback,
  auto_ack=True
)

print(' [*] Waiting for messages, To exit press CTRL+C')
channel.start_consuming()

