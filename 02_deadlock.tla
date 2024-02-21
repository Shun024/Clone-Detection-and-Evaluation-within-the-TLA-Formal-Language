\* http://imnaseer.net/paxos-from-the-ground-up.html?section=3&slide=8
---- MODULE 02_deadlock ----
EXTENDS TLC, Sequences, Integers
CONSTANTS
  Acceptors,
  Proposers,
  Capacity,
  Null

VARIABLES
  acceptorValues,
  inboxes,
  acceptedMsgs,
  rejectedMsgs,
  promises

m == INSTANCE messaging

vars == <<acceptorValues, inboxes, promises, acceptedMsgs, rejectedMsgs>>

Init ==
  /\ m!Init(Acceptors)
  /\ acceptorValues = [a \in Acceptors |-> Null]
  \* When an acceptor promises to not accept other proposals, the proposal is
  \* saved here.
  /\ promises = [a \in Acceptors |-> Null]

Propose(proposer) ==
  LET sequenceNumber == 1 IN
  LET proposal == <<sequenceNumber, proposer>> IN
  LET promiseMsg == <<"promise", proposal>> IN
  LET acceptMsg == <<"accept", proposal>> IN
  \/ \E a \in Acceptors: ~m!HasMessageReceived(a, promiseMsg)
    /\ ~m!HasMessageRejected(a, promiseMsg)
    /\ acceptorValues[a] = Null
    /\ m!Send(a, promiseMsg)
    /\ UNCHANGED <<acceptorValues, promises>>
  \/ \E a \in Acceptors: m!HasMessageAccepted(a, promiseMsg)
    /\ ~m!HasMessageRejected(a, acceptMsg)
    /\ \A acp \in Acceptors: m!HasMessageAccepted(acp, promiseMsg)
    /\ m!Send(a, acceptMsg)
    /\ UNCHANGED <<acceptorValues, promises>>

AcceptMsg(acceptor, msg) ==
  acceptorValues' = [acceptorValues EXCEPT ![acceptor] = msg]

Promise(acceptor, msg) ==
  promises' = [promises EXCEPT ![acceptor] = msg]

HasAccepted(acceptor) ==
  acceptorValues[acceptor] /= Null

Accept(acceptor) ==
  \E msg \in m!Receive(acceptor):
    LET messageType == msg[1] IN
    LET proposal == msg[2] IN
    LET nothingPromised == promises[acceptor] = Null IN
    LET alreadyPromised == ~nothingPromised IN
    LET promisedThis == promises[acceptor] = proposal IN
    \/
      /\ ~HasAccepted(acceptor)
      /\ messageType = "promise"
      /\ nothingPromised
      /\ Promise(acceptor, proposal)
      /\ m!AckMsg(acceptor)
      /\ UNCHANGED <<acceptorValues>>
    \/
      /\ ~HasAccepted(acceptor)
      /\ messageType = "accept"
      /\ promisedThis
      /\ AcceptMsg(acceptor, msg)
      /\ m!AckMsg(acceptor)
      /\ UNCHANGED <<promises>>
    \/
      /\
        \/ HasAccepted(acceptor)
        \/ messageType = "promise" /\ alreadyPromised
        \/ messageType = "accept" /\ ~promisedThis
      /\ m!RejectMsg(acceptor)
      /\ UNCHANGED <<acceptorValues, promises>>

Terminating ==
  /\ \A node \in DOMAIN inboxes: Len(inboxes[node]) = 0
  /\ UNCHANGED vars

Next ==
  \/ \E p \in Proposers: Propose(p)
  \/ \E a \in Acceptors: Accept(a)
  \/ Terminating

Spec == Init /\ [][Next]_vars /\ WF_vars(Next)

Range(f) == {f[x] : x \in DOMAIN f}
AllValuesEqual == \A v1, v2 \in Range(acceptorValues): v1 = v2
EventuallyConsistent == <>[]AllValuesEqual

NoValuesNull == \A v \in Range(acceptorValues): v /= Null
ValuesGetEventuallySet == <>[]NoValuesNull
====
