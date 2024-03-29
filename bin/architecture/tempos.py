import sys
import time
sys.path.append('../')
import os
import json
import xml.etree.ElementTree as et
from rdbms.rdbms import RDBMS
from data_structure.query import Query 
from components.stanford_parser import StanfordParser
from components.node_mapper import NodeMapper
from components.entity_resolution import entity_resolute
from components.tree_structure_adjustor import TreeStructureAdjustor
from components.explainer import explain
from components.sql_translator import translate
from misc.similarity import load_model, lemmatize
from misc.process_command import CommandProcessor

import glob
import pickle
os.environ['CLASSPATH'] = "D:/nalir-py/jars/new_jars/"
token_path = "../"+'/'.join(os.getcwd().split('/')[:-1] + ['zfiles', 'tokens.xml'])
config_path = '../'+'/'.join(os.getcwd().split('/')[:-1] + ['config', 'config.json'])

col = glob.glob("../zfiles/dict_*")
#load_model()
#print(col)
global dicts 
dicts = {}

for file in col:
    arq = open(file, "rb")
    nome = lemmatize(file.split('_')[1])
    #print(nome)
    d = pickle.load(arq)
    dicts[nome] = d
    arq.close()

config_stream = open(config_path, 'r')
config_obj = json.load(config_stream)

commandProcessor = CommandProcessor()
#print('Reading tokens')
tokens = et.parse(token_path)

#print('connecting to database')

#print (config_obj['database'])

rdbms = RDBMS(config_obj['database'], config_obj['connection'])

def run(query):
    #print 'building query'
    #print(query.sentence.output_words)
    
    #print 'Stanford Parser running'
    StanfordParser(query)
    
    #print 'Node mapper running'
    NodeMapper.phrase_process(query,rdbms,tokens, dicts)
    
    #print 'Resolution Entities running'
    entity_resolute(query)
    
    #print 'Tree Structure Adjustor running'
    TreeStructureAdjustor.tree_structure_adjust(query,rdbms)
    
    #print 'Explainer running'
    #explain(query)
    
    
    #print 'Translate running'
    translate(query, rdbms)
    
    return query.translated_sql

def consulta(query="return me the authors"):
    q = Query(query,rdbms.schema_graph)
    return run(q)
#'''
query = Query("return me the total citations of papers in the VLDB conference in 2005. ", rdbms.schema_graph)
r = run(query)
print ('\n'+ r+ '\n\n')

#'''
'''
arq = open('../queries2.txt','r')
s = int(input("start:"))
e = int(input("end:"))
exp = arq.readlines()[s:e:]
arq.close()
c = s
tempo = 0
results = open('../comEntidades'+str(e)+'.txt','w')
for q in exp:
    q = q.replace('\n', '').replace('\r', '').replace(',','')
    if len(q) > 2:
        c+= 1
        print( c, ')')
        results.write(str(c)+')\n\n')
        query = Query(q, rdbms.schema_graph)
        t1 = time.time()
        r = run(query)
        t2 = time.time()-t1
        tempo += t2/(e-s)
        print ('\n\n'+ r+ '\n\n')
        results.write(str(query.sentence)+'\n'+r+'\n\n')

results.write("\ntempo: "+str(tempo)+"\n")
results.close()
#'''
