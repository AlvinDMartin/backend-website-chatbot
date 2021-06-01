#In[1]
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
from time import strftime
from A_save_datamodel import savedata
import os

_sd = savedata()
stemmer = LancasterStemmer()

class A_main():

    def Action(self , bool_data, bool_models):
    
        self.bool_data = bool_data
        self.bool_models = bool_models
        self.count_stop = 0

        with open("dataset/data.json",  encoding="utf8") as file:
            data = json.load(file)

        rundata = bool_data
        runmodel = bool_models

        if rundata == True:
            print("run DATA")
            _sd.learningdata(data)

        with open("datamodel/data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)

        tf.compat.v1.reset_default_graph()
        net = tflearn.input_data(shape=[None, len(training[0])]) #input layer
        net = tflearn.fully_connected(net, 8)   # 8neuron hidden layer
        net = tflearn.fully_connected(net, 8)   # 8neuron hidden layer
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")    #output layer
        net = tflearn.regression(net)
        model = tflearn.DNN(net)

        self.model = model
        self.words = words
        self.labels = labels
        self.data = data

        if runmodel == True:
            print("Run MODEL")
            model.fit(training, output, n_epoch=1000, batch_size=8, show_metric = True)
            model.save("datamodel/model.tflearn")

        model.load("datamodel/model.tflearn")

    def save_new_questions(self,val_patt):
        check = True

        if os.stat('Update_dataset/newquestions.json').st_size == 0:
            with open('Update_dataset/newquestions.json', 'w',encoding='utf-8') as out_file:
                json.dump([], out_file, indent = 1,ensure_ascii=False)
            print("Danh sách question đang trống!, đã được tạo mới")


        with open('Update_dataset/newquestions.json','r',encoding='utf-8') as in_file:
            data = json.load(in_file)

        for i in range(len(data)):
            if data[i] == str(val_patt):
                check = False
                print("câu hỏi đã tồn tại")

        if check == True:
            data.append(str(val_patt))

        in_file.close()

        with open('Update_dataset/newquestions.json', 'w',encoding='utf-8') as out_file:
            json.dump(data, out_file, indent = 1,ensure_ascii=False)

    def bag_of_words(self,s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i,w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return np.array(bag)

    def chat(self, input_text):
        print("Hãy bắt đầu nói chuyện với tôi- Tên tôi là BOT")
        while True:

            inp = input_text

            if inp.lower() == "tạm biệt":
                self.output_text = "Chúc quý khách một ngày tốt lành và hẹn gặp lại"
                return self.output_text
                break

            results = self.model.predict([self.bag_of_words(inp, self.words)])[0]
            results_index = np.argmax(results)
            tag = self.labels[results_index]
            
            if results[results_index] > 0.7:
                
                for tg in self.data["intents"]:
                    if tg['tag'] == tag:
                        self.count_stop = 0
                        responses = tg['responses']

                self.output_text = str(random.choice(responses))
                return self.output_text

            else:
                self.count_stop += 1
                print(self.count_stop)
                if self.count_stop == 1:
                    self.save_new_questions(str(inp))
                    self.output_text = str("Có lẽ tôi chưa được học, bạn liên hệ nhân viên để được giải đáp ạ.")
                    return self.output_text
                else:
                    self.output_text = str("Tôi chưa hiểu, bạn có thể lặp lại")
                    return self.output_text

    def hello(self, input_text=''):
        while True:
            day_time = int(strftime('%H'))
            if input_text == '':
                intro = "Xin chào quí khách! mình là Nhân viên tư vấn bán hàng thông minh, bạn cho mình biết tên ạ"
                self.output_text = intro
                return self.output_text
            else:
                name = self.input_text
                first_name = ''

                for l in name[::-1]:
                    if l != ' ':
                        first_name =str(l) +  first_name
                    else:
                        break

                if day_time < 12:
                    self.output_text = str("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(first_name))
                    return self.output_text

                elif 12 <= day_time < 18:
                    self.output_text = str("Chào buổi chiều bạn {}. Bạn có thể hỏi mình ngay bây giờ ạ.".format(first_name))
                    return self.output_text
                else:
                    self.output_text = str("Chào buổi tối bạn {}. Mình có thể giúp gì được cho bạn ạ.".format(first_name))
                    return self.output_text



