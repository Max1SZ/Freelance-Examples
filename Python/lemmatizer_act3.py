import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet 
nltk.download('averaged_perceptron_tagger_eng')
lemmatizer = WordNetLemmatizer()
oracion = "the striped bats are hanging on their feet for best"
word_list = nltk.word_tokenize(oracion)
print(word_list)
print(nltk.pos_tag(word_list))