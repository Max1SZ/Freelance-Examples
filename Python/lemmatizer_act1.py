import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
oracion = ("The striped bats are hanging on their feet for best")
word_list = nltk.word_tokenize(oracion)
print(word_list)