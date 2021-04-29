import sys
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
from data_structure.parse_tree import ParseTree
from misc.similarity import load_model, lemmatize
from misc.process_command import CommandProcessor

import glob
import pickle
#from __future__ import print
os.environ['CLASSPATH'] = "D:/nalir-py/jars/new_jars/"
token_path = '../'+'/'.join(os.getcwd().split('/')[:-1] + ['zfiles', 'tokens.xml'])
config_path = '../'+'/'.join(os.getcwd().split('/')[:-1] + ['config', 'config.json'])

config_stream = open(config_path, 'r')
config_obj = json.load(config_stream)

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

commandProcessor = CommandProcessor()
#print('Reading tokens')
tokens = et.parse(token_path)

#print('connecting to database')

#print (config_obj['database'])

rdbms = RDBMS(config_obj['database'], config_obj['connection'])

# line = raw_input('command: ')
# query = commandProcessor.process_input(line)
# while query != CommandProcess.EXIT_COMMAND:
# 	if query.process_input(line) is None:
# 		print('type a valid command')
# 	line = raw_input('command: ')
# print 'Loading Word Embedding model'
# load_model()

print('building query')
#query = Query('return me the authors of "Making data system usable"',rdbms.schema_graph)
#query = Query('return me the number of papers written by "H. V. Jagadish", "Yunyao Li", and "Cong Yu"',rdbms.schema_graph)
#query = Query('return me the author in the "University of Michigan" whose papers in Databases area have the most total citations ',rdbms.schema_graph)
query = Query('return me the author in the "University of Michigan" whose papers have the most total citations.',rdbms.schema_graph)

print ('Stanford Parser running')
StanfordParser(query)
print ('Node mapper running')
NodeMapper.phrase_process(query,rdbms,tokens, dicts)

print ('Resolution Entities running')
entity_resolute(query)

print ('Tree Structure Adjustor running')
TreeStructureAdjustor.tree_structure_adjust(query,rdbms)
print (query.query_tree)
#print ('Explainer running')
#explain(query)
print ('#################')
print (query.query_tree)
print ('#################')
print ('Translate running')
translate(query, rdbms)
#print (query.parse_tree)
print(query.translated_sql)
