import pickle
import socket
import random
from BFTAgent import BFTAgent

# Traitor class for BFT Traitor, subclass of BFTAgent
class BFTTraitor(BFTAgent):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport, queue):
        super(BFTTraitor, self).__init__(id, masterRepPort, masterPubPort, config, agentudpport, queue)

    # Traitor also lie in voting
    def vote_result(self):
        self.queue.put(str(random.choice([0,1])))

    # Traitor can lie in sending the values
    def send(self, round):
        self.logger.info("%s %d: round %s sending"%(type(self).__name__, self.id, round))
        send_list = self.msg_tree.get_message(round, self.id)
        for peer_id in self.agentudpport:
            if peer_id != self.id:
                self.logger.debug("%s %d: round %d sending to %d with %d messages" %(type(self).__name__, self.id, round, peer_id, len(send_list)))
                for i in range(0, len(send_list)):
                    msg = send_list[i]
                    msg['val'] = str(random.choice([0,1]))
                    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_socket.connect(("127.0.0.1", self.agentudpport[peer_id]))
                    send_socket.send(pickle.dumps(msg))
                    send_socket.close()

                    self.logger.debug("%s %d: round %s send to %d number %d out of %d msg %s"%(type(self).__name__, self.id, round, peer_id, i, len(send_list), msg))