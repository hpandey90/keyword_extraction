from itertools import product
import csv as csv
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import time
title_threshold = 0.5
body_threshold = 0.4
support_threshold = 1

train_filename = 'pre_processed_train.csv'
test_filename = 'pre_processed_test.csv'
output_filename = 'output.csv'
f1_output_filename = 'f1_output.csv'

client = MongoClient()
db = client.kaggle_facebook

print "starting"

def main():
    print "combination genration started for 1"
    start_time = time.time()
    generate_combinations(1) # generate title and tags combinations
    print (time.time() - start_time), "seconds"
    print "combination genration started for 2"
    start_time = time.time()
    generate_combinations(2) # generate body and tags combinations
    print (time.time() - start_time), "seconds"
    print "running test model"
    start_time = time.time()
    test_model()
    print (time.time() - start_time), "seconds"

def generate_combinations(idx):
    train_file = "pre_processed_train.csv"
    output_file = "output_bigram_"+str(idx)+".csv"
    with open("/home/hpandey/Desktop/"+train_file) as readfrom, open("/home/hpandey/Desktop/"+output_file, "w") as writeto:
        header = readfrom.next()
        readfrom = csv.reader(readfrom)
        writeto = csv.writer(writeto)
        for row in readfrom:
            for a,b in product(row[idx].strip().lower().split(),row[3].strip().lower().split()):
                    writeto.writerow((a,b))
    bigram_count = compute_bigrams(idx)
    unigram_count = compute_unigrams(idx)
    calculate_bigram_probability(idx,bigram_count,unigram_count)
    
def calculate_bigram_probability(idx,bigram_count,unigram_count):
    probabilities = db['temp'+str(idx)]
    output_file = "output_bigram_probabilty_"+str(idx)+".csv"
    with open("/home/hpandey/Desktop/"+output_file, "w") as writeto:
        writeto = csv.writer(writeto)
        for key in bigram_count:
            word_arr = key.split()
            word = word_arr[0]
            tag = word_arr[1]
            bigram_probability = float(bigram_count[key])/float(unigram_count[word])
            if idx==1:
                if bigram_count[key]>=support_threshold and bigram_probability>=title_threshold:
                    #writeto.writerow((word,tag,bigram_probability))
                    probability = {'word':word,'tag':tag, 'score':bigram_probability}
                    probabilities.insert(probability)
            else:
                if bigram_count[key]>=support_threshold and bigram_probability>=body_threshold:
                    #writeto.writerow((word,tag,bigram_probability))
                    probability = {'word':word,'tag':tag, 'score':bigram_probability}
                    probabilities.insert(probability)
    
def compute_bigrams(idx):
    with open("/home/hpandey/Desktop/output_bigram_"+str(idx)+".csv") as readfrom:
        readfrom = csv.reader(readfrom)
        bigram_count = {}
        for row in readfrom:
            bigram = row[0]+' '+row[1]
            if bigram  not in bigram_count:
                bigram_count[bigram]=1
            else:
                bigram_count[bigram]=bigram_count[bigram]+1
    return bigram_count

def compute_unigrams(idx):
    with open("/home/hpandey/Desktop/pre_processed_train.csv") as readfrom:
        readfrom = csv.reader(readfrom)
        unigram_count = {}
        for line in readfrom:
            for word in line[idx].strip().lower().split():
                if word  not in unigram_count:
                    unigram_count[word]=1
                else:
                    unigram_count[word]=unigram_count[word]+1
    return unigram_count
        
def test_model():
    titles_probabilities = db['temp1']
    titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    body_probabilities.create_index([("word", ASCENDING)])
    print 'predicting...'
    test_file_object = csv.reader(open("/home/hpandey/Desktop/pre_processed_test.csv", 'rb'))
    header = test_file_object.next()
    output_file = csv.writer(open("/home/hpandey/Desktop/"+output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
    output_file.writerow(['Id','Tags'])
    for row in test_file_object:
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
        output_file.writerow([int(row[0]),' '.join(predicted_tags)])
    print 'done'


def F1_score(tags,predicted):
    tags = set(tags)
    predicted = set(predicted)
    tp = len(tags & predicted)
    fp = len(predicted) - tp
    fn = len(tags) - tp
 
    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
 
        return 2*((precision*recall)/(precision+recall))
    else:
        return 0

if __name__=="__main__":
    main()