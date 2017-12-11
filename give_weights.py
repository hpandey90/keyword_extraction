from itertools import product
import csv as csv
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import time
import queue as Q

client = MongoClient()
db = client.kaggle_facebook

train_filename = 'pre_process_train.csv'
#test_filename = 'pre_process_test.csv'
#output_filename = 'output.csv'
#f1_output_filename = 'f1_output.csv'

def main():
    test_model(train_filename)


def test_model(train_filename):
    titles_probabilities = db['temp1']
    titles_probabilities.create_index([("word", ASCENDING)])
    body_probabilities = db['temp2']
    body_probabilities.create_index([("word", ASCENDING)])
    print ('testing...')
    test_filename="/home/bgm/Desktop/IDS/keyword_extraction/pre_processed_train.csv"
    with open(test_filename) as readfrom:
        header = readfrom.readline()
        test_file_object = csv.reader(readfrom)
        #output_file = csv.writer(open('..'+os.path.sep+'csv'+os.path.sep+f1_output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
        #output_file.writerow(['Id','F1 score'])
        #max_to_test = 100
        #f1_mean = 0
        i=0
        w_title = 0
        w_body = 0
        for row in test_file_object:
            predicted_tags = row[3].lower().split()
            # find tags based on title
            c_title = 0
            c_body = 0
            for word in row[1].lower().split():
                find_result = titles_probabilities.find({'word':word})#,'score':{'$gte':title_threshold}})
                for tag_result in find_result:
                    if tag_result['tag'] in predicted_tags:
                        c_title += 1
                        break
            # find tags based on body
            for word in row[2].lower().split():
                find_result = body_probabilities.find({'word':word})#,'score':{'$gte':body_threshold}})
                for tag_result in find_result:
                    if tag_result['tag'] in predicted_tags:
                        #predicted_tags.append(tag_result['tag'])
                        c_body += 1
                        break
            #print(str(c_title)+' '+str(len(predicted_tags)))
            w_title += c_title / len(predicted_tags)
            w_body += c_body / len(predicted_tags)
            i += 1
            if(i%1000 == 0):
                print(str(i)+'steps done')
                print(' title accuracy = ' + str(w_title/i))
                print(' body accuracy = ' + str(w_body/i))
            #output_file.writerow([int(row[0]),F1_score(row[3].lower().split(),predicted_tags)])
            #f1_mean += F1_score(row[3].lower().split(),predicted_tags)
            #i+=1
            #if i==max_to_test:
                #break
        print (w_title/i)
        print (w_body/i)
        
if __name__=="__main__":
    main()