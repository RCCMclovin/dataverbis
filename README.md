# Data Verbis

## Instalação

Primeiramente verifique se sua máquina possui npm, python 2.7 e as bibliotecas gensim, setuptools, glob e nltk.

Após clonar o repositório, faça o download do banco de dados em:
https://s3.amazonaws.com/umdb-users/cjbaik/mas.sql

E carregue-o em um banco de dados MySQL ativo em sua máquina.

Carregue também o arquivo setup_mas.sql, disponível na raiz desse projeto, no MySQL.

Faça download também dos jars em:
https://drive.google.com/file/d/1ggwTbEQsYHb0idMpr0qWvKjk7ulSJQTy/view

Guarde os jars dentro da pasta bin.

Execute o programa config.py para fazer as configurações iniciais.

obs.: config.py ira requisitar informações para acessar o banco de dados que acabamos de baixar.
O config.py deverá ser executado em python 2.
Digite as informações entre aspas simples ou duplas senão ocorrerá um erro.


Para iniciar a interface, execute os seguintes comandos:
```
npm install
npm start
```
O servidor será inicializado na porta 3000.

