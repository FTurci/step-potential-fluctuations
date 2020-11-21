from dynamoutils import io
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename")

parser.add_argument("frame", type=int)

args = parser.parse_args()

io.conf_to_atom(args.filename, args.frame)   
