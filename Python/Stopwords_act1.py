import nltk 
nltk.download('stopwords')
from nltk.corpus import stopwords

espaniol = stopwords.words("spanish")

print(espaniol)