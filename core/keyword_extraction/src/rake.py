import operator
import os
from pathlib import Path

import jpype as jp

import phrase_generator as pg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZEMBEREK_PATH = os.path.join(BASE_DIR, "zemberek-full.jar")


# ZEMBEREK_PATH = '../zemberek-full.jar'

class Rake:
    def __init__(self, min_len=1, max_len=10):
        if jp.isJVMStarted():
            return
        self.phrase_generator = pg.PhraseGenerator()
        self.filename = ''

        self.min_len = min_len
        self.max_len = max_len

        self.cand_phrases = []
        self.phrase_scores = {}

        jp.startJVM(jp.getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % ZEMBEREK_PATH, convertStrings=True)

    def __del__(self):
        jp.shutdownJVM()

    def run(self, filename):

        self.generate_candidate_phrases(filename)
        word_scores = self.calculate_word_scores()
        self.calculate_phrase_scores(word_scores)
        self.sort_phrases()

        return self.phrase_scores

    def generate_candidate_phrases(self, text):
        self.cand_phrases = self.phrase_generator.run(text)

    def calculate_word_scores(self):
        word_frequency = {}
        word_degrees = {}
        word_scores = {}

        for phrase in self.cand_phrases:
            phrase_len = len(phrase)
            phrase_degree = phrase_len - 1
            for word in phrase:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1

                word_degrees.setdefault(word, 0)
                word_degrees[word] += phrase_degree

        for key, value in word_frequency.items():
            word_degrees[key] = word_degrees[key] + value

        for item in word_frequency:
            word_scores.setdefault(item, 0)
            word_scores[item] = word_degrees[item] / (word_frequency[item])

        return word_scores

    def calculate_phrase_scores(self, word_scores):
        self.phrase_scores = {}
        for phrase in self.cand_phrases:
            # if self.cand_phrases.count(phrase) >= self.min_len
            phrase_str = ' '.join(phrase)
            self.phrase_scores.setdefault(phrase_str, 0)
            candidate_score = 0
            for word in phrase:
                candidate_score += word_scores[word]
            self.phrase_scores[phrase_str] = candidate_score

        return self.phrase_scores

    def print_candidate_phrases(self):
        for elem in self.cand_phrases:
            print(elem)

    def print_word_scores(self):
        for key, value in self.word_score.items():
            print("{}:{}".key, value)

    def sort_phrases(self):
        sorted_phrases = sorted(self.phrase_scores.items(), key=operator.itemgetter(1), reverse=True)
        self.phrase_scores = sorted_phrases

    def print_phrase_scores(self, ):
        count = 0
        for phrase in self.phrase_scores:
            if len(phrase[0].split()) in range(self.min_len, self.max_len):
                new_phrase = ''
                analysis = list(
                    self.phrase_generator.morphology.analyzeAndDisambiguate(phrase[0]).bestAnalysis().toArray())
                for word in analysis:
                    word_lemma = word.getLemmas()[0]
                    new_phrase += word_lemma + ' '

                print(new_phrase)
                count += 1
                if count == 5:
                    break

    def write_phrase_scores_for_db(self, lemmatized_keywords, keywords):
        count = 0
        for phrase in self.phrase_scores:
            if len(phrase[0].split()) in range(self.min_len, self.max_len):
                new_phrase_lemmatized = ''
                new_phrase = ''
                analysis = list(
                    self.phrase_generator.morphology.analyzeAndDisambiguate(phrase[0]).bestAnalysis().toArray())
                for word in analysis:
                    word_lemma = word.getLemmas()[0]
                    new_phrase_lemmatized += word_lemma + ' '
                    new_phrase += word.surfaceForm() + ' '

                lemmatized_keywords.write(new_phrase_lemmatized + '\n')
                keywords.write(new_phrase + '\n')
                count += 1
                if count == 5:
                    lemmatized_keywords.write('+++\n')
                    keywords.write('+++\n')
                    break


if __name__ == '__main__':

    PATH = '../fetchedCases'

    result = list(Path(PATH).glob('**/*.txt'))

    rk = Rake()
    lemmatized_keywords = open('lemmatized_keywords.txt', 'w')
    keywords = open('keywords.txt', 'w')

    count = 0
    for i in range(len(result)):
        rk.run(result[i])
        rk.write_phrase_scores_for_db(lemmatized_keywords, keywords)
    lemmatized_keywords.close()
    keywords.close()
