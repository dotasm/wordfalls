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

channel.queue_declare(queue='pipe_search')


# 通过搜索百科获取图文解释
def do_search(word):
  # Algorithm

  return ''


def callback(ch, method, properties, body):
  word = str(body, encoding="utf-8")
  print(" [x] Receive %r" % word)

  #explain = do_search(word)
  #t = time.time()
  #we_cql = "insert into v1_word_explain(word,explain,ts) values('{w}', '{e}', {ts})".format(w=word, e=explain, ts=int(round(t * 1000)))
  #session_data.execute(we_cql)

#----------------------------------------------
channel.basic_consume(
  queue='pipe_search',
  on_message_callback=callback,
  auto_ack=True
)

print(' [*] Waiting for messages, To exit press CTRL+C')
channel.start_consuming()

