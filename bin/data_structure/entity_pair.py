from data_structure.parse_tree_node import ParseTreeNode

class EntityPair(object):
    def __init__(self, right, left):
        self.right = right
        self.left = left

    def is_entity(self, node1, node2):
        if node1 == self.left.node_id and node2 == self.right.node_id:
            return True
        elif node1 == self.right.node_id and node2 == self.left.node_id:
            return True
        else:
            return False
    
    def __str__(self):
        result = ""
        result += self.left.label + "(" + str(self.left.node_id) +") and "
        result += self.right.label + "(" + str(self.right.node_id) +") are the same entity"
        return result