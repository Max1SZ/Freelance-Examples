import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("stripes",'v'))
print(lemmatizer.lemmatize("stripes",'n'))