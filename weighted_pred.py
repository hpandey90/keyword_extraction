from itertools import product
import csv as csv
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import time

client = MongoClient()
db = client.kaggle_facebook
weight_title = 0
weight_body = 0

def main():
    run_model()

def run_model():
    test_filename="one_test.csv"
    output_filename="output2.csv"
    print 'starting...'
    titles_probabilities = db['temp1']
    #print 'creating index for temp1'
    #titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    #print 'creating index for temp2'
    #body_probabilities.create_index([("word", ASCENDING)])
    #print 'predicting...'
    count=0
    with open(test_filename) as readfrom, open(output_filename,"w") as writeto:
        test_file_object = csv.reader(readfrom)
        output_file = csv.writer(writeto)
        output_file.writerow(['Id','Tags'])
        for row in test_file_object:
            if count%10000==0:
                print str(count)+" steps done"
            predicted_tags_title = {}
            predicted_tags_body = {}
            predicted_tags=[]
            sort_by_wt=[]
            # find tags based on title
            title = row[1].lower().split()
            body = row[2].lower().split()
            for word in title:
                find_result = titles_probabilities.find({'word':word})#,'score':{'$gte':title_threshold}})
                for tag_result in find_result:
                    if tag_result['tag'] not in predicted_tags_title:
                        predicted_tags_title[tag_result['tag']]=1
                    else:
                        predicted_tags_title[tag_result['tag']]+=1
                for tags in predicted_tags_title:
                    sort_by_wt.append([tags,predicted_tags_title[tags]*weight_title/len(title)])
                
                # find tags based on body
            for word in body:
                find_result = body_probabilities.find({'word':word})#,'score':{'$gte':body_threshold}})
                for tag_result in find_result:
                     if tag_result['tag'] not in predicted_tags_body:
                        predicted_tags_body[tag_result['tag']]=1
                    else:
                        predicted_tags_body[tag_result['tag']]+=1
                for tags in predicted_tags_body:
                    sort_by_wt.append([tags,predicted_tags_body[tags]*weight_body/len(body)])
            sort_by_wt = sorted(sort_by_wt, key=lambda x : -x[1])
            k=0
            for weighted_tag in sort_by_wt:
                if weighted_tag not in predicted_tags:
                    predicted_tags.append(weighted_tag)
                k+=1
                if k==5:
                    break
            count+=1
            output_file.writerow([int(row[0]),' '.join(predicted_tags)])
    print 'done'

if __name__=="__main__":
    main()