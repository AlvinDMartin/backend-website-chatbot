#In[1]
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from tensorflow import keras
import random
import json
import pickle
from time import strftime
from A_save_datamodel import savedata
from Open_Webbrowser import open_webbrowser
import os
from nltk.stem import WordNetLemmatizer
# import matplotlib.pyplot as plt

_sd = savedata()
open_web = open_webbrowser()
stemmer = LancasterStemmer()
lemmatizer = WordNetLemmatizer()

class A_main():

    def Action(self , bool_data, bool_models):
    
        self.bool_data = bool_data
        self.bool_models = bool_models

        with open("dataset/intents_VN.json",  encoding="utf8") as file:
            data = json.load(file)
        file.close()

        rundata = bool_data
        runmodel = bool_models

        if rundata == True:
            print("run DATA")
            _sd.learningdata(data)

        with open("datamodel/data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)
        f.close()


        self.words = words
        self.labels = labels
        self.data = data

        model = keras.models.Sequential([
                keras.layers.Input(shape=(len(training[0]))),
                keras.layers.Dense(128, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(len(output[0]), activation='softmax')
                ])
        #model.summary()

        if runmodel == True:
            print("Run MODEL")

            optimizer = 'Adam'
            model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"])
            hist = model.fit(np.array(training), np.array(output), epochs=300, batch_size=5, verbose=1)
            #model.save(r'datamodel/chatbot_models.h5')
            model.save_weights('datamodel/chatbot_models.h5')
            # plt.plot(hist.history['loss'])
            # plt.show()
        

        #model = keras.models.load_model('datamodel/chatbot_models.h5')
        model.load_weights('datamodel/chatbot_models.h5')
        self.model = model

    def save_new_questions(self,val_patt):
        check = True

        if os.stat('Update_dataset/newquestions.json').st_size == 0:
            with open('Update_dataset/newquestions.json', 'w',encoding='utf-8') as out_file:
                json.dump([], out_file, indent = 1,ensure_ascii=False)
            out_file.close()
            print("Danh sách question đang trống!, đã được tạo mới")


        with open('Update_dataset/newquestions.json','r',encoding='utf-8') as in_file:
            data = json.load(in_file)
        in_file.close()

        for i in range(len(data)):
            if data[i] == str(val_patt):
                check = False
                print("câu hỏi đã tồn tại")

        if check == True:
            data.append(str(val_patt))

        in_file.close()

        with open('Update_dataset/newquestions.json', 'w',encoding='utf-8') as out_file:
            json.dump(data, out_file, indent = 1,ensure_ascii=False)
        out_file.close()

    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        #s_words = [stemmer.stem(word.lower()) for word in s_words]
        s_words = [lemmatizer.lemmatize(word) for word in s_words]

        for se in s_words:
            for i,w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return np.array(bag)

    def chat(self, input_text):
        while True:

            inp = input_text

            # if inp.lower() == "tạm biệt":
            #     self.output_text = "Chúc quý khách một ngày tốt lành và hẹn gặp lại"
            #     return self.output_text
            #     break

            bow = self.bag_of_words(inp, self.words)
            results = self.model.predict(np.array([bow]))[0]
            results_index = np.argmax(results)

            #Draw Test
            # plt.xlabel('Vị trí tag')
            # plt.ylabel('Phần trăm')
            # plt.axis([0, len(results), -2, 102])
            # plt.title('Predict')
            # plt.legend()
            # for i, r in enumerate(results):
            #     plt.scatter(i,r * 100,c='b')
            # plt.scatter(results_index,results[results_index] * 100,c='r')
            # plt.show()


            tag = self.labels[results_index]
            if results[results_index] > 0.55:
                for tg in self.data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                self.output_text = str(random.choice(responses))

                #openweb
                # if tag == "Ý kiến khách hàng":
                #     open_web.run_web("https://docs.google.com/forms/d/1AwwqmHLFqH5CCEfA8ft_6RV6Fy7oKUn-B8OdmFZMUsw/edit?usp=sharing")
                #     return self.output_text
                # elif tag == "Tư vấn giá sản phẩm":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/search/name")
                #     return self.output_text
                # elif tag =="Giới thiệu sản phẩm":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/search/name")
                #     return self.output_text
                # elif tag =="Thanh toán hóa đơn":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/cart")
                #     return self.output_text
                # elif tag =="Mở trang mua đầm":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/search/category/Dress/name/all/min/0/max/0/rating/0/order/newest/pageNumber/1")
                #     return self.output_text
                # elif tag =="Mở trang mua nguyên bộ":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/search/category/Set/name/all/min/0/max/0/rating/0/order/newest/pageNumber/1")
                #     return self.output_text
                # elif tag =="Mở trang mua chân váy":
                #     open_web.run_web("https://chopper-shop-1.herokuapp.com/search/category/Skirt/name/all/min/0/max/0/rating/0/order/newest/pageNumber/1")
                #     return self.output_text
                # else:
                #     return self.output_text
                return self.output_text

            else:
                if len(inp.split()) < 2:
                    self.output_text = str("Tôi chưa hiểu, bạn hãy hỏi câu hỏi dài hơn một chút nhé.")
                elif len(inp.split()) >= 15:
                    self.output_text = str("Câu hỏi dài quá tôi không hiểu hết, bạn hãy hỏi từng câu nhé.")
                else:    
                    self.save_new_questions(str(inp))
                    self.output_text = str("Có lẽ tôi chưa được học, bạn đợi Admin để được giải đáp nhé.")
                return self.output_text
                # self.output_text = str("Tôi chưa hiểu, bạn có thể lặp lại")
                # return self.output_text

    def hello(self, input_text=''):
        while True:
            day_time = int(strftime('%H'))
            if input_text == '':
                intro = "Xin chào quí khách. Tôi là Nhân viên tư vấn bán hàng thông minh. Bất đầu hỏi tôi đi nào"
                self.output_text = intro
                return self.output_text
            else:
                name = input_text
                # first_name = ''

                # for l in name[::-1]:
                #     if l != ' ':
                #         first_name =str(l) +  first_name
                #     else:
                #         break

                if day_time < 12:
                    self.output_text = str("Chào buổi sáng bạn {}.Tôi là nhân viên ảo. Chúc bạn một ngày tốt lành.".format(name))
                    return self.output_text

                elif 12 <= day_time < 18:
                    self.output_text = str("Chào buổi chiều bạn {}. Tôi là nhân viên ảo. Bạn có thể hỏi tôi ngay bây giờ nhé.".format(name))
                    return self.output_text
                else:
                    self.output_text = str("Chào buổi tối bạn {}.Tôi là nhân viên ảo. Tôi có thể giúp gì được cho bạn nà.".format(name))
                    return self.output_text




# %%
