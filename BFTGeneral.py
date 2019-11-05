from BFTAgent import BFTAgent
import pickle
import socket
import random

# General class for BFT General, subclass of BFTAgent
class BFTGeneral(BFTAgent):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport, queue):
        super(BFTGeneral, self).__init__(id, masterRepPort, masterPubPort, config, agentudpport, queue)

    # General will provide the true value back to master
    def vote_result(self):
        self.queue.put({
            "true_val": self.true_val
        })
    
    # Round 0 general should send the true value to its followers
    def process_round_0(self):
        self.send(0)

    # General doesn't care about messages from peers. It's not democracy here
    def recv(self, round):
        self.logger.info("round BFTGeneral_recv %s from agent %d"%(round, self.id))

    # General only send in round 0
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