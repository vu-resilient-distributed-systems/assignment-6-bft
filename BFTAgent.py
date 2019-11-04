import logging
import sys
import zmq
import os,time
import socket
import threading
import multiprocessing
import pickle
from BFTMessage import BFTMessage


class BFTAgent(multiprocessing.Process):
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport):
        super(BFTAgent, self).__init__()
        self.id = id
        self.masterRepPort = masterRepPort
        self.masterPubPort = masterPubPort
        self.config = config
        self.agentudpport = agentudpport
        self.msg_chain = ""
        self.last_val = ''
        self.msg_tree = BFTMessage(config['agent_numbers'])

    def run(self):
        # note in round 0 all except the 1 should listen and get the message from the general. You need to fill some code.

        self.logger=logging.getLogger('BFTAgent%s'%(id))
        # create console handler and set level to debug
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s - %(message)s')
        formatter = logging.Formatter('%(name)s:%(process)d:%(thread)d:%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        #The BFT agent should setup a ZMQ  context
        context = zmq.Context(io_threads=4)
        self.logger.info("my pid is %s" %(os.getpid()))
        #receive messages from the master to say that lets proceed on a round
        self.subsocket= context.socket(zmq.SUB)
        self.reqsocket=context.socket(zmq.REQ)
        self.reqsocket.connect("tcp://localhost:%s" % (self.masterRepPort))
        self.logger.info ("connected to parent rep")
        self.subsocket.connect("tcp://localhost:%s" % (self.masterPubPort))
        #dont forget to set the subscribe option.
        self.logger.info("connected to parent pub")
        self.subsocket.setsockopt(zmq.SUBSCRIBE, b"")
        
        
        #use a udp socket to talk to my peers
        self.rounds = int(self.config['rounds'])
        self.peersocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.peersocket.bind(('', self.agentudpport[self.id]))
        
        #Set up a socket based on your configuration file.
        
        self.barrier(0)
        self.logger.debug("BFT synchronization round 0")

        self.process_round_0()

        for i in range(1, self.rounds):
            roundi_recv = threading.Thread(target=self.recv, args=(i,))
            roundi_send = threading.Thread(target=self.send, args=(i,))
            roundi_send.start()
            roundi_recv.start()
            roundi_recv.join()
            roundi_send.join()
            self.logger.info("%s %d finished round %d" %(type(self).__name__, self.id, i))

    def process_round_0(self):
        self.recv(0)
        
    def barrier(self, round):
        readymessage={
            "id": self.id,
            "status":"ready",
            "round": round

        }

        #create to tell master I am ready. The same port will be used later to connect to other agents as required.

        self.logger.info("%s trying to sync before round %d" %(type(self).__name__, round))
        self.reqsocket.send_pyobj(readymessage)
        msg = self.reqsocket.recv_string()
        self.logger.info("now waiting for published go message from parent on round %d" %(round))
    
        msg = self.subsocket.recv_string()
        self.logger.info("received message from parent on round %d" %(round))
        if msg == "go":
            self.logger.info ("master told to go on round %d" %(round))

    def recv(self, round):
        round_len = 1
        for i in range(0, round):
            round_len = round_len * (len(self.agentudpport) - 2)
        msg_chain = ''

        self.logger.info("%s %d expecting %d messages for round %d" %(type(self).__name__, self.id, round_len, round))
        for i in range(0, round_len):
            msg = self.peersocket.recv(4096)
            msg = pickle.loads(msg)
            msg_src = msg['msg_chain'][-1]

            self.msg_tree.add_message(msg, round)

            self.last_val = msg['val']
            self.logger.info("%s %d: round %s recv msg from %s, msg is: %s"%(type(self).__name__, self.id, round, msg_src, msg))

    def send(self, round):
        send_list = self.msg_tree.get_message(round, self.id)
        for peer_id in self.agentudpport:
            if peer_id != self.id:
                self.logger.info("%s %d: round %d sending to %d with %d messages" %(type(self).__name__, self.id, round, peer_id, len(send_list)))
                for msg in send_list:
                    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    send_socket.connect(("127.0.0.1", self.agentudpport[peer_id]))
                    send_socket.send(pickle.dumps(msg))
                    send_socket.close()

                    self.logger.info("%s %d: round %s send to %d msg %s"%(type(self).__name__, self.id, round, peer_id, msg))
            
        
