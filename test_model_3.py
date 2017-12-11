from itertools import product
import csv as csv
import time
import queue as Q
import mysql.connector
cnx = mysql.connector.connect(user='hpandey', password='Rootat123',
                              host='mysql.cise.ufl.edu',
                              database='keyword_extraction')
cursor = cnx.cursor()
query_title = ("SELECT word, tag, score FROM keyword_title "
         "WHERE word='%s'")
query_body = ("SELECT word, tag, score FROM keyword_body"
         "WHERE word='%s'")
import re

regex = r"['\"\\]"
pattern = re.compile(regex)

regex1 = r"[\x00-\x7F]+"
pattern1 = re.compile(regex1)
def main():
    run_model()

def run_model():
    test_filename="pre_processed_test.csv"
    output_filename="output.csv"
    print ('predicting...')
    count=0
    with open(test_filename,'r',encoding='utf8') as readfrom, open(output_filename,"w") as writeto:
        header = readfrom.readline()
        test_file_object = csv.reader(readfrom)
        output_file = csv.writer(writeto)
        output_file.writerow(['Id','Tags'])
        for row in test_file_object:
            if count%100000==0:
                print (str(count)+" steps done")
            predicted_tags = {}
            write_tags = []
            for word in row[1].lower().split():
                #print (word)
                if pattern.findall(word):
                    1
                elif pattern1.findall(word):
                    try:
                        cursor.execute("SELECT word, tag, score FROM keyword_title WHERE word='"+word+"'")
                        for (word, tag, score) in cursor:
                            if not tag in predicted_tags:
                                predicted_tags[tag]=1
                            else:
                                predicted_tags[tag]+=1
                    except:
                        pass
                # find tags based on body
            for word in row[2].lower().split():
                #print (word)
                if pattern.findall(word):
                    1
                elif pattern1.findall(word):
                    try:
                        cursor.execute("SELECT word, tag, score FROM keyword_body WHERE word='"+word+"'")
                        #cursor.execute(query_body, (word))
                        for (word, tag, score) in cursor:
                            if not tag in predicted_tags:
                                predicted_tags[tag]=1
                            else:
                                predicted_tags[tag]+=1
                    except:
                        pass
            prio_queue = Q.PriorityQueue()
            for item in predicted_tags:
                prio_queue.put((-predicted_tags[item],item))
            c=0
            while not prio_queue.empty():
                c+=1
                write_tags.append(prio_queue.get()[1])
                if c==5:
                    break
            if len(write_tags)==0:
                write_tags.append("javascript c# python php java")
            count+=1
            output_file.writerow([int(row[0]),' '.join(write_tags)])
    print ('done')

if __name__=="__main__":
    main()