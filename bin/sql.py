import sys
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

token_path = '/'.join(os.getcwd().split('/')[:] + ['bin','zfiles', 'tokens.xml'])
config_path = '/'.join(os.getcwd().split('/')[:] + ['bin','config', 'config.json'])
col_path = '/'.join(os.getcwd().split('/')[:] + ['bin','zfiles'])

col = glob.glob(col_path+"/dict_*")
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

#print dicts
config_stream = open(config_path, 'r')
config_obj = json.load(config_stream)

commandProcessor = CommandProcessor()
#print('Reading tokens')
tokens = et.parse(token_path)

#print('connecting to database')

#print (config_obj['database'])

rdbms = RDBMS(config_obj['database'], config_obj['connection'])

def run(q):
    #print q
    query = Query(q,rdbms.schema_graph)
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

#raise TypeError
print('consulta = '+sys.argv[1])
print
print run(sys.argv[1])
