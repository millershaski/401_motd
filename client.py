# Tyler Millershaski
# CS 401
# Lab Assignment 1 (Message of the Day Server)
# 20 Sep 2025
# This is the client script. It connects to the server and can send any command that the user inputs (via keyboard)


import socket
import sys

SERVER_PORT = 5555
VALID_COMMANDS = "MSGGET | MSGSTORE | QUIT | SHUTDOWN" # Note that this is printed for the user rather than used in any control structure


# Gets the next line from the server, and converts it into a string with \n and \r stripped
def read_line(connection_stream) -> str:
    data = connection_stream.readline()
    if not data:
        return ''

    return data.decode('utf-8').rstrip('\n').rstrip('\r')


# Sends the provided line to the server (to the connectionStream)
def send_line(connection_stream, line: str):
    if not line.endswith("\n"):
        line = line + "\n"

    connection_stream.write(line.encode('utf-8'))
    connection_stream.flush()


# Called by the entry-point, this is where most of the "functionality" is defined
def main():
    if len(sys.argv) < 2: # missing command line parameter
        print("Server address must be passed as a command line parameter")
        sys.exit(1)

    host = sys.argv[1]

    try:
        with socket.create_connection((host, SERVER_PORT)) as sock: # attempt to connect to server
            connection_stream = sock.makefile('rwb', buffering=0)
            print(f"Connected to {host}:{SERVER_PORT}")
            print("Enter one of: " + VALID_COMMANDS)

            while True:
                try:
                    cmd = input("Enter Command: ").strip()
                except (EOFError, KeyboardInterrupt):  # This will automatically send the QUIT command to the server in the event that client is aborted or has error.
                    cmd = "QUIT"
                    print()

                if not cmd:
                    continue  # null command, try again

                upper = cmd.upper()

                if upper == 'MSGGET':
                    send_line(connection_stream, 'MSGGET')
                    # Should receive "200 OK\nMOTD"
                    code = read_line(connection_stream)
                    if not code: # null response, server must have closed
                        print("[Server closed]")
                        break
                    print(f"Server: {code}")
                    motd = read_line(connection_stream)
                    if motd:
                        print(motd)

                elif upper == 'MSGSTORE':
                    send_line(connection_stream, 'MSGSTORE')
                    # Should receive "200OK"
                    code = read_line(connection_stream)
                    if not code:
                        print("[Server closed]")
                        break
                    print(f"Server: {code}")

                    # Server has authorized MSGSTORE, so now get and send the new MOTD
                    if code.upper().startswith('200'):
                        try:
                            new_message = input("Enter new message of the day: ")
                        except (EOFError, KeyboardInterrupt):  # This will automatically send the QUIT command to the server in the event that client is aborted or has error.
                            send_line(connection_stream, 'QUIT')
                            break # stop listening, as we told the server that we quit

                        send_line(connection_stream, new_message)

                        # If MOTD was correctly saved, we should receive a 200
                        code = read_line(connection_stream)
                        print(code)
                    else:
                        print("Upload not authorized by server.")

                elif upper == 'QUIT':
                    send_line(connection_stream, 'QUIT')
                    code = read_line(connection_stream)
                    if code:
                        print(f"Server: {code}")
                    break

                elif upper == 'SHUTDOWN':
                    send_line(connection_stream, 'SHUTDOWN')
                    code = read_line(connection_stream)
                    if not code:
                        print("[Server closed]")
                        break
                    print(f"Server: {code}")

                    # Server response of 300 means that it's now waiting for the password
                    if code.upper().startswith('300'):
                        try:
                            password = input("Password: ")
                        except (EOFError, KeyboardInterrupt):  # This will automatically send the QUIT command to the server in the event that client is aborted or has error.
                            send_line(connection_stream, 'QUIT')
                            break # stop listening, we told server that we quit

                        send_line(connection_stream, password)
                        code = read_line(connection_stream)
                        if code:
                            print(f"Server: {code}")

                            # If 200, then server will be closing, so we (the client) can also stop listening
                            if code.upper().startswith('200'):
                                break
                    else:
                        # Server rejected the command unexpectedly
                        pass

                else:
                    print("Unknown command. Use: " + VALID_COMMANDS)

        print("Disconnected.")
    except ConnectionRefusedError as e:
        print(f"Connection refused, is the server running?: {e}")


# Entry-point
if __name__ == '__main__':
    main()
