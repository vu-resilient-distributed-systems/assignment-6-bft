#this is the master code. That provides the semaphore capabilities.
# we will use zmq REP sockets to receive information from the client
# using a REP socket. The REP socket will count how many BFT agents are running
# When it receives 7 unique ids then it will allow everyone to start the rounds
# The round message will be sent by a publisher

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
    queue = mp.Queue()
    for i in range (1, agent_numbers+1):
        if i == general_id:
            general = BFTGeneral(i, masterRepPort, masterPubPort, config, agentudpport, queue)
            agents.append(general)
        elif str(i) in traitor_ids:
            traitor = BFTTraitor(i, masterRepPort, masterPubPort, config, agentudpport, queue)
            agents.append(traitor)
        else:
            agent = BFTAgent(i, masterRepPort, masterPubPort, config, agentudpport, queue)
            agents.append(agent)

    for agent in agents:
        agent.start()

    utils.barrier_synchronization(agent_numbers, publisherSocket, repSocket, logger)

    for agent in agents:
        agent.join()

    # Process the values received by the agents to verify consensus was achieved
    yes_num = 0
    final_val = -1
    true_val = -1
    while not queue.empty():
        obj = queue.get()
        if type(obj) is str:
            yes_num += int(obj)
        else:
            true_val = int(obj['true_val'])
            yes_num += true_val

    final_val = 1 if yes_num >= agent_numbers / 2 else 0
    majority = max(yes_num, agent_numbers - yes_num)

    logger.info("True value sent by general is: %d" %(true_val))
    logger.info("Value agreed by lieutenants is: %d" %(final_val))
    
    if (final_val == true_val):
        logger.info("Consensus achieved")
        logger.info("Number of 'correct' agents: %d, out of %d agents" %(majority, agent_numbers))
    else:
        logger.info("Consensus was not achieved")
        logger.info("Number of 'incorrect' agents: %d, out of %d agents" %(majority, agent_numbers))
