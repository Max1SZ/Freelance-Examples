from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer

ss = SnowballStemmer("spanish")
ps = PorterStemmer()
palabras = ["program","programming","programer","programs","programmed"]
for palabra in palabras:
    print(palabra, "\t", ps.stem(palabra))
    print()