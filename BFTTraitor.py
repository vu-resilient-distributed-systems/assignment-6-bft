import pickle
import socket
import random
from BFTAgent import BFTAgent

class BFTTraitor(BFTAgent):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport):
        super(BFTTraitor, self).__init__(id, masterRepPort, masterPubPort, config, agentudpport)

    def send(self, round):
        send_list = self.msg_tree.get_message(round, self.id)
        for peer_id in self.agentudpport:
            if peer_id != self.id:
                self.logger.info("%s %d: round %d sending to %d with %d messages" %(type(self).__name__, self.id, round, peer_id, len(send_list)))
                for msg in send_list:
                    msg['val'] = str(random.choice([0,1]))
                    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_socket.connect(("127.0.0.1", self.agentudpport[peer_id]))
                    send_socket.send(pickle.dumps(msg))
                    send_socket.close()

                    self.logger.info("%s %d: round %s send to %d msg %s"%(type(self).__name__, self.id, round, peer_id, msg))