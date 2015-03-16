SO you'd like to help, huh?
===========================

There's a lot of stuff to be done yet, since this project is in the "will it
even work" phase. The following is an small indication of stuff that needs to
be done. Feel free to add items here, too:

- DONE (Finish porting landscape/message_schemas.py and landscape/lib/bpickle.py to
  python3. (lots of unicode vs. strings). Some tests are currently marked @skip
  and that should disappear)
- Add some tests to most test files. Right now only the happy path is tested.
- The main (landscape/main.py) doesn't quite work yet, but serves as a high-level
  view of how things should (?) work. Feel free to run it, see what's not working,
  and fix it :)
- Switch to using multiprocessing instead of threads
- Make the squite access thread-proof (don't share a connection object, AFAICT)
