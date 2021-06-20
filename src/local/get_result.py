import os
import argparse
import sys

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-f", dest = "score_filename", required=True,
   help="score file name")
ap.add_argument("-t", dest = "threshold", required=True,
   help="threshold")
ap.add_argument("-r", dest = "result_filename", required=True,
   help="result file name")
args = vars(ap.parse_args())

try:
    score_file = open(args['score_filename'], "r")
except IOError:
    sys.exit("Error reading file")

try:
    threshold = float(args['threshold'])
except ValueError:
    sys.exit("Error convert stirng to float")

try:
    result_file = open(args['result_filename'], "w")
except IOError:
    sys.exit("ErError creating result file")

line = score_file.read().splitlines()[0]


input_id, db_id, score = line.split(' ')
score = float(score)
if score > threshold:
    result_file.write("Accepted")
else:
    result_file.write("Rejected")

score_file.close()
result_file.close()




