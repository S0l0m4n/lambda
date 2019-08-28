#!/usr/bin/python3

import json

PREFIX = "/switchee/gen3/telemetry"

def make_body(event):
  body = ""
  x = json.loads(event)
  try:
    path = x['path']
  except KeyError:
    return body
  if path.startswith(PREFIX):
    rest = path[1+len(PREFIX):] # get string after PREFIX (and /)
    client_id = rest.split("/")[0] # split on / and get first entry  
    body = client_id # this is the client id
  return body

def lambda_handler(event, context):
  # TODO
  body = make_body(event)
  return {
      'statusCode': 200,
      'body': body
  }

if __name__ == '__main__':
  with open('foo.txt', 'r') as f:
    for line in f:
      print(make_body(line))
