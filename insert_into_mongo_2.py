from itertools import product
import csv as csv
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import time

client = MongoClient()
db = client.kaggle_facebook
def main():
    insert_into_mongo()
    
def insert_into_mongo():
    probabilities = db['temp2']
    output_file = "output_bigram_probabilty_2.csv"
    with open("/home/hpandey/Desktop/"+output_file) as readfrom:
        readfrom = csv.reader(readfrom)
        for row in readfrom:
            probability = {'word':row[0],'tag':row[1], 'score':float(row[2])}
            probabilities.insert(probability)

if __name__=="__main__":
    main()