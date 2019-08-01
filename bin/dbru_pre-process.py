import pickle


dict_relations = { 'aluno': ['student', 'pupil', 'undergraduate', 'alumnus', "customer",'client'],\
                   'aplicacao': ["application", 'appliance', 'function', 'role','post','duty','mission'],\
                   'curso_aluno': ['course', 'class','school', 'graduation'],\
                   'grupo' : ['group','team', 'troupe', 'cluster', 'committee'],\
                   'movimentacao' : ['movement', 'transaction', 'deal', 'negotiation', 'operation'],\
                   'restaurante' : ['restaurant', 'eatery'],\
                   'setor': ['sector', 'section', 'department', 'district'],\
                   'usuario': ['user', 'employee', 'functionary', 'servant','worker','clerk'],\
                   'tab_estruturada': ['structure', 'frame', 'table', 'index'],\
                   'tipo_alimentacao': ['meals', 'lunch', 'dinner', 'breakfast']
                   }

dict_usuario = { 'id' : ['id','index'],\
                 'nome': ['name','user'],\
                 'senha':['password']
                }

dict_aluno = { 	     'id' : ['id','index','identification'],\
                     'cpf' : ['cpf'],\
                     'dt_nascimento': ['birthday', 'nativity','birth'],\
                     'foto': ['photo', 'photography'],\
                     'nome_pessoa':['name','designation'],\
                     'rg':['register','rg']
                     }
                     
dict_aplicacao = {   'id' : ['id','index','identification'],\
                     'date_created' : ['created','produced'],\
                     'descricao': ['description', 'portrait'],\
                     'dtfim':['end'],\
                     'dtinicio':['begin']
                     }              

dict_curso_aluno = { 'id' : ['id','index','identification'],\
                     'ano_ingresso' : ['entrance','admission'],\
                     'cod_curso': ['code', 'course_code'],\
                     'matr_aluno':['registration','registry','enrollment','registry'],\
                     'nome_curso':['course','program', 'name', 'study', 'course_name']                     
                     }  

dict_grupo = { 	    'id' : ['id','index','identification'],\
                    'descricao': ['description', 'portrait']
                    }
                    
dict_menu = { 	    'id' : ['id','index','identification'],\
                    'descricao': ['description', 'portrait']
                    }

dict_movimentacao = {	'id' : ['id','index','identification'],\
                        'num_venda': ['sales'],\
		              	'quantidade': ['amount','quantity'],\
		              	'saldo': ['sum','balance'],\
		                'tipo_operacao': ['operation'],\
		                'total_pago': ['paid'],\
		                'troco': ['change'],\
		                'valor_item':['price','item_value'],\
		                'valor_fornecedor':['cost','supply_value']	                
                    }

dict_restaurante = { 'id' : ['id','index','identification'],\
                    'descricao': ['description', 'portrait'],\
                    'responsavel':['observant','responsible']
                    }

dict_tipo_alimentacao = {   'id' : ['id','index'],\
                 	    'descricao' : ['description', 'name'],\
                 	    'valor_aluno': ['student_price','price'],\
                 	    'valor_fornecedor':['supplier_price','cost'],\
                        'quantidade_maxima':['max']
                     	}

dict_tab_estruturada = {'id_tabela' : ['id','index'],\
                 	    'cod_tabela' : ['table'],\
                 	    'descricao' : ['description', 'type'],\
                 	    'item_tabela':['item']
                     	}
                     		
dict_setor = {'id' : ['id','index'],\
              'descricao' : ['description', 'name'],\
              'restaurante_id':['restaurant']
             }


outfile = open('zfiles/dict_relations','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_usuario','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_aluno','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_aplicacao','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_curso_aluno','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_grupo','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_menu','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_movimentacao','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_restaurante','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_tipo_alimentacao','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_tab_estruturada','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_setor','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

