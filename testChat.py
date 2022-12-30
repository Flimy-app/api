import aiml
import re
import string
import time
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import ngrams
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
# k = aiml.Kernel()
# k.learn("std-startup.xml")
# k.respond("load aiml b")
# print("Parsing aiml files")
# k.learn("testChatto.aiml")
# print("jalan kok ini program")
# rabin = []

# daisu = []
pattern_to_template = {}
temp_pattern = None
with open('file.aiml', 'r') as f:
  lines = f.readlines()
  for line in lines:
    if '<pattern>' in line:
      temp_pattern = line.split('<pattern>')[1].split('</pattern>')[0]
    if '<template>' in line:
      if (temp_pattern is None):
        print("Ga ada pattern bro")
        continue
      pattern_to_template[temp_pattern] = line.split('<template>')[1].split('</template>')[0]
      temp_pattern = None
data = [(pattern, template) for (pattern, template) in pattern_to_template.items()]


def casefolding(input_text):
    input_text = input_text.lower()
    return input_text

def numberfilter(input_text):
    input_text = re.sub(r"\d+", "", input_text)
    return input_text

def symbolfilter(input_text):
    input_text = input_text.translate(str.maketrans('', '', string.punctuation))
    return input_text

def filtering(input_text):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    input_text = stopword.remove(input_text)
    return input_text

def stemming(input_text):
    factorystem = StemmerFactory()
    stemmer = factorystem.create_stemmer()
    input_text = stemmer.stem(input_text)
    return input_text
    
def whitespacefilter(input_text):
    input_text = input_text.strip()
    input_text = input_text.replace(" ", "")
    return input_text

def tokenizing(input_text):
    input_text = list(ngrams(input_text, 3))
    return input_text

def hashing(input_text):
    rabin = []
    for i in range(len(input_text)):
        var = input_text[i]
        length = len(var) - 1
        hash = 0
        for x in var:
            hash = hash +ord(x)*(5**length)
            length = length - 1
        rabin.append(hash)
    #     print(hash)
    # print(rabin)
    # print("")
    return rabin

def dice(sama, a, b):
    temp = 2 * sama / (a + b)
    temp = temp * 100
    return temp


app = Flask(__name__)
CORS(app, support_credentials=True)
api = Api(app)
# cors = CORS(app, resources={r"*": {"origins": "http://localhost:3000/Chatbot"}})
@app.route("/result", methods=['POST', 'GET'])
# @cross_origin(supports_credentials=True)
def chateraise():
    return ("haleluya")
    tempo = 0
    sama = 0
    daisutemp = 0
    input_text = request.get_json()
    input_text = input_text['query']
    # input_text = input(">Human: ")
    start = time.time() 
    input_text = casefolding(input_text)
    input_text = numberfilter(input_text)
    input_text = symbolfilter(input_text)
    input_text = filtering(input_text)
    input_text = stemming(input_text)
    input_text = whitespacefilter(input_text)
    input_text = tokenizing(input_text)
    rabinori = input_text   
    rabin = hashing(input_text)
    for n in range(len(data)):
        input_text2 = data[n][0]
        input_text2 = casefolding(input_text2)
        input_text2 = numberfilter(input_text2)
        input_text2 = symbolfilter(input_text2)
        input_text2 = filtering(input_text2)
        input_text2 = stemming(input_text2)
        input_text2 = whitespacefilter(input_text2)
        input_text2 = tokenizing(input_text2)
        rabin2ori = input_text2
        rabin2 = hashing(input_text2)
        for i in range(len(rabin)):
            for j in range(len(rabin2)):
                if(rabin[i] == rabin2[j]):
                    if(rabinori[i] == rabin2ori[j]):
                        sama = sama + 1
        if (tempo < dice(sama, len(rabin), len(rabin2))):
            daisutemp = n
            tempo = dice(sama, len(rabin), len(rabin2))
        # daisu.append(dice(sama, len(rabin), len(rabin2)))
        # if (dice(sama, len(rabin), len(rabin2)) > 70):
        #     checker = 1
        #     daisutemp = len(daisu) - 1
        #     sama = 0
        #     break
        sama = 0
    # if (checker == 0):
    # for i in range(len(daisu)):
    #     if (daisu[i] > daisu[daisutemp]):
    #         daisutemp = i
    # print("Jalan kok")
    # print("")
    # print(daisu[daisutemp])
    if(tempo > 50):
        # print(tempo)
        return(data[daisutemp][1])
    else:
        # print(tempo)
        return("Saya tidak mengerti pertanyaan anda. Mohon gunakan pertanyaan dari daftar pertanyaan")
    # daisutemp = 0
    # daisu= []
    # tempo = 0a
    # end = time.time()a
    # print(end - start)a
    # response = k.respond(input_text)
    # print("Bot> " + response)
if __name__ == '__main__':
    app.run(debug=True)
