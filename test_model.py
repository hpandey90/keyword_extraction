from itertools import product
import csv as csv
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import time

client = MongoClient()
db = client.kaggle_facebook

def main():
    run_model()

def run_model():
    test_filename="one_test.csv"
    output_filename="output2.csv"
    print 'starting...'
    titles_probabilities = db['temp1']
    print 'creating index for temp1'
    titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    print 'creating index for temp2'
    body_probabilities.create_index([("word", ASCENDING)])
    print 'predicting...'
    count=0
    with open(test_filename) as readfrom, open(output_filename,"w") as writeto:
        test_file_object = csv.reader(readfrom)
        output_file = csv.writer(writeto)
        output_file.writerow(['Id','Tags'])
        for row in test_file_object:
            if count%10000==0:
                print str(count)+" steps done"
            predicted_tags = []
            # find tags based on title
            for word in row[1].lower().split():
                find_result = titles_probabilities.find({'word':word})#,'score':{'$gte':title_threshold}})
                for tag_result in find_result:
                    if not tag_result['tag'] in predicted_tags:
                        predicted_tags.append(tag_result['tag'])
                # find tags based on body
            for word in row[2].lower().split():
                find_result = body_probabilities.find({'word':word})#,'score':{'$gte':body_threshold}})
                for tag_result in find_result:
                    if tag_result['tag'] not in predicted_tags:
                        predicted_tags.append(tag_result['tag'])
            count+=1
            output_file.writerow([int(row[0]),' '.join(predicted_tags)])
    print 'done'

if __name__=="__main__":
    main()