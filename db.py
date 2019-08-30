#!/usr/bin/python3

import boto3
from pprint import PrettyPrinter

TABLE = "SamTestGen3Telemetry"
HASHKEY = "Row"
RANGEKEY = "PositionInRow"

def convertDatetime(dt):
  # Assume valid datetime string (YYMMDD_hhmmss)
  YY = dt[0:2]
  MM = dt[2:4]
  DD = dt[4:6]
  hh = dt[7:9]
  mm = dt[9:11]
  ss = dt[11:13]
  return "{0}-{1}-{2} {3}:{4}:{5}".format(YY, MM, DD, hh, mm, ss)


class MyDynamoDbResource():
  def __init__(self, client_id):
    self.client = boto3.client('dynamodb')
    self.client_id = client_id

  def getLogs(self, start, end):
    """
    Get all logs between start and end datetimes

    start: start datetime (string) in YYMMDD_hhmmss format, e.g. "190829_132355"
    end: end datetime (string) in YYMMDD_hhmmss format

    return: list containing all the logs

    Description: This method makes use of the timestamp (ts) key in the
    database. The format of ts values is "YY-MM-DD hh:mm:ss", so we need to
    convert to this from the input format.
    """
    start = convertDatetime(start)
    end = convertDatetime(end)
    return self.client.query(
        TableName=TABLE,
        ExpressionAttributeNames={
          "#name": HASHKEY,
          "#ts": RANGEKEY,
        },
        KeyConditionExpression="#name = :name and #ts between :start and :end",
        ExpressionAttributeValues={
          ":name": {"S": self.client_id},
          ":start": {"S": start},
          ":end": {"S": end},
        })


if __name__ == '__main__':
  db = MyDynamoDbResource("sam1")
  print(db.getLogs("190828_142336", "190828_142400"))
