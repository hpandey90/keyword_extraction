import csv as csv
from bs4 import BeautifulSoup
import time
def main():
    start_time = time.time()
    data_preprocess()
    print (time.time() - start_time), "seconds"
def data_preprocess():
    train = csv.reader(open("/home/hpandey/Desktop/Train.csv"))
    wtrain = csv.writer(open("/home/hpandey/Desktop/pre_processed_train.csv",'wb'))
    swords = csv.reader(open("/home/hpandey/Desktop/stop-word-list.csv"))
    row_header = train.next()
    wtrain.writerow(row_header)
    stop_words = set()
    for s in swords:
        for word in s:
            stop_words.add(word.strip().lower())
    for line in train:
        if len(line)==4:
            wtrain.writerow((int(line[0]),remove_stop_words(line[1],stop_words),remove_stop_words(remove_html_tags(line[2]),stop_words),line[3]))

def remove_stop_words(sentence,stop_words):
    if isinstance(sentence, unicode):
        sentence = sentence.encode('utf8')
    symbols = ['?',',','.',':',';','+','=','"','/']
    for symbol in symbols:
        sentence = sentence.replace(symbol,' ')
    new_line=""
    for word in sentence.split():
        if word.lower() not in stop_words:
            new_line+=word+" "
    return new_line

def remove_html_tags(sentence):
    if isinstance(sentence, unicode):
        sentence = sentence.encode('utf8')
    bs = BeautifulSoup(sentence)
    for tags in ['a','code']:
        text = bs.findAll(tags)
        [tag.extract() for tag in text]
    return bs.get_text()

if __name__=="__main__":
    main()