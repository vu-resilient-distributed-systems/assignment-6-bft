#this is the master code. That provides the semaphore capabilities.
# we will use zmq REP sockets to receive information from the client
# using a REP socket. The REP socket will count how many BFT agents are running
# When it receives 7 unique ids then it will allow everyone to start the rounds
# The round message will be sent by a publisher

'''
runs for m+1 rounds where m is the traitos
'''

import zmq
import sys
import multiprocessing as mp
import os,time
import threading, socket
import logging
import json
import utils
from BFTAgent import BFTAgent
from BFTGeneral import BFTGeneral
from BFTTraitor import BFTTraitor

'''
# this function will be used by the BFT agent to recv message from other agents. the identity of who sent the message can be checked using recv from and the port from agentudpport dictionary
def BFTAgent_recv(myid, agentSocket, logger, round):
    #do all code for receiving messages from peers
    logger.info("round BFTAgent_recv%s from agent %d"%(round,myid))

# this function will be used by the BFT agent to seends message to other agents in a round. the  port for an agent is to be read from agentudpport dictionary
def BFTAgent_send(myid, agentSocket, logger, round):
    # connect to an Anget and send it a dictionary containing the path of the message and the message content
    # then disconnect. Mak sure to connect to only one at a time.
     logger.info("round BFTAgent_send %s from agent %d"%(round,myid))
    

def BFTAgentBarrier(reqsocket,subsocket,round):
     
    readymessage={
        "id":1,
        "status":"ready",
        "round":round
    }

    #create to tell master I am ready. The same port will be used later to connect to other agents as required.

    reqsocket.send_pyobj(readymessage)
    msg=reqsocket.recv_string()
    logger.info("now waiting for published go message from parent")
 
    msg=subsocket.recv_string()
    logger.info("received message from parent")
    if msg == "go":
        logger.info ("master told to go")




def BFTAgent (id):
    logger=logging.getLogger('BFTAgent%s'%(id))
    # create console handler and set level to debug
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    #The BFT agent should setup a ZMQ  context
    context =zmq.Context(io_threads=4)
    logger.info("my pid is %s" %(os.getpid()))
    #receive messages from the master to say that lets proceed on a round
    subsocket= context.socket(zmq.SUB)
    reqsocket=context.socket(zmq.REQ)
    reqsocket.connect("tcp://localhost:%s" % (masterRepPort))
    logger.info ("connected to parent rep")
    subsocket.connect("tcp://localhost:%s" % (masterPubPort))
    #dont forget to set the subscribe option.
    logger.info("connected to parent pub")
    subsocket.setsockopt(zmq.SUBSCRIBE, b"")
    
    
    #use a udp socket to talk to my peers
    peersocket= socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    peersocket.bind(('', agentudpport[id]))
    
    #Set up a socket based on your configuration file.
    
    BFTAgentBarrier(reqsocket,subsocket, 0)
    logger.debug("BFT synchronization round 0" )    
  
    # note in round 0 all except the 1 should listen and get the message from the general. You need to fill some code.



    #Now send the round messages to other BFT agents as required for Byzantine fault tolerance. But we will do this in rounds using threading API.
    round1_recv = threading.Thread(target=BFTAgent_recv, args=(id,peersocket,logger,1,))
    round1_send = threading.Thread(target=BFTAgent_send, args=(id,peersocket,logger,1,))
    round1_send.start()
    round1_recv.start()
    round1_recv.join()
    round1_send.join()

    # process the round 1 


    #start round 2.... do more rounds as required
    round2_recv = threading.Thread(target=BFTAgent_recv, args=(id,peersocket,logger, 2,))
    round2_send = threading.Thread(target=BFTAgent_send, args=(id,peersocket,logger,2,))
    round2_send.start()
    round2_recv.start()
    round2_recv.join()
    round2_send.join()

    return
'''

if __name__== '__main__':
    #make sure no default logging is set
    logging.root.setLevel(logging.NOTSET)

    # This is the configuration section it can contain all the information.
    with open('config.json', 'r') as f:
        config = json.load(f)

    agent_numbers = config['agent_numbers']
    general_id = config['general_id']
    traitor_ids = config['traitor_ids'].keys()

    agentudpport={}
    for i in range(1,agent_numbers+1):
        agentudpport[i]=6000+i

    masterRepPort = 5551
    masterPubPort= 5552

    # configuration ends
    logger=logging.getLogger('master')
    # create console handler and set level to debug
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    context =zmq.Context(io_threads=2)
    logger.info("my pid is %s" %(os.getpid()))
    publisherSocket = context.socket(zmq.PUB)
    repSocket= context.socket(zmq.REP)
    repSocket.bind("tcp://*:%s" % (masterRepPort))
    publisherSocket.bind("tcp://*:%s" % (masterPubPort))
    
    readymsg = 0

    agents = []
    for i in range (1, agent_numbers+1):
        if i == general_id:
            general = BFTGeneral(i, masterRepPort, masterPubPort, config, agentudpport)
            agents.append(general)
        elif str(i) in traitor_ids:
            traitor = BFTTraitor(i, masterRepPort, masterPubPort, config, agentudpport)
            agents.append(traitor)
        else:
            agent = BFTAgent(i, masterRepPort, masterPubPort, config, agentudpport)
            agents.append(agent)

    for agent in agents:
        agent.start()

    utils.barrier_synchronization(agent_numbers, publisherSocket, repSocket, logger)

    for agent in agents:
        agent.join()







