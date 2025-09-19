Run Instructions:

The program is written in Python, so you'll need to run it via a Python interpreter. There are 2 scripts: client.py and server.py. The server.py can be started without any command line options. The client.py, however, requires that the server IP is passed as a command line argument (the first and only command line argument).

Note that the server listens on 127.0.0.1, so you must pass 127.0.0.1 to the client.

All available commands are displayed in the client's output console:
MSSGET
MSGSTORE
QUIT
SHUTDOWN

Quickstart:

Run server.py (no arguments)
Run client.py (127.0.0.1 as argument)

Type commands in client.py via the keyboard. Observe that the server responds appropriately.

Testing:

Case: Launch client.py without passing server host.
Expected: Client displays useful error message for user.
Observed: Client displays useful error message for user.

Case: Launch client.py with correct arguments, but without running server.
Expected: Client displays useful error message for user.
Observed: Client displays useful error message for user.

Case: Launch server then client with correct arguments
Expected: Client connects to the server and server displays incoming client message.
