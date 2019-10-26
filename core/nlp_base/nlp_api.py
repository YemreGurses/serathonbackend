import jpype as jp
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rakepath = os.path.join(BASE_DIR, "keyword_extraction/src")

sys.path.append("../keyword_extraction/src")
from rake import Rake

# ZEMBEREK_PATH = os.path.join(BASE_DIR, "zemberek-full.jar")
ZEMBEREK_PATH = "../zemberek-full.jar"

#TODO: Rename
class NlpBase:
    def __init__(self, open_jvm = False):
        self.open_jvm = open_jvm

        if open_jvm == True:
            jp.startJVM(jp.getDefaultJVMPath(), '-ea', 
                    '-Djava.class.path=%s' % (ZEMBEREK_PATH))

        self.created_morphology = False
        self.created_extractor = False
        self.extractor = Rake() 


    #Given a text, returns list of sentences
    def split_sentences(self, text_to_split):
        extractor = self.get_extractor()
        
        sentence_list = list(extractor.fromParagraph(text_to_split).toArray())
        return sentence_list

    #Given a single word, returns all possible lemmas
    def lemmatize_single_word(self, word):
        pass
    
    def get_morphology(self):
        if not self.created_morphology:
            TurkishMorphology = jp.JClass(
                    'zemberek.morphology.TurkishMorphology')
            self.morphology = TurkishMorphology.createWithDefaults()
            self.created_morphology = True

        return self.morphology

    # IMPORTANT: get_extractor returns extractor_zemberek,
    # not extractor itself! It is a good idea to rename these
    def get_extractor(self):
        if not self.created_extractor:
            TurkishSentenceExtractor = jp.JClass(
                    'zemberek.tokenization.TurkishSentenceExtractor')
            self.extractor_zemberek = TurkishSentenceExtractor.DEFAULT
            self.created_extractor = True

        return self.extractor_zemberek

    #Given text, returns list of lemma words
    def lemmatize_all(self, text):
        
        morphology = self.get_morphology()
        sentence_list = self.split_sentences(text)
        
        lemma_list = []
        for sentence in sentence_list:
            analysis = list(morphology.analyzeAndDisambiguate(sentence).bestAnalysis().toArray())
            for word in analysis:
                lemma = word.getLemmas()[0]
                if lemma.isalpha():
                    lemma_list.append(lemma) 

        return lemma_list
    

    #Given text returns list of highest scored keywords
    def extract_keywords(self, text):
        all_phrases = self.extractor.run(text) 
        return [elem[0] for elem in all_phrases[:5]]

    def tokenize(self, word):
        pass


    def __del__(self):
        if self.open_jvm == True:
            jp.shutdownJVM()


if __name__ == "__main__":
    base = NlpBase()
    text = '''Bir zamanlar küçük bir kız varmış, bu küçük kız inatçılığından dolayı hep kırmızı başlıklı bir pelerin giyermiş. Ailesinin ısrarına rağmen bu pelerini hiç çıkarmazmış ve artık bu pelerin kokuşmaya başlamış. Bu yüzden herkes ona kırmızı başlıklı kız dermiş. Kırmızı başlıklı kız; ailesinin sözünden çıkan, illet, düşman başına, yaramaz mı yaramaz bir çocukmuş.'''

    #print(base.split_sentences(text))
    #print(base.lemmatize_all(text))
    print(base.extract_keywords(text))
    
