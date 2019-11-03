import logging
import time

def barrier_synchronization(numBFTAgents,publisherSocket,repSocket,logger):
    recvMessages={}
    for i in range(1,numBFTAgents+1):
        recvMessages[i]=0

    print (str(recvMessages))

    while 0 in recvMessages.values():
        msg=repSocket.recv_pyobj()
        repSocket.send_string("ok")
        logger.info("sent the reply to the child")
        if msg["status"]=="ready":
            logger.info ("received ready message from child %s"%msg["id"])
            recvMessages[msg["id"]]=1
        
    # now send go ahead to all.
    logger.info ("sending the message to children for round %d" %(msg["round"]))
    time.sleep(2) # lets wait a bit and then send.
    publisherSocket.send_string("go")