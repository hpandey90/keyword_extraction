import csv as csv
def main():
    data_preprocess()
def data_preprocess():
    train = csv.reader(open("/home/hpandey/Desktop/sample_train.csv"))
    wtrain = csv.writer(open("/home/hpandey/Desktop/pre_processed_sample_train.csv",'wb'))
    swords = csv.reader(open("/home/hpandey/Desktop/stop-word-list.csv"))
    row_header = train.next()
    wtrain.writerow(row_header)
    stop_words = set()
    for s in swords:
        for word in s:
            stop_words.add(word.strip())
    for line in train:
        if len(line)==4:
            wtrain.writerow((int(line[0]),remove_stop_words(line[1],stop_words),remove_stop_words(line[2],stop_words),line[3]))
    
def remove_stop_words(sentence,stop_words):
    symbols = ['?',',','.',':',';','+','=','"','/']
    for symbol in symbols:
        sentence = sentence.replace(symbol,' ')
    new_line=""
    for word in sentence.split():
        if word not in stop_words:
            new_line+=word+" "
    return new_line
if __name__=="__main__":
    main()

    