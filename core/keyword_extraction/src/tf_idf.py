import tokenizer as tok
import math
import operator


class Tf_Idf:
    def __init__(self, ndocs):
        self.filename_base = 'example_cases/sample'
        self.ndocs = ndocs
        
        self.tokenizer = tok.Tokenizer()
        self.inv_freq_dict = {}

    def generate_dict(self):
        for i in range(self.ndocs):
            filename = self.filename_base + str(i) + '.txt'
            with open(filename) as f:
                data = self.tokenizer.tokenize(f.read())
            
            for token in data:
                #if len(token)<=1:
                #    continue
                if token not in self.inv_freq_dict:
                    self.inv_freq_dict[token] = {i: 1}
                elif i in self.inv_freq_dict[token]:
                    self.inv_freq_dict[token][i] += 1
                else:
                    self.inv_freq_dict[token][i] = 1
    
    def calculate_scores(self,index):
        tf_scores = {}
        idf_scores = {}
        
        filename = self.filename_base + str(index) + '.txt'
        with open(filename) as f:
            data = self.tokenizer.tokenize(f.read())
        total_words = len(data) 

        for word in data:
            word_tcount = data.count(word) #number of instances of a word in a doc
            tf_scores[word] = word_tcount/total_words

            word_dcount = len(self.inv_freq_dict[word]) #word is in how many docs
            idf_scores[word] = math.log10(self.ndocs/word_dcount) 

        tf_idf_scores = {}
        for key, value in tf_scores.items():
          tf_idf_scores[key] = value*idf_scores[key]

        sorted_phrases = sorted(tf_idf_scores.items(),key=operator.itemgetter(1),reverse=True)
        for phrase in sorted_phrases:
            print (phrase) 
    
    def run(self, index):
        self.generate_dict()
        self.calculate_scores(index)

    def print_inverse_dict(self):
        for key,value in self.inv_freq_dict.items():
            print(key + ':' + str(value))


if __name__ == '__main__':
    tf_idf = Tf_Idf(10)
    tf_idf.run(3)
