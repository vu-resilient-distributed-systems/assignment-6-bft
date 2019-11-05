import copy

class BFTNode():
    def __init__(self, size, id=-1, val='-1'):
        self.size = size
        self.id = id
        self.val = val
        self.children = []
        for i in range(0, size+1):
            self.children.append(None)

# Tree class that represents the message tree of each agent
# Root node is a pseudo node that has invalid values and points to first node, which is sent by the beloved General
class BFTMessage():
    def __init__(self, num_agents):
        self.size = num_agents
        self.root = BFTNode(self.size)

    # recursive method to do majority voting based on the values of children nodes
    def vote(self):
        def majority_vote(node):
            yes_num = 0
            leaf_node = True
            size = 0

            for child in node.children:
                if child != None:
                    leaf_node = False
                    yes_num += int(majority_vote(child))
                    size += 1
            
            if leaf_node:
                return node.val
            
            return '1' if yes_num >= (self.size - 2) / 2 else '0'

        # call majority_vote on the only child of root
        for child in self.root.children:
            if child != None:
                return majority_vote(child)
        
        
        # if root has no child, something is wrong
        return 'e'

    # add the current message to the tree by traversing through the message chain path
    def add_message(self, msg, round):
        val = msg['val']
        msg_chain = msg['msg_chain'].split(',')
        cur = self.root

        for cur_node in msg_chain:
            index = int(cur_node)
            if cur.children[index] == None:
                cur.children[index] = BFTNode(self.size, index, val)
                break
            cur = cur.children[index]

    # get all messages for current with the id of the agent
    # build the messages by doing BFS with backtracking from the top at the tree and stop when the message chain length is appropriate
    def get_message(self, round, id):
        def build_message(cur_chain, cur_node, cur_round):
            if cur_round == round:
                cur_chain.append(str(id))
                res.append({
                    'val': cur_node.val,
                    'msg_chain': ','.join(cur_chain)
                })
                return
            
            for child in cur_node.children:
                if child != None:
                    next_chain = copy.deepcopy(cur_chain)
                    next_chain.append(str(child.id))
                    build_message(next_chain, child, cur_round + 1)

        res = []
        build_message([], self.root, 0)
        return res


