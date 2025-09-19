# Tyler Millershaski
# CS 401
# Lab Assignment 1 (Message of the Day Server)
# 20 Sep 2025
# This is the server script. It listens for the 4 specific commands as outlined in the requirements.


import socket
import threading
import sys
from contextlib import closing

Port = 5555
Host = "127.0.0.1"  # Just use localhost for testing

Ok_Message = "200 OK"

motd_lock = threading.Lock()  # lock so that multiple clients can't change the motd at the same time
motd = "An apple a day keeps the doctor away."  # Message of the Day (motd)

Shutdown_Password = "123!abc"
shutdown_event = threading.Event()


# Prints the passed string to the console (requirement)
def show_client_message(message):
    print("Client: " + message)


# Converts raw bytes from the network stream and converts to string (strips \n and \r from the returned string)
def raw_byte_to_string(raw_byte):
    return raw_byte.decode('utf-8').rstrip('\n').rstrip('\r')


# Sends the passed line to the connectionStream (to the client)
def send_line(connection_stream, line: str):
    # Ensure that line ends with a newline character
    if not line.endswith("\n"):
        line = line + "\n"

    connection_stream.write(line.encode('utf-8'))
    connection_stream.flush()


# Handle the messages (commands) that the user sends us
def handle_client(conn: socket.socket, addr):
    global motd

    try:
        with conn:
            connection_stream = conn.makefile('rwb', buffering=0)

            # Wrap for text I/O (manual encode/decode via helpers for clarity)
            while not shutdown_event.is_set():
                line_bytes = connection_stream.readline()
                if not line_bytes:
                    break  # client closed
                try:
                    line = raw_byte_to_string(line_bytes)
                except UnicodeDecodeError:
                    break

                cmd = line.strip().upper()  # clean up the command (whitespace) and convert to upper
                show_client_message(cmd)  # must print all messages received from the client (requirement)

                if cmd == 'MSGGET':
                    with motd_lock:
                        current = motd
                    send_line(connection_stream, Ok_Message + "\n" + current + "\n")

                elif cmd == 'MSGSTORE':
                    # Authorize upload
                    send_line(connection_stream, Ok_Message)
                    # Then wait for the client to send us the new MOTD
                    new_line_raw = connection_stream.readline()
                    if not new_line_raw:
                        # Client didn't send message, treat this as an error and break out of listening
                        break

                    new_message = raw_byte_to_string(new_line_raw)
                    show_client_message(new_message)  # print the new message (requirement)

                    with motd_lock:
                        motd = new_message
                    send_line(connection_stream, Ok_Message)

                elif cmd == 'QUIT':
                    send_line(connection_stream, Ok_Message)
                    break  # Stop listening to this client

                elif cmd == 'SHUTDOWN':
                    send_line(connection_stream, "300 PASSWORD REQUIRED")

                    password_raw = connection_stream.readline()
                    if not password_raw:
                        # Client never sent password? Skip this command
                        continue

                    password = raw_byte_to_string(password_raw)
                    show_client_message(password)  # print the sent password (requirement)

                    if password == Shutdown_Password:
                        send_line(connection_stream, "200 OKAY")
                        shutdown_event.set()
                        break  # break out and stop listening as the server will now stop
                    else:
                        send_line(connection_stream, "301 WRONG PASSWORD")

                else:
                    # Unknown command, send back 400
                    send_line(connection_stream, "400 BAD REQUEST")

    except (ConnectionResetError, BrokenPipeError):
        pass  # Client disconnected, just ignore


# Listens on the specified port forever
def serve_forever(host, port):
    # Use a timeout on accept so we can periodically check for shutdown_event
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        s.settimeout(1.0)  # 1s accept timeout to poll shutdown_event
        print(f"YAMOTD server listening on {host}:{port}")
        print("Default message:", motd)
        try:
            while not shutdown_event.is_set():
                try:
                    conn, addr = s.accept()
                    print(f"A new client has connected via: {addr}")
                except socket.timeout:  # note that this is triggered when the server timeout is reached, and used only to handle the shutdown event
                    continue
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
        finally:
            print("Server shutting down...")


# Entry-point:
if __name__ == '__main__':
    serve_forever(Host, Port)
