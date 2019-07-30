from .mapped_schema_element import MappedSchemaElement
from misc.similarity import similarity_list, if_list_similar, similarity_words, if_schema_similar

class SchemaElement:

    def __init__(self, id=-1, name=None, type_elem=None):
        self.element_id = id
        self.name = name
        self.type = type_elem
        self.relation = None
        self.attributes = []
        self.primary_key = None
        self.default_attribute = None
        self.in_elements = []
    
    def is_schema_exist(self, tag, dicts):
        mapped_schema_element = None
        if self == self.relation.default_attribute:
            if str(self.relation.name) in dicts and\
               str(self.name) in dicts[str(self.relation.name)] and\
               (if_list_similar(tag, dicts['relation'][str(self.relation.name)]) or\
               if_list_similar(tag, dicts[str(self.relation.name)][str(self.name)])):
               
                mapped_schema_element = MappedSchemaElement(self)
                mapped_schema_element.similarity = similarity_list(tag, dicts['relation'][str(self.relation.name)])
                mapped_schema_element.similarity = 1 - (1 - mapped_schema_element.similarity) * (1 -
                    similarity_list(tag, dicts[str(self.relation.name)][str(self.name)]))
    
            elif if_schema_similar(self.relation.name, tag) or if_schema_similar(self.name, tag):
                mapped_schema_element = MappedSchemaElement(self)
                mapped_schema_element.similarity = similarity_words(self.relation.name, tag)
                mapped_schema_element.similarity = 1 - (1 - mapped_schema_element.similarity) * (1 -
                    similarity_words(self.name,tag))
                
        elif str(self.relation.name) in dicts and str(self.name) in dicts[str(self.relation.name)] and\
             if_list_similar(tag, dicts[str(self.relation.name)][str(self.name)]):
            mapped_schema_element = MappedSchemaElement(self)
            mapped_schema_element.similarity = similarity_list(tag, dicts[str(self.relation.name)][str(self.name)])

        elif if_schema_similar(self.name, tag):
            mapped_schema_element = MappedSchemaElement(self)
            mapped_schema_element.similarity = similarity_words(self.name, tag) 

        #print tag, mapped_schema_element
        return mapped_schema_element 


    def is_text_exist(self, value, connection):
        sql = u'select * from size WHERE size.relation = \'{0}\''.format(self.relation.name).encode('utf-8').strip()
        #print sql
        cursor = connection.cursor()
        cursor.execute(sql)
        for (line) in cursor:
            size = line[0]
        
        sql = ''
        if size < 2000:
            sql = u'select {0} from {1}'.format(self.name, self.relation.name).encode('utf-8').strip()

        elif size >= 2000 and size < 100000:
            sql = u'select {0} from {1} where {2} like \'%{3}%\' LIMIT 0,2000'.format(self.name, self.relation.name, self.name ,value).encode('utf-8').strip()
        
        else:
            sql = u'select {0} from {1} where match({2}) against(\'{3}\') LIMIT 0,2000'.format(self.name, self.relation.name, self.name ,value).encode('utf-8').strip()
        #print sql
        mapped_schema_element = MappedSchemaElement(self)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
        except:
            sql = u'select {0} from {1} where {2} like \'%{3}%\' LIMIT 0,2000'.format(self.name, self.relation.name, self.name ,value).encode('utf-8').strip()
        for (line) in cursor:
            mapped_schema_element.mapped_values += [line[0]]


        if len(mapped_schema_element.mapped_values) != 0:
            return mapped_schema_element
        
        return None


    def is_num_exist(self,number, operator, connection):
        cursor = connection.cursor()
        sql = u'select {0} from {1} where {2} {3} {4} LIMIT 0, 10'.format(self.name, self.relation.name, self.name, operator, number).encode('utf-8').strip()
        #print sql
        cursor.execute(sql)
        mapped_schema_element = MappedSchemaElement(self)
        
        for (line) in cursor:
            mapped_schema_element.mapped_values += [str(line[0])]

        if len(mapped_schema_element.mapped_values) != 0:

            return mapped_schema_element

        return None

    # def __eq__(self,other):
    #     if other is None or type(self) != type(other):
    #         return False

    #     return other.element_id == other.element_id


    def print_for_check(self):
        print('{0}.{1};\n'.format(self.relation.name, self.name))


    def __repr__(self):
        return '{2}: {0}.{1}; '.format(self.relation.name, self.name, self.element_id)
