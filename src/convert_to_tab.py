#!/usr/bin/python3

import json
import logging
import random
import sys

logging.basicConfig(level=logging.INFO)

class GuitarTab(object):
  STRING_e = ["E4","F4", "F#4","G4", "G#4","A4","A#4","B4", "C5", "C#5","D5","D#5","E5","F5", "F#5","G5"]
  STRING_B = ["B3","C4", "C#4","D4", "D#4","E4","F4", "F#4","G4", "G#4","A4","A#4","B4","C5", "C#5","D5"]
  STRING_G = ["G3","G#3","A3", "A#3","B3", "C4","C#4","D4", "D#4","E4", "F4","F#4","G4","G#4","A4", "A#4"]
  STRING_D = ["D3","D#3","E3", "F3", "F#3","G3","G#3","A3", "A#3","B3", "C4","C#4","D4","D#4","E4", "F4"]
  STRING_A = ["A2","A#2","B2", "C3", "C#3","D3","D#3","E3", "F3", "F#3","G3","G#3","A3","A#3","B3", "C3"]
  STRING_E = ["E2","F2", "F#2","G2", "G#2","A2","A#2","B2", "C3", "C#3","D3","D#3","E3","F4", "F#4","G4"]
  FRETBOARD = [STRING_E, STRING_A, STRING_D, STRING_G, STRING_B, STRING_e]
  POSITIONS = {}

##########################################################################
# Create a structure in memory for fast searching
# "Note": [ (note position on string, string position on fretboard) ]
# "E4":   [(0, 0), (5, 1), (9, 2)]
# A note can appear on one-to-many strings
# Playing an open string corresponds to the note at index 0 on the string
##########################################################################
  def __init__(self):
    for s, guitarString in enumerate(self.FRETBOARD):
      for n, note in enumerate(guitarString):
        if note in self.POSITIONS:
          self.POSITIONS[note].append((n, s))
        else:
          self.POSITIONS[note] = [(n, s)]

##########################################################################
# Given a list of notes, select tuples in the POSITIONS cache
# For each note in the list, the tuple selected represents the closest
# position to the previous note. A distance measure is used to calculate
# how far positions are from each other on the fretboard.
##########################################################################
  def getTab(self, notes: []) -> []:
    tab = []
    lastPosOnString, lastStringOnFret = 0, 0
    for msg in notes:
      midi = json.loads(msg)
      if midi["NOTE_ON"] not in self.POSITIONS:
        continue
      if len(tab) == 0:
        POS_ON_STRING, STRING_ON_FRET = random.choice(self.POSITIONS[midi["NOTE_ON"]])
        tab.append(json.dumps({"TIMESTAMP": midi["TIMESTAMP"], "NOTE_ON": midi["NOTE_ON"], "POS_ON_STRING": POS_ON_STRING, "STRING_ON_FRET": STRING_ON_FRET}))
        lastPosOnString, lastStringOnFret = POS_ON_STRING, STRING_ON_FRET
        continue
      dist = {}
      for v in self.POSITIONS[midi["NOTE_ON"]]:
        dist[v] = abs(lastPosOnString - v[0]) + abs(lastStringOnFret - v[1])
      NOTE_ON_STRING, STRING_ON_FRET = min(dist, key=dist.get)
      tab.append(json.dumps({"TIMESTAMP": midi["TIMESTAMP"], "NOTE_ON": midi["NOTE_ON"], "POS_ON_STRING": POS_ON_STRING, "STRING_ON_FRET": STRING_ON_FRET}))
      lastPosOnString, lastStringOnFret = POS_ON_STRING, STRING_ON_FRET

    return tab


def main():
  notes = []
  for line in sys.stdin:
    for midi in line.split("NEXT"):
      if len(midi) > 1:
        notes.append(midi)

###########################################################################################################
# Example message
# {"TIMESTAMP": 1621207176.3159494, "NOTE_ON": "A4"}NEXT{"TIMESTAMP": 1621207177.7371988, "NOTE_ON": "G4"}
###########################################################################################################

  tab = GuitarTab().getTab(notes)
  for t in tab:
    print(t)

if __name__ == "__main__":
  main()

# [('F5', (13, 0))]
  
