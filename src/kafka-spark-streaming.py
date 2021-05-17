import json
from datetime import datetime
from pyspark import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import to_timestamp, window, udf
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StringType, TimestampType

##############################################################
# Example message on Kafka topic some_session_id_midi_stream
# {"TIMESTAMP": 1621252842.876252, "NOTE_ON": "G4"}
##############################################################

BOOTSTRAP = "ip-172-31-91-111.ec2.internal:9092, " \
            "ip-172-31-86-76.ec2.internal:9092, " \
            "ip-172-31-84-154.ec2.internal:9092"
OFFSET = "earliest" #.option("startingOffsets", OFFSET) \
TOPIC = "some_session_id_midi_stream"

def createContext(cores, gb):
  conf = (
    SparkConf()
     .setMaster('local[{}]'.format(cores))
     .set('spark.driver.memory', '{}g'.format(gb))
  )
  sc = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")
  return sc

def getTimestamp(s):
  t = json.loads(s)["TIMESTAMP"] 
  return datetime.utcfromtimestamp(t).strftime("%Y-%m-%dT%H:%M:%SZ")
 

def getNote(s):
  return json.loads(s)["NOTE_ON"]

def main():
  spark = SparkSession(createContext(1, 2))
  df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", BOOTSTRAP) \
    .option("subscribe", TOPIC) \
    .load()

  df = df.selectExpr("CAST(value AS STRING)")
  df.printSchema()
  df.createOrReplaceTempView("MIDI_NOTES")

  spark.udf.register("getTimestampUDF", getTimestamp, StringType())
  spark.udf.register("getNoteUDF", getNote, StringType())

  query = spark.sql("SELECT to_timestamp(getTimestampUDF(value)) AS timestamp, getNoteUDF(value) AS note from MIDI_NOTES")

# pyspark.sql.functions.window(timeColumn, windowDuration, slideDuration=None, startTime=None)[source]^
# Creates a 10 second window that hops by 5 seconds
# Watermark is a moving threshold in event-time that trails behind to accommodate late arriving data
  windowed = query.withWatermark("timestamp", "10 seconds") \
    .groupBy(
      "note",
      window("timestamp", "10 seconds", "5 seconds")) \
    .count()

  results = windowed.writeStream \
   .format("console") \
   .outputMode("append") \
   .start()

  results.awaitTermination(180)

if __name__ == "__main__":
  main()



