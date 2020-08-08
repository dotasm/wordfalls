#!/usr/bin/env python3

import pika
import jieba
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

channel.queue_declare(queue='pipe_base')
channel.queue_declare(queue='pipe_search')
channel.queue_declare(queue='pipe_query')

symbol_list = [',', '，', '.', '。', '、', ':', '：', '“', '”', '/']


def get_word_explain():
  query = "select word from v1_word_explain"
  statement = SimpleStatement(query, fetch_size=1000)
  rows = session_data.execute(statement)

  word_set = set()
  for item in rows:
    word_set.add(item.word)

  return word_set


def callback(ch, method, properties, body):
  s = str(body, encoding="utf-8")
  print(" [x] Receive %r" % s)

  word_list = jieba.lcut(s)

  for word in word_list:
    if word not in symbol_list:
      # 1.事实表可用于统计词频
      wc_cql = "update v1_word_count set count=count+1 where word='{d}'".format(d=word)
      session_data.execute(wc_cql)

      # 2.未解释的新词进入二级队列 用于手动或自动补全名词解释
      if word not in job_search:        
        channel.basic_publish(
          exchange='',
          routing_key='pipe_search',
          body = word
        )
        print("[Search] pipe_search: " + word)

        job_search.add(word)
      else:
        # 3.已解释的旧词跳过二级直接进入三级队列 驱动API和websocket显示        
        channel.basic_publish(
          exchange='',
          routing_key='pipe_query',
          body = word
        )
        print("[Query] pipe_query: " + word)

        #job_search.add(word)
        # debug      
        #print(word)

#----------------------------------------------
# 遗留搜索结果异步更新问题 需要支持定时更新/实时更新/手动更新/指定更新等场景
# 目前默认手动更新
job_search = get_word_explain()
print(job_search)

channel.basic_consume(
  queue='pipe_base',
  on_message_callback=callback,
  auto_ack=True
)

print(' [*] Waiting for messages, To exit press CTRL+C')
channel.start_consuming()

