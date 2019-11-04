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

    def add_message(self, msg, round, id):
        val = msg['val']
        msg_chain = msg['msg_chain'].split(',')
        cur = self.root

        for cur_node in msg_chain:
            index = int(cur_node)
            if cur.children[index] == None:
                cur.children[index] = BFTNode(self.size)
            cur = cur.children[index]

        cur = BFTNode(self.size, id=id, val=val)

    def get_message(self, round):
        res = []
        self.build_message(res, [], self.root, 0, round)
        return res

    def build_message(self, res, cur_chain, cur_node, cur_round, round):
        if cur_round == round:
            res.append({
                'val': cur_node.val,
                'msg_chain': ','.join(cur_chain)
            })
            return
        
        for child in cur_node.children:
            if child != None:
                if round == 1 and child.id == 1:
                    print('dsaoubfoubd')
                next_chain = copy.deepcopy(cur_chain)
                next_chain.append(str(child.id))
                self.build_message(res, next_chain, child, cur_round + 1, round)


