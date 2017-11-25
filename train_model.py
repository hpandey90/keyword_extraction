from itertools import product
import csv as csv

title_threshold = 0.000001
body_threshold = 0.000001
support_threshold = 1

def main():
    generate_combinations(1) # generate title and tags combinations
    generate_combinations(2) # generate body and tags combinations
    #train_model()

def generate_combinations(idx):
    train_file = "pre_processed_sample_train.csv"
    output_file = "output_bigram_sample"+str(idx)+".csv"
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
    output_file = "output_bigram_probabilty_sample"+str(idx)+".csv"
    with open("/home/hpandey/Desktop/"+output_file, "w") as writeto:
        writeto = csv.writer(writeto)
        for key in bigram_count:
            word_arr = key.split()
            word = word_arr[0]
            tag = word_arr[1]
            bigram_probability = float(bigram_count[key])/float(unigram_count[word])
            if idx==1:
                if bigram_count[key]>=support_threshold and bigram_probability>=title_threshold:
                    writeto.writerow((word,tag,bigram_probability))
            else:
                if bigram_count[key]>=support_threshold and bigram_probability>=body_threshold:
                    writeto.writerow((word,tag,bigram_probability))
    
def compute_bigrams(idx):
    with open("/home/hpandey/Desktop/output_bigram_sample"+str(idx)+".csv") as readfrom:
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
    with open("/home/hpandey/Desktop/pre_processed_sample_train.csv") as readfrom:
        readfrom = csv.reader(readfrom)
        unigram_count = {}
        for line in readfrom:
            for word in line[idx].strip().lower().split():
                if word  not in unigram_count:
                    unigram_count[word]=1
                else:
                    unigram_count[word]=unigram_count[word]+1
    return unigram_count
        
if __name__=="__main__":
    main()