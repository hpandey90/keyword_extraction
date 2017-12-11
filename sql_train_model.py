from itertools import product
import csv as csv
import time
import mysql.connector
cnx = mysql.connector.connect(user='hpandey', password='Rootat123',
                              host='mysql.cise.ufl.edu',
                              database='keyword_extraction')
cursor = cnx.cursor()


add_row = ("INSERT INTO keyword "
               "(word, tag, score) "
               "VALUES (%s, %s, %s)")

title_threshold = 0.1
body_threshold = 0.5
support_threshold = 5

train_filename = 'pre_processed_train.csv'
test_filename = 'pre_processed_test.csv'
output_filename = 'output.csv'
f1_output_filename = 'f1_output.csv'


print ("starting")

def main():
    print ("combination generation started for 1")
    start_time = time.time()
    generate_combinations(1) # generate title and tags combinations
    print (str((time.time() - start_time))+"seconds")
    print ("combination generation started for 2")
    start_time = time.time()
    generate_combinations(2) # generate body and tags combinations
    print (str((time.time() - start_time))+"seconds")

def generate_combinations(idx):
    bigram_count = {}
    unigram_count = {}
    train_file = "pre_processed_train.csv"
    with open(train_file) as readfrom:
        header = readfrom.readline()
        readfrom = csv.reader(readfrom)
        for row in readfrom:
            for a in row[idx].strip().lower().split():
                if a not in unigram_count:
                    unigram_count[a]=1
                else:
                    unigram_count[a]+=1
            for a,b in product(row[idx].strip().lower().split(),row[3].strip().lower().split()):
                    if (a,b) not in bigram_count:
                        bigram_count[(a,b)]=1
                    else:
                        bigram_count[(a,b)]+=1
    calculate_bigram_probability(idx,bigram_count,unigram_count)
    
def calculate_bigram_probability(idx,bigram_count,unigram_count):
    #probabilities = db['temp'+str(idx)]
    output_file = "op_bigram_probabilty_"+str(idx)+".csv"
    with open(output_file, "w") as writeto:
        writeto = csv.writer(writeto)
        for key in bigram_count:
            word = key[0]
            tag = key[1]
            bigram_probability = float(bigram_count[key])/float(unigram_count[word])
            if idx==1:
                if bigram_count[key]>=support_threshold and bigram_probability>=title_threshold:
                    #writeto.writerow((word,tag,bigram_probability))
                    data = (word, tag, score)
                    cursor.execute(add_row, data)
                    #probability = {'word':word,'tag':tag, 'score':bigram_probability}
                    #probabilities.insert(probability)
            else:
                if bigram_count[key]>=support_threshold and bigram_probability>=body_threshold:
                    #writeto.writerow((word,tag,bigram_probability))
                    data = (word, tag, score)
                    cursor.execute(add_row, data)
                    #probability = {'word':word,'tag':tag, 'score':bigram_probability}
                    #probabilities.insert(probability)
                    

if __name__=="__main__":
    main()