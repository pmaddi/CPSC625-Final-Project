class CreateMode:
    EPHEMERAL = 1
    EPHEMERAL_SEQUENTIAL = 2
    PERSISTENT = 3
    PERSISTENT_SEQUENTIAL = 4

class WatcherStates:
    pass

class ZookeeperStates:
    pass

class KeeperException:
    APIERROR    =  1
    AUTHFAILED  =  2
    BADARGUMENTS    =  3
    BADVERSION  =  4
    CONNECTIONLOSS  =  5
    DATAINCONSISTENCY   =  6
    INVALIDACL  =  7
    INVALIDCALLBACK     =  8
    MARSHALLINGERROR    =  9
    NOAUTH  =  10
    NOCHILDRENFOREPHEMERALS     =  11
    NODEEXISTS  =  12
    NONODE  =  13
    NOTEMPTY    =  14
    OK  =  15
    OPERATIONTIMEOUT    =  16
    RUNTIMEINCONSISTENCY    =  17
    SESSIONEXPIRED  =  18
    SESSIONMOVED    =  19
    SYSTEMERROR     =  20
    UNIMPLEMENTED   =  21




'''
NodeChildrenChanged

NodeCreated

NodeDataChanged

NodeDeleted

None




ASSOCIATING

AUTH_FAILED

CLOSED

CONNECTED

CONNECTING



AuthFailed
          Auth failed state
Disconnected
          The client is in the disconnected state - it is not connected to any server in the ensemble.
Expired
          The serving cluster has expired this session.
NoSyncConnected
          Deprecated.
SyncConnected
          The client is in the connected state - it is connected to a server in the ensemble (one of the servers specified in the host connection parameter during ZooKeeper client creation).
Unknown



APIERROR
          API errors.
AUTHFAILED
          Client authentication failed
BADARGUMENTS
          Invalid arguments
BADVERSION
          Version conflict
CONNECTIONLOSS
          Connection to the server has been lost
DATAINCONSISTENCY
          A data inconsistency was found
INVALIDACL
          Invalid ACL specified
INVALIDCALLBACK
          Invalid callback specified
MARSHALLINGERROR
          Error while marshalling or unmarshalling data
NOAUTH
          Not authenticated
NOCHILDRENFOREPHEMERALS
          Ephemeral nodes may not have children
NODEEXISTS
          The node already exists
NONODE
          Node does not exist
NOTEMPTY
          The node has children
OK
          Everything is OK
OPERATIONTIMEOUT
          Operation timeout
RUNTIMEINCONSISTENCY
          A runtime inconsistency was found
SESSIONEXPIRED
          The session has been expired by the server
SESSIONMOVED
          Session moved to another server, so operation is ignored
SYSTEMERROR
          System and server-side errors.
UNIMPLEMENTED
'''
