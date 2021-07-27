#In[]
from underthesea import word_tokenize
from nltk.stem import WordNetLemmatizer
from A_save_datamodel import savedata
lemmatizer = WordNetLemmatizer()
ignore_letter = ['?','!', '.', ',']
_sd = savedata()

text ="bạn có bán giầy ko"
doc = _sd.remove_stop_word(text.lower())
doc = word_tokenize(doc)
words = [lemmatizer.lemmatize(w) for w in doc if w not in ignore_letter]
print(words)

# %%
