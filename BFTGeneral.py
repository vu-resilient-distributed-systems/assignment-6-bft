from BFTAgent import BFTAgent
import pickle
import socket
import random

class BFTGeneral(BFTAgent):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport):
        super(BFTGeneral, self).__init__(id, masterRepPort, masterPubPort, config, agentudpport)
    
    def process_round_0(self):
        self.send(0)

    def recv(self, round):
        self.logger.info("round BFTGeneral_recv %s from agent %d"%(round, self.id))

    def send(self, round):
        if (round == 0):
            self.true_val = str(random.choice([0,1]))
            msg = {
                'val': self.true_val,
                'msg_chain': str(self.id)
            }

            for peer_id in self.agentudpport:
                if peer_id != self.id:
                    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_socket.connect(("127.0.0.1", self.agentudpport[peer_id]))
                    send_socket.send(pickle.dumps(msg))
                    send_socket.close()

            self.logger.info("round %d BFTGeneral_send val %s"%(round, self.true_val))