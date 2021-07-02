import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
import pickle
from underthesea import word_tokenize
lemmatizer = WordNetLemmatizer()
stemmer = LancasterStemmer()

class savedata:

    def remove_stop_word(self, line):

        # Danh sách stopword
        f = open("stopword.txt", "r",encoding="utf8")
        stopword = f.read()
 
        words = []
        for word in line.strip().split():
            if word not in stopword:
                words.append(word)
        return ' '.join(words)


    def learningdata(self, data):
        self.data = data

        words = []
        labels = []

        X_train = []
        Y_train = []

        ignore_letter = ['?','!', '.', ',']

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                patt = self.remove_stop_word(pattern.lower())

                wrds = word_tokenize(patt)
                #wrds = nltk.word_tokenize(patt)          #tách từ chữ
                
                words.extend(wrds)
                X_train.append(wrds)
                Y_train.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [lemmatizer.lemmatize(w) for w in words if w not in ignore_letter] # Qui đổi về từ gốc (dùng trong tiếng anh)

        words = sorted(list(set(words)))
        labels = sorted(labels)


        training = []
        output = []

        out_empty = [0] * len(labels)   # tạo 1 mảng các số 0  gắn với label tag

        for i, doc in enumerate(X_train):
            bag = []

            wrds = [lemmatizer.lemmatize(w) for w in doc]       # Qui đổi về từ gốc (dùng trong tiếng anh)

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = list(out_empty)
            output_row[labels.index(Y_train[i])] = 1

            training.append(bag)
            output.append(output_row)

        training = list(training)
        output = list(output)

        with open("datamodel/data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output),f)
