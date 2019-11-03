import logging
import sys
import zmq
import os,time
import socket
import threading


class BFTAgent():
    def __init__(self, id, masterRepPort, masterPubPort, config, agentudpport):
        self.logger=logging.getLogger('BFTAgent%s'%(id))
        # create console handler and set level to debug
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        #The BFT agent should setup a ZMQ  context
        context = zmq.Context(io_threads=4)
        self.logger.info("my pid is %s" %(os.getpid()))
        #receive messages from the master to say that lets proceed on a round
        self.subsocket= context.socket(zmq.SUB)
        self.reqsocket=context.socket(zmq.REQ)
        self.reqsocket.connect("tcp://localhost:%s" % (masterRepPort))
        self.logger.info ("connected to parent rep")
        self.subsocket.connect("tcp://localhost:%s" % (masterPubPort))
        #dont forget to set the subscribe option.
        self.logger.info("connected to parent pub")
        self.subsocket.setsockopt(zmq.SUBSCRIBE, b"")
        
        
        #use a udp socket to talk to my peers
        self.rounds = config['rounds']
        self.peersocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.peersocket.bind(('', agentudpport[id]))
        
        #Set up a socket based on your configuration file.
        
        self.barrier(0)
        self.logger.debug("BFT synchronization round 0" )    
    
        # note in round 0 all except the 1 should listen and get the message from the general. You need to fill some code.

        for i in range(1, self.rounds):
            roundi_recv = threading.Thread(target=self.recv, args=(id,i,))
            roundi_send = threading.Thread(target=self.send, args=(id,i,))
            roundi_send.start()
            roundi_recv.start()
            roundi_recv.join()
            roundi_send.join()

        return

    def barrier(self, id):

        readymessage={
            "id":1,
            "status":"ready",
            "round":round
        }

        #create to tell master I am ready. The same port will be used later to connect to other agents as required.

        self.reqsocket.send_pyobj(readymessage)
        msg = self.reqsocket.recv_string()
        self.logger.info("now waiting for published go message from parent")
    
        msg = self.subsocket.recv_string()
        self.logger.info("received message from parent")
        if msg == "go":
            self.logger.info ("master told to go")

    def recv(self, id, round):
        self.logger.info("round BFTAgent_recv %s from agent %d"%(round, id))

    def send(self, id, round):
        self.logger.info("round BFTAgent_send %s from agent %d"%(round, id))
