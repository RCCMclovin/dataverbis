from rdbms.schema_element import SchemaElement
from data_structure.parse_tree_node import ParseTreeNode
#from data_structure.block import Block

class SQLElement(object):
    def __init__(self, block, node):
        self.block = block
        self.node = node
    
    def to_string(self, block=None, attribute=""):
        result = "" 
        #print '-- '+self.node.label
        if block == self.block and len(self.node.mapped_elements) > 0:
            element = self.node.mapped_elements[self.node.choice].schema_element 
            result += element.relation.name + "." + element.name
        elif self.block.outer_block == block:
            if attribute == "":
                result += "block_" + str(self.block.block_id) + "." + self.node.parent.function 
            else:
                result += "block_" + str(self.block.block_id) + "." + attribute 
        else:
            if attribute == "" and self.block.outer_block:
                result += "block_" + str(self.block.outer_block.block_id) + "." + self.node.parent.function
            else:
                result += "block_" + str(self.block.block_id) + "." + attribute 
    
        return result


