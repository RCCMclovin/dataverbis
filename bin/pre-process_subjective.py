import pickle

dict_relations = {'products':['products'],\
                  'attributes':['attributes']}

dict_products = { 'name' : ['name','product'],\
                     'category' : ['category', 'type'],\
                     'brand' : ['brand', "maker"],\
                     'model_number' : ['model']
                     }

dict_attributes = { 'att_name': ['name', 'attribute'],\
                'value': ['value'],\
                'sentiments': ['sentiments', 'adjective', 'is']
                }


outfile = open('zfiles/dict_relations','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_products','wb')
pickle.dump(dict_products, outfile)
outfile.close()

outfile = open('zfiles/dict_attributes','wb')
pickle.dump(dict_attributes, outfile)
outfile.close()
