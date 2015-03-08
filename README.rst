What is Portrait-client?
========================

portrait-client is a vailliant attempt at writing a landscape-client from scratch
using modern python tools, mostly in order to have a python3 compatible one.

That means, specifically:

- Not using twisted (python3!)
- Using standard library features as much as possible (sched, squite3)

General idea
------------

Subject to change, but, the general idea is:

Having a scheduler (sched) coordinate several events:
- A message sender that looks into a message store (sqlite) if messages are to
  be sent, and sends them all.
- A set of reporters that "report" status by inserting messages in the message store.
- A set of managers that action on the running system.

Monitors and managers should be maintained as a set of classes.

Monitors should drop privileges as soon as possible.

They should be allowed to reschedule their own run somehow (by keeping a reference
to the scheulder for example).

They should each be called in a separate thread so as to run in parallel.
