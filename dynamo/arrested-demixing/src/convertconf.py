import dynamoio
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")

parser.add_argument("frame", type=int)

args = parser.parse_args()

dynamoio.conf_to_atom(args.filename, args.frame)   
