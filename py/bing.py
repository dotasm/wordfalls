########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, ast
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# cassandra
cluster_data = Cluster(['10.0.0.5'])
session_data = cluster_data.connect('sea')

# bing
# https://azure.microsoft.com/zh-cn/services/cognitive-services/
# https://dev.cognitive.microsoft.com/docs/services/f40197291cd14401b93a478716e818bf/operations/56b4447dcf5ff8098cef380d
# https://azure.microsoft.com/zh-cn/pricing/details/cognitive-services/search-api/
# https://azure.microsoft.com/zh-cn/try/cognitive-services/my-apis/

# 搜索关键词
word = 'PEEK'

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': word,
    'count': '10',
    'offset': '0',
    'mkt': 'zh-CN',
    'safesearch': 'Moderate',
})

try:
    conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
    conn.request("GET", "/bing/v7.0/search?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()

    all_content = json.loads(data.decode('utf-8'))
    webpages_list = all_content['webPages']['value']

    num = 1
    for i in webpages_list:
        print(i['url'])
        print(i['name'])
        print(i['snippet'])
        print(i['dateLastCrawled'])

        cql = "insert into v1_word_bing(word,degree,name,snippet,url,datelastcrawled) values('{w}',{d},'{n}','{s}','{u}','{last}')".format(w=word,d=num,n=i['name'],s=i['snippet'],u=i['url'],last=i['dateLastCrawled'])
        session_data.execute(cql)

        num = num + 1
        
    # str.encode("raw_unicode_escape").decode("utf-8")

    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################