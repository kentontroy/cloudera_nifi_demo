#!/usr/local/bin/python3

import json
import logging
import math
import sys
import time
import zmq
from confluent_kafka import Producer
from rtmidi import midiconstants
from rtmidi.midiutil import open_midiinput

NUM_SEMITONES = 12
MAP_SEMITONES = { 0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
                  6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B" }

logging.basicConfig(level=logging.INFO)

class Endpoint(object):
  def publish(self, noteOnVal: {}):
    pass 

class Kafka(Endpoint):
  def __init__(self, properties: {}, destTopic: str):
    self._producer = Producer(properties)
    self._destTopic = destTopic

  def __ack__(self, err, msg):
    if err is not None:
      logging.error("Delivery to Kafka failed: {0}: {1}".format(msg.value(), err.str()))
    else:
      logging.info("Delivery to Kafka succeeded: {0}".format(msg.value()))

  def publish(self, midiMsg: {}):
    self._producer.produce(self._destTopic, key="some_session_id", value=midiMsg, callback=self.__ack__)

  def flush(self):
    self._producer.flush(30)

class MidiKeySwitchHandler(object):
  def __init__(self, port, key, endpoint):
    logging.info("Listening to MIDI from [%s]" % (port)) 
    logging.info("Observing key switch via [%s]" % (key)) 
    self.port = port
    self._wallclock = time.time()
    self._endpoint = endpoint
    
##############################################################################
# Callback handler for incoming midi messages
# INFO:root:[AE-01] @1618305121.659230 [144, 48, 120] 
# Midi Note range values
# C0 -> 12
# C3 -> 48 
##############################################################################
  def __call__(self, event, data=None):
    message, deltatime = event
    self._wallclock += deltatime
    logging.debug("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
    if message[0] & 0xF0 == midiconstants.NOTE_ON:
      status, note, velocity = message
      channel = (status & 0xF)
      octave = math.floor((note / NUM_SEMITONES) - 1)
      noteVal = "{0}{1}".format(MAP_SEMITONES[note % NUM_SEMITONES], octave)
      logging.info("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
      logging.info("Discovered note: [%s]" % noteVal)
 
# Publish NOTE_ON Midi val to Kafka
      jsonMsg = json.dumps({"TIMESTAMP": self._wallclock, "NOTE_ON": noteVal })
      self._endpoint.publish(jsonMsg)

def main():
  port = sys.argv[1] if len(sys.argv) > 1 else None
  try:
    midiin, input_port = open_midiinput(port)
  except (EOFError, KeyboardInterrupt):
    sys.exit()

  settings = {
    "bootstrap.servers": "ec2-3-235-146-59.compute-1.amazonaws.com",
    "acks": 1
  }
  producer = Kafka(settings, "some_session_id_midi_stream")   

  logging.info("Attaching MIDI input callback handler.")
  midiin.set_callback(MidiKeySwitchHandler(input_port, "C3", producer))

  logging.info("Entering main loop. Press Control-C to exit.")
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    producer.flush()

  finally:
    logging.info("Exit.")
    midiin.close_port()
    del midiin

if __name__ == "__main__":
  main()
