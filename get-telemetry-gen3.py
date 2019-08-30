#!/usr/bin/python3

# Expect an API request to be like so:
#   GET <base-url>/switchee/gen3/telemetry/<client_id>/<start>/<end>
# where start and end time formats are YYMMDD_hhmmss, e.g:
#   19/08/27 13:14:24 -> 190827_131424

import json

PREFIX = "/switchee/gen3/telemetry"

def make_body(event):
  body = ""
  try:
    path = event['path']
  except KeyError:
    return body
  if path.startswith(PREFIX):
    rest = path[1+len(PREFIX):] # get string after PREFIX (and /)
    fields = rest.split("/")
    try:
      client_id = fields[0]
      start = fields[1]
      end = fields[2]
      body = "GET msgs for {0} from {1} to {2}".format(client_id, start, end)
    except IndexError:
      pass
  return body

def lambda_handler(event, context):
  # TODO
  body = make_body(event)
  return {
      'statusCode': 200,
      'body': json.dumps(body)
  }

if __name__ == '__main__':
  with open('foo.txt', 'r') as f:
    for line in f:
      print(lambda_handler(json.loads(line), ""))
