Note that this was my first Python program (I have over 10 years experience as a programmer / developer)!


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

Functions:

In server.py, the following functions are defined:
    show_client_message(message)
    - Prints the passed string to the console (requirement)

    raw_byte_to_string(raw_byte):
    - Converts raw bytes from the network stream and converts to string (strips \n and \r from the returned string)

    send_line(connection_stream, line: str):
    - Sends the passed line to the connectionStream (to the client)

    handle_client(conn: socket.socket, addr)
    - Handle the messages (commands) that the user sends us

    serve_forever(host, port)
    - Listens on the specified port forever

In client.py, the following functions are defined:
    read_line(connection_stream) -> str:
    - Gets the next line from the server, and converts it into a string with \n and \r stripped

    send_line(connection_stream, line: str):
    - Sends the provided line to the server (to the connectionStream)

    main()
    - Called by the entry-point, this is where most of the "functionality" is defined


Testing:

Case: Launch client.py without passing server host.
Expected: Client displays useful error message for user.
Observed: Client displays useful error message for user.

Case: Launch client.py with correct arguments, but without running server.
Expected: Client displays useful error message for user.
Observed: Client displays useful error message for user.

Case: Launch server then client with correct arguments
Expected: Client connects to the server and server displays incoming client message.
Observed: Client connects to the server and server displays incoming client message.

Case: Launch server and client with correct arguments. Type invalid command to send to server.
Expected: Client displays error to user and prevents command from being sent to server. Server has no client input (no incoming messages) in its log.
Observed: Client displays error to user and prevents command from being sent to server. Server has no client input (no incoming messages) in its log.

Case: Launch server and client with correct arguments. Send MSGGET command.
Expected: Server displays incoming client message. Client displays current message of the day.
Observed: Server displays incoming client message. Client displays current message of the day.

Case: Launch server and client with correct arguments. Send MSGSTORE command, followed by new message of the day, followed by MSGGET command.
Expected: Server displays all incoming client messages. The MSGGET command returns the new message rather than the default (or former) one.
Observed: Server displays all incoming client messages. The MSGGET command returns the new message rather than the default (or former) one.


Case: Launch server and client with correct arguments. Send MSGSTORE command, followed by closing the client
Expected: Server displays all incoming client messages. The server receives a QUIT response from the client and disconnects the client.
Observed: Server displays all incoming client messages. The server receives a QUIT response from the client and disconnects the client.

Case: Launch server and client with correct arguments. Send QUIT command.
Expected: Server displays all incoming client messages. The client outputs that it has been disconnected. No further commands can be sent to the server.
Observed: Server displays all incoming client messages. The client outputs that it has been disconnected. No further commands can be sent to the server.

Case: Launch server and client with correct arguments. Send SHUTDOWN command followed by incorrect password.
Expected: Server displays all incoming client messages. The client outputs that the password was incorrect. The server remains operational.
Observed: Server displays all incoming client messages. The client outputs that the password was incorrect. The server remains operational.

Case: Launch server and client with correct arguments. Send SHUTDOWN command followed by correct password.
Expected: Server displays all incoming client messages. The server outputs that it's shutting down. The server is no longer operational.
Expected: Server displays all incoming client messages. The server outputs that it's shutting down. The server is no longer operational.


Case: Launch server and client with correct arguments. Send SHUTDOWN command followed by closing the client.
Expected: Server displays all incoming client messages. The server receives a QUIT command and disconnects the client. The shutdown process is aborted.
Observed: Server displays all incoming client messages. The server receives a QUIT command and disconnects the client. The shutdown process is aborted.