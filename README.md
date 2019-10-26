# assignment-6

**Assignment 5**

**Byzantine Fault Tolerance**

******************

**Due: 1 week Tuesday 5 November**


**Description**: 

In this assignment you will implement the BFT algorithm (class slides) (python) using ZMQ (TCP client/Server -http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/client_server.html ) directly exchanged between the peers. All peers will have to know each other's addresses. You can provide that using a configuration file that is read before the system starts. Note if you are not comfortale in python you can use any other language of your choice. Every node will connect to every node in order to be able to send messages.

Assume that the node number 1 is general.  Assume that node 2 and node 3 are traitors. All nodes will need to achieve consensus. Refer to the [class slides](https://github.com/vu-resilient-distributed-systems/lectures-fall-2019/tree/master/Module-5-AvoidingFailures) and create the required tree data structure to store the message from all rounds.

Note that this is a one machine assignment. You will launch 7 processes. Each process should read in the configuration file which gives it the id and address of other participants. The process will also need to know its own id, which also will be passed as a command line paramter.

Note that in each message pass the identity of the sender along with the round number. The message should contain other information that will let the receiver know the full path of the message. For example the message should say that node 2 tells that node 4 says that node 3 received Attack from general. Refer to class slides.

Note that use of TCP and ZMQ will allow you to start the nodes/processes in any order.

**Submission**:

- Submit your code and a readme explaining how to run your submissions.

**Bonus (50 points)**

Make your code parameterizable. That is you can have N processes. Anyone can be the general and anyone can be traitor. The number of nodes will depend upon the number of entries in the configuration file.

**Useful References**

- [Class Material](https://github.com/vu-resilient-distributed-systems/lectures-fall-2019/tree/master/Module-5-AvoidingFailures)

- https://medium.com/coinmonks/a-note-from-anthony-if-you-havent-already-please-read-the-article-gaining-clarity-on-key-787989107969
