from BFTAgent import BFTAgent

class BFTTraitor(BFTAgent):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport):
        super(BFTTraitor, self).__init__(id, masterRepPort, masterPubPort, config, agentudpport)

    # def send(self, round):
    #     self.logger.info("round BFTTraitor_send %s from agent %d"%(round, self.id))