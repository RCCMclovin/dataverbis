from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize, download



try:
    p = pos_tag(word_tokenize('dog'))
    print('Todos os modulos necessarios ja foram instalados')
except:
    print("Fazendo download de modulos necessarios.\n")
    download('punkt')
    download('averaged_perceptron_tagger')
    download('wordnet')

arq = open('bin/config/config.json','w')
database = str(input("Entre com o banco de dados alvo: "))
host = str(input("Entre com o nome do host: "))
user = str(input("Entre com seu usuario mysql: "))
senha = str(input("Entre com sua senha: "))

arq.write("{\n\"connection\":{\n\"host\":\""+host+"\",\n\"password\":\""+senha+"\",\n\
\"user\":\""+user+"\",\n\"database\":\""+database+"\"\n},\n\"database\": \""+\
database+"\"\n}")
arq.close()

