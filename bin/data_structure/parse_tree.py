from data_structure.parse_tree_node import ParseTreeNode
import sys
class ParseTree (object):
    def __init__(self):
        self.root = ParseTreeNode(0,"ROOT","ROOT","ROOT", None)
        self.root.token_type = "ROOT"
        self.all_nodes = [self.root]
        self.deleted_nodes = []

    def build_node(self, entry):
        if len(self.root.children) == 0:
            node = ParseTreeNode(int(entry[0]), entry[1],entry[2], entry[5], self.root)
            self.root.children.append(node)
            self.all_nodes.append(node)
            return True
        else:
            l = [self.root]
            while len(l) != 0:
                parent = l.pop(0)

                if parent.word_order == int(entry[3]):
                    node = ParseTreeNode(int(entry[0]), entry[1],entry[2],entry[5], parent)
                    parent.children.append(node)
                    self.all_nodes.append(node)
                    return True

                for child in parent.children:
                    l += [child]    
        return False


    def search_node_by_order(self, order):    
        for node in self.all_nodes:
            if node.word_order == order:
                return node            
        return None

    def search_node_by_id(self, id):
        for node in self.all_nodes:
            if node.node_id == id:
                return node
        return None

    def delete_node(self, node):
        parent = node.parent
        node.parent = None
        position = 0
        try:
            position = parent.children.index(node)
        except ValueError:
            position = -1
        #print ('parent: ' + parent.label)
        #print position
        if position == -1:
            return

        parent.children.remove(node)
        if node.left_rel != '' and len(node.children) > 0:
            node.children[0].left_rel = node.left_rel
        
        #print([x.label for x in parent.children])
        for i in range(len(node.children)):
            #print ''
            node.children[i].parent = parent
            parent.children.insert(position+i, node.children[i])
        
        self.all_nodes.remove(node)
        
        if node.token_type != "QT":
            self.deleted_nodes.append(node)
        #print self
        #sys.exit()

    def __repr__(self):
        result = ''
        node_list = [self.root]
        level_list = [0]
        while len(node_list) != 0:
            cur_node = node_list.pop(len(node_list) - 1)
            cur_level = level_list.pop(len(level_list) - 1)
            #for i in range(0, cur_level):
            result += cur_level*"    "
            result += '(' + str(cur_node.node_id) + ')'

            result += cur_node.label + '\n'
            # result += cur_node.label + ' t: ' +cur_node.token_type + ' c:'+ str(cur_node.choice)+\
            #  ' m:' + ' '.join([ str(x.schema_element.relation.name) + \
            #     '.' + str(x.schema_element.name) + \
            #     ': ' + str(x.similarity)
            #     for x in cur_node.mapped_elements])  + '\n'
             # [str(x.mapped_elements[x.choice]) for x in cur_node.mapped_elements]
            tam = len(cur_node.children)
            for i in range(tam):
                nxt = cur_node.children[tam -i - 1]
                #if nxt not in node_list:
                node_list.append(nxt)
                level_list.append(cur_level + 1)
        return result
