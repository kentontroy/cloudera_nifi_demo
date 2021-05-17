#!/usr/local/bin/python3

import boto3
import logging
import os
import sys
import threading
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
 
BUCKET = "statisticalfx"
BUCKET_PATH = "Data/Midi"

def upload(fileName, bucket, objectName=None):
  if objectName is None:
    objectName = fileName
  s3_client = boto3.client('s3')
  try:
    response = s3_client.upload_file(fileName, bucket, objectName, 
      Callback=ProgressPercentage(f))
  except ClientError as e:
    logging.error(e)
    return False
  return True

class ProgressPercentage(object):
  def __init__(self, fileName):
    self._fileName = fileName
    self._size = float(os.path.getsize(fileName))
    self._seenSoFar = 0
    self._lock = threading.Lock()

  def __call__(self, bytes_amount):
    with self._lock:
      self._seenSoFar += bytes_amount
      percent = (self._seenSoFar / self._size) * 100
      logging.info("\r%s  %s / %s  (%.2f%%)" % 
        (self._fileName, self._seenSoFar, self._size, percent))

if __name__ == "__main__":
  topDir = sys.argv[1] if len(sys.argv) > 1 else "../data"
  for dirName, subDirList, fileList in os.walk(topDir):
    for fName in fileList:
      key = BUCKET_PATH + dirName.replace(topDir, "") + "/" + fName     
      f = os.path.join(dirName, fName)
      logging.info("key = {0}, file = {1}".format(key, f))      
      upload(f, BUCKET, key)
  

