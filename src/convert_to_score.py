#!/usr/bin/python3

import json
import logging
import pandas as pd
import sys

logging.basicConfig(level=logging.INFO)

class Score(object):
  def __init__(self, tabLineSize: int = 20):
    self.notes = []
    self.tabLineSize = tabLineSize

  def write(self, note: str):
    self.notes.append(note)

##########################################################################
# For each line on the tab, find which positions are played and when
##########################################################################
  def drawTabLine(self) -> str:
    NUM_OF_STRINGS = 6
    l: str = ""
    for s in range(NUM_OF_STRINGS):
      l = l + "EADGBe"[s] + " | "
      size = min(len(self.notes), self.tabLineSize)
      for i in range(size):
# Check if the ith entry in the tab occurs on the sth guitar string
# If so, place fret position for the note in the tab line
# If not, place an empty tab line
        if self.notes[i][1] == s:
          if len(str(self.notes[i][0])) == 2:
            l = l + "-" + str(self.notes[i][0])  + "-"
          else:
            l = l + "--" + str(self.notes[i][0])  + "-"
        else:
          l = l + "----"
      l = l + "\n"
    return l

###############################################################################################
# One-to-many of the below messages received
# {"TIMESTAMP": 1621223794.0542884, "NOTE_ON": "F#4", "POS_ON_STRING": 7, "STRING_ON_FRET": 1}
###############################################################################################

def main():
  score = Score()

# Of course, sort by timestamp

  df = pd.DataFrame(columns=["TIMESTAMP", "NOTE_ON", "POS_ON_STRING", "STRING_ON_FRET"])

  for line in sys.stdin:
    note = json.loads(line)      
    df = df.append(note, ignore_index=True)    

  df = df.sort_values(by=["TIMESTAMP"])
  for index, row in df.iterrows(): 
    score.write((row["POS_ON_STRING"], row["STRING_ON_FRET"]))

  print(score.drawTabLine())

if __name__ == "__main__":
  main()

  
