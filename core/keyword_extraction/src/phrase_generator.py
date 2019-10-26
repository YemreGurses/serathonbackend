import string
import jpype as jp


#class for a single word instance
class Token:
    def __init__(self, word, pos, morphemes, lemma):
        self.word = word 
        self.pos = pos #i.e Noun, Verb etc.
        self.morphemes = morphemes #list of morphemes
        self.lemma = lemma 

    def __repr__(self):
        return 'word: {}\n pos: {}\n morphemes: {}\n lemma: {}\n\n'.format(self.word, self.pos, self.morphemes, self.lemma)

#TODO: Consider NER

#Constructs a list of possible keywords
class PhraseGenerator:
    
    def __init__(self):
        self.sentences = []
        self.phrases = []
        self.tokens = [] 

        self.valid_pos = ['Noun', 'Adjective', 'Conjunction'] 

        self.sent_extractor = None #To split into sentences
        self.ne_extractor = None #To remove named entities (Person, Org..)

        self.max_len = 5
        self.zemberek_inited = False

    def init_zemberek(self):
    
        TurkishSentenceExtractor = jp.JClass('zemberek.tokenization.TurkishSentenceExtractor')
        TurkishMorphology = jp.JClass('zemberek.morphology.TurkishMorphology')     
        
        self.morphology = TurkishMorphology.createWithDefaults()
        self.sent_extractor = TurkishSentenceExtractor.DEFAULT
    
    def run(self, text):
        if not self.zemberek_inited:
            self.init_zemberek()
            self.zemberek_inited = True

        self.split_sentences(text)
        self.create_tokens()
        self.generate_base_phrases()
        #self.permutate()
        

        
        return self.phrases
    
    #First split the sentences using zemberek tokenization
    def split_sentences(self, data):
        self.sentences = list(self.sent_extractor.fromParagraph(data).toArray())
    
    #Label every sentence with part of speech tags
    def create_tokens(self):
        self.tokens = []
        for sentence in self.sentences:
            analysis = list(self.morphology.analyzeAndDisambiguate(sentence).bestAnalysis().toArray())
            sent_pos = []
            for word in analysis:
                base_word = word.surfaceForm()
                pos = word.getPos().toString()
                morphemes = word.formatLexical()
                lemmas = word.getLemmas()[0]
                
                token = Token(base_word, pos, morphemes, lemmas)
                sent_pos.append(token)
            
            self.tokens.append(sent_pos)
    
    #TODO: Implement when Zemberek supports
    def remove_named_entities(self):
        for sentence in self.sentences:
            pass     

    #TODO: Add simple clauses
    def is_valid_stopword(self, pos):
        if pos in self.valid_pos:
            return True
    

    def generate_base_phrases(self):
        self.phrases = []
        for sentence in self.tokens:
            phrase = []
            for token in sentence:
                word = token.word
                pos = token.pos
                if self.is_valid_stopword(pos):
                    phrase.append(word)
                else:
                    self.phrases.append(phrase)
                    phrase = []
            if phrase != []:
                self.phrases.append(phrase)
                phrase = []

    #TODO: May not use it
    def refine(self):
        new_phrases = []
        for phrase in self.phrases:
            for i, word in enumerate(phrase):
                for j in range(2, self.max_len + 1):
                    if i + j < len(phrase):
                        new_phrases.append(phrase[i:i+j])
        
        self.phrases = new_phrases
        
        for phrase in self.phrases:
            if phrase != []:
                print(phrase)

if __name__ == '__main__':
    filename = '../example_cases/sample1.txt'
   
    with open('../stopwords.txt') as sf:
        stopwords = sf.read().split()
    
    t = PhraseGenerator()
    with open(filename) as f:
        data = f.read()
        print (data)
        t.run(data)
        

