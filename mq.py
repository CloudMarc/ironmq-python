import json
import time
import sys
import hmac
import hashlib
import signal
import urllib2
import urllib
import httplib
import syslog
import base64
#import MultipartPostHandler
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def handler(signum, frame):
  print 'Signal handler called with signal', signum

signal.signal(signal.SIGALRM, handler)

token = "TSjcQAnNMZKWGdOyCJhxnN64CTk"
token = "jTxYQDmMx5ZtVeZBT8jVx6oJDLw"
#project_id = "4e71843298ea9b6b9f000004"
#project_id = "77aca33fc4f93528d8c3e28da5d36657"
#project_id = "4e8aa70d67a20c0ed4000002"
project_id = "4ed16540cddb131dae000004"
# http://mq-aws-us-east-1.iron.io/ping
# host= "mq-aws-us-east-1.iron.io"
host= "174.129.54.171"
port = "8081"
version = "1"
#project_id = "4e71843298ea9b6b9f000004"
#project_id = "77aca33fc4f93528d8c3e28da5d36657"

def baseUrl(host, port, version, project_id):
  url = "http://"+host+":"+port+"/"+version+'/projects/'+project_id
  return url

#GET /projects/:project_id/queues/:queue_name/messages - get message from queue
def getMsg(baseUrl, key, token):
  url = baseUrl+'/queues/'+key + "/messages?oauth="+token
  print "About to get:  "+ url
  req = urllib2.Request(url, None, {})
  ret = urllib2.urlopen(req)
  s = ret.read()
  return s

#POST /projects/:project_id/queues/:queue_name/messages - push message onto queue
def postMsg(baseUrl, key, msg, token, project_id, host, port):
  #url = baseUrl+key + "?oauth="+token
  #host= "mq-aws-us-east-1.iron.io"
  #port = "80"
  #version = "1"
  #conn = httplib.HTTPConnection(host + ":" + port)
  conn = httplib.HTTPConnection(host, port)
  print "msg = " + msg
  data = json.dumps({"body" : msg})
  headers = {}
  headers['Content-Type'] = "application/json"
  dataLen = len(data)
  headers['Content-Length'] = dataLen
  uri = '/'+version+'/projects/'+project_id + '/queues/'+key+'/messages?oauth='+token
  print "POST uri = " + uri
  conn.request("POST", uri, data, headers)
  response = conn.getresponse()
  print response.status, response.reason
  res = response.read()
  print "post msg response data:  " + res
  conn.close()
  return res

#DELETE /messages/#{message_id} - delete message
def delMsg(baseUrl, key, msg_id, token, project_id, host, port):
  url = baseUrl+key + "?oauth="+token
  #host= "184.72.210.108"
  #port = "80"
  version = "1"
  conn = httplib.HTTPConnection(host + ":" + port)
  data = json.dumps({"msg" : msg})
  headers = {}
  #headers['Content-Type'] = "application/json"
  #dataLen = len(data)
  #headers['Content-Length'] = dataLen
  print "DELETE, msg_id = "+ str(msg_id)
  uri = "/"+version+"/projects/" + project_id + "/queues/testKey/messages/"+str(msg_id)+"?oauth="+token
  print "DELETE, uri = " + uri
  conn.request("DELETE", uri)
  response = conn.getresponse()
  print "Past getresponse...",response.status, response.reason
  res = response.read()
  print "post msg response data:  " + res
  conn.close()
  return res

bUrl = baseUrl(host, port, version, project_id)
key = "/this/is/a/key"
key = "testKey"
msg = "YAY!!! " + time.asctime()

#for i in range(10):
t0 = time.time()
msg = "YAY!!! " + time.asctime()
ret = postMsg(bUrl, key, msg, token, project_id, host, port)
#sys.exit()
#time.sleep(1)
ret = getMsg(bUrl, key, token)
print "get returns:  " + str(ret)
a = json.loads(ret)
msg_id = a['id']
print "retrieved msg:  " + msg

x = delMsg(bUrl, key, msg_id, token, project_id, host, port)
dt = time.time() - t0
print "Time for 3 basic ops:  " + str(dt)
print "Result of delete message:  " + str(x)
