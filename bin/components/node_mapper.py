from copy import deepcopy
from misc.similarity import similarity, lemmatize, is_numeric


class NodeMapper:
	@staticmethod
	def phrase_process(query, db, tokens, d):
		NodeMapper.tokenizer(query, tokens)
		NodeMapper.delete_useless(query)
		NodeMapper.map(query,db, d)
		NodeMapper.individual_rank(query, d)
		NodeMapper.group_ranking(query,db)

	
	@staticmethod	
	def tokenizer(query, tokens):
		parse_tree = query.parse_tree
		parse_tree.root.token_type = 'ROOT'

		for i in range(len(parse_tree.root.children)):
			root_child = parse_tree.root.children[i]
			if NodeMapper.is_of_type(tokens, parse_tree, root_child, 'CMT_V', None):
				root_child.token_type = 'CMT'
		
		for i in range(len(parse_tree.all_nodes)):
			cur_node = parse_tree.all_nodes[i] 
			if cur_node.token_type == 'NA' and NodeMapper.is_of_type(tokens, parse_tree, cur_node, 'NEG',None):
				cur_node.token_type = 'NEG'
		i = 0
		while i < len(parse_tree.all_nodes):
		#for i in range(len(parse_tree.all_nodes)):
			cur_node = parse_tree.all_nodes[i]
			if cur_node.token_type == 'NA' and cur_node.relationship == 'mwe':
				if cur_node.word_order > cur_node.parent.word_order:
					cur_node.parent.label = cur_node.parent.label + ' ' + cur_node.label
				else:
					cur_node.parent.label =cur_node.label + ' ' + cur_node.parent.label
				parse_tree.delete_node(cur_node)
				i-=1
			i+=1


		cur_size = 0
		while cur_size != len(parse_tree.all_nodes):
			cur_size = len(parse_tree.all_nodes)
			#print (cur_size)
			i = 0
			while i < len(parse_tree.all_nodes):
			#for i in range(len(parse_tree.all_nodes)):
				#print i, len(parse_tree.all_nodes), parse_tree.all_nodes[i]
				cur_node = parse_tree.all_nodes[i]

				if cur_node.token_type == 'NA' and NodeMapper.is_of_type(tokens, parse_tree, cur_node, 'FT', 'function'):
					cur_node.token_type = 'FT'

				elif cur_node.token_type == 'NA' and NodeMapper.is_of_type(tokens, parse_tree, cur_node, 'OT', 'operator'):
					#print("X > ", cur_node.label)
					cur_node.token_type = 'OT'

				elif cur_node.token_type == 'NA' and NodeMapper.is_of_type(tokens, parse_tree, cur_node, 'OBT', None):
					cur_node.token_type = 'OBT'

				elif is_numeric(cur_node.label):
					cur_node.token_type = 'VT'

				elif cur_node.token_type == 'NA' and (cur_node.pos.startswith('NN') or cur_node.pos == 'CD'):
					#print "{0} is name".format(cur_node.label)
					cur_node.token_type = 'NTVT'

				elif cur_node.token_type == 'NA' and cur_node.pos.startswith('JJ'):
					#print "{0} is name".format(cur_node.label)
					cur_node.token_type = 'JJ'

				elif cur_node.token_type == 'NA' and NodeMapper.is_of_type(tokens, parse_tree, cur_node, 'QT', 'quantity'):
					cur_node.token_type = 'QT' 
				#print (cur_node.token_type, cur_node.pos)
				i+=1


	@staticmethod
	def delete_useless(query):
		parse_tree =  query.parse_tree
		query.original_parse_tree = deepcopy(parse_tree)
		i = 0
		while i < len(parse_tree.all_nodes):
			parse_tree_node = parse_tree.all_nodes[i]
			if parse_tree_node.token_type == 'NA' or parse_tree_node.token_type == 'QT':
				#print 'removing ', parse_tree_node.label
				cur_node = parse_tree_node
				#print (cur_node.label)
				if cur_node.label in ['on', 'in', 'of', 'by'] and len(cur_node.children):
					cur_node.children[0].prep = cur_node.label
				if cur_node.token_type == 'QT':
					cur_node.parent.QT = cur_node.function

				parse_tree.delete_node(cur_node)
				i-= 1
			i+=1



	@staticmethod
	def map(query, db, d):
		parse_tree = query.parse_tree
		all_nodes = parse_tree.all_nodes
		#print parse_tree.all_nodes[-1].parent.label

		for i in range(len(all_nodes)):
			tree_node = all_nodes[i]
			if tree_node.token_type == 'NTVT' or tree_node.token_type == 'JJ':
				db.is_schema_exist(tree_node, d)
				db.is_text_exist(tree_node)

				# for element in tree_node.mapped_elements:
				#  	print 'xxxx', tree_node.label, element.schema_element.relation.name,element.schema_element.name, element.similarity

				if len(tree_node.mapped_elements) == 0:
					tree_node.token_type = 'NA'
	
			elif tree_node.token_type == 'VT':
				OT = '='
				if tree_node.parent.token_type == 'OT':
					OT = tree_node.parent.function
				elif len(tree_node.children) == 1 and tree_node.children[0].token_type == 'OT':
					OT = tree_node.children[0].function
				db.is_num_exist(OT, tree_node)
				tree_node.token_type = 'VTNUM'
		#print '-------'
		#print parse_tree

		
	@staticmethod				
	def delete_no_match(query):
		parse_tree = query.parse_tree
		for i in range(len(parse_tree.all_nodes)):
			tree_node = parse_tree.all_nodes[i]
			if tree_node.token_type == 'NA':
				cur_node = tree_node
				parse_tree.delete_node(cur_node)
				if cur_node.label == 'on' or cur_node.label == 'in':
					cur_node.parent.prep = cur_node.label
				i-=1

	@staticmethod
	def individual_rank(query,d):
		tree_nodes = query.parse_tree.all_nodes
		for i in range(len(tree_nodes)):
			if len(tree_nodes[i].mapped_elements) == 0:
				#print ('{0} has none mapped elements'.format(tree_nodes[i].label))
				continue

			tree_node = tree_nodes[i]
			mapped_list = tree_node.mapped_elements
			#print mapped_list
			for j in range(len(mapped_list)):
				mapped_element = mapped_list[j]
				#print mapped_element
				similarity(tree_node, mapped_element,d)
			    
			#TODO: check how to sort this list	
			mapped_list.sort(key=lambda elem : elem.similarity, reverse=True)
			#print tree_node.label
			#print mapped_list
			#print 'similarities for ', tree_node.label
			# for k in range(len(mapped_list)):
			# 	print tree_node.label,  mapped_list[k].schema_element.relation.name,\
			# 	mapped_list[k].schema_element.name, mapped_list[k].similarity
			
			tree_node.mapped_elements = mapped_list

		tree_nodes = query.parse_tree.all_nodes
		#print(query.parse_tree)
		for i in range(len(tree_nodes)):
			tree_node = tree_nodes[i]
			if  tree_nodes[i].token_type != 'NTVT':
				continue

			delete_list = []
			tree_node = tree_nodes[i]
			mapped_list = tree_node.mapped_elements
			for j in range(len(mapped_list)):
				NT = mapped_list[j]
				k = j + 1
				while k < len(mapped_list):
				#for k in range(j + 1, len(mapped_list)):
					VT = mapped_list[k]
					if len(NT.mapped_values) == 0 and  (len(VT.mapped_values) != 0)  \
					and NT.schema_element == VT.schema_element:
						if NT.similarity >= VT.similarity:
							VT.similarity = NT.similarity
							#print VT.similarity, NT.similarity
							VT.choice = -1
							VT_position = k
							NT_idx = j
							tree_node.mapped_elements[NT_idx] = VT
							tree_node.mapped_elements[VT_position] = NT
							#print VT.similarity, NT.similarity
						delete_list += [VT_position]
					k+=1
			clean_mapped_elements = []
			for  j in range(len(mapped_list)):
				if not(j in delete_list): 
					clean_mapped_elements.append(mapped_list[j])
			tree_node.mapped_elements = clean_mapped_elements
			#print ('---------------')
			#print(query.parse_tree)
		

	@staticmethod
	def group_ranking(query, db):
		root = query.parse_tree.all_nodes[0]
		root_score = 0
		for i in range(len(query.parse_tree.all_nodes)):
			node = query.parse_tree.all_nodes[i]
			score = 0
			if len(node.mapped_elements) != 0:
				if len(node.mapped_elements) == 1:
					score = 1
				else:
					#print (node.label)
					#print(node.mapped_elements)
					score = 1.0 - (node.mapped_elements[1].similarity / node.mapped_elements[0].similarity)

				if score >= root_score:
					root = node
					root_score = score

		if root.label == 'ROOT':
			return

		root.choice = 0
		done = [False] * len(query.parse_tree.all_nodes)
		queue = [root, root]
		#print 'Group Ranking'
		while len(queue) != 0:
			parent = queue.pop(0)
			child = queue.pop(0)

			if not done[query.parse_tree.all_nodes.index(child)]:
				if parent != child:
					max_position = 0
					max_score = 0
					mapped_elements = child.mapped_elements
					for i in range(len(mapped_elements)):
						parent_element = parent.mapped_elements[parent.choice]
						child_element = child.mapped_elements[i]
						distance = db.schema_graph.distance(parent_element.schema_element, child_element.schema_element)
						#print ('distance btw ', distance, parent_element.schema_element.relation.name,
						# parent_element.schema_element.name,  child_element.schema_element.relation.name, child_element.schema_element.name)
						cur_score = parent_element.similarity * child_element.similarity * distance


						if cur_score > max_score:
							max_score = cur_score
							max_position = i
					#print child.label, max_position, mapped_elements
					child.choice = max_position
				
				if len(child.mapped_elements) == 0:
					for i in range(len(child.children)):
						queue += [parent]
						queue += [child.children[i]]
					if child.parent is not None:
						queue += [parent]
						queue += [child.parent]
				else:
					for i in range(len(child.children)):
						queue += [child]
						queue += [child.children[i]]

					if child.parent is not None:
						queue += [child]
						queue += [child.parent]

				done[query.parse_tree.all_nodes.index(child)] = True

		for i in range(len(query.parse_tree.all_nodes)):
			node = query.parse_tree.all_nodes[i]
			if node.token_type == 'NTVT' or node.token_type == 'JJ':
				if len(node.mapped_elements) > 0:
					if len(node.mapped_elements[node.choice].mapped_values) == 0 or \
					node.mapped_elements[node.choice].choice == -1: 
						node.token_type = 'NT'
					else:
						#print node.label, node.mapped_elements
						node.token_type = 'VTTEXT'
	
				
	@staticmethod
	def is_of_type(tokens, tree,node,token, tag):
		if NodeMapper.is_of_inner_type(tokens, tree, node, token, 1, tag):
			return True
		elif NodeMapper.is_of_inner_type(tokens, tree, node, token, 2, tag):
			return True

		return False


	@staticmethod
	def is_of_inner_type(tokens, tree, node, token, type, tag):
		label = ''
		if type == 1:
			label = node.label.lower()
		elif type == 2:
			tmp_label = node.label.split(' ')[0]
			label = lemmatize(tmp_label).lower()
		#print len(tokens.iter(token))
		tokenE = next(tokens.iter(token)) #.__next__()
		# print tokenE
		for phrase_item in tokenE.iter('phrase'):
			phrase_text = phrase_item.text.strip()
			if len(phrase_text.split(' ')) == 1 and not (' ' in  label):
				if label == phrase_text:
					node.token_type = token

					if tag is not None:
						try:
							attr_text = next(phrase_item.iter(tag)).text.strip()
							#print attr_text
							node.function = attr_text
						except:
							node.function = '.'
					return True

			elif len(phrase_text.split(' ')) == 1 and (' ' in  label):
				if (phrase_text + ' ') in label:
					node.token_type = token
					if tag is not None:
						try:
							attr_text = next(phrase_item.iter(tag)).text.strip()
							node.function = attr_text
						except:
							node.function = '.'

					return True
			elif label in phrase_text:
				if phrase_text == label:
					return True
				phrase_words = phrase_text.split(' ')
				j = 0
				while j < len(phrase_words):
					if phrase_words[j] == label:
						break
					j+=1

				index = node.word_order
				if (index - j) > 1:
					whole_phrase =  ' '
					k = 0
					while k < len(phrase_words) - 1 and tree.search_node_by_order(index - j  + k) is not None:
						if j == k:
							whole_phrase += label + ' '
						else:
							whole_phrase += str(tree.search_node_by_order(index - j  + k))
						k+=1

					if tree.search_node_by_order(index-j+len(phrase_words)-1) is not None:
						whole_phrase += tree.search_node_by_order(index-j+len(phrase_words)-1).label

					if phrase_text in whole_phrase:
						node.token_type = token
						if tag is not None:
							attr_text = next(phrase_item.iter(tag)).text.strip()
							node.function = attr_text
						node.label = phrase_text
						for k in range(len(phrase_words)):
							if j != k:
								if tree.search_node_by_order(index -j + k) is not None:
									tree.delete_node(tree.search_node_by_order(index-j+k))

						return True
		return False

	
