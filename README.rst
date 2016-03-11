What is Portrait-client?
========================

portrait-client is a valiant attempt at writing a landscape-client from scratch
using modern python tools, mostly in order to have a python3 compatible one.

That means, specifically:

- Not using twisted (python3!)
- Using standard library features as much as possible (sched, sqlite3)

General idea
------------

Having a scheduler (sched) coordinate several events:
- A message sender that looks into a message store (sqlite) if messages are to
  be sent, and sends them all (the exchanger in portrait/exchanger/exchange.py)
- A set of reporters that "report" status by inserting messages in the message store.
- Once the exchanger gets the list of server->client messages after an exchange, it delegates handling of individual messages to...
- ...A set of handlers that action on the running system

Most non-scheduler work is done *in new threads* (or processes, TBD). The only action these spawns should be allowed is interacting with the system (handling their own locks when relevant), and communicating by either adding messages to the message queue (using sqlite as the locking mechanism), or consuming message from the incoming queue (again, delegating to the database as far as locking is concerned).

Monitors and managers should (?) be maintained as a set of classes.

Monitors should drop privileges as soon as possible.
