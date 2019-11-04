import copy

class BFTNode():
    def __init__(self, size, id=-1, val='-1'):
        self.size = size
        self.id = id
        self.val = val
        self.children = []
        for i in range(0, size+1):
            self.children.append(None)

class BFTMessage():
    def __init__(self, num_agents):
        self.size = num_agents
        self.root = BFTNode(self.size)

    def vote(self):
        def majority_vote(node):
            yes_num = 0

            for i in range(1, self.size+1):
                yes_num += node.children

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


