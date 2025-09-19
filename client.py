# Tyler Millershaski
# CS 401
# Lab Assignment 1 (Message of the Day Server)
# 20 Sep 2025
# This is the client script. It connects to the server and can send any command that the user inputs (via keyboard)


import socket
import sys

Server_Port = 5555
Valid_Commands = "MSGGET | MSGSTORE | QUIT | SHUTDOWN" # Note that this is printed for the user rather than used in any control structure


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
    if len(sys.argv) < 2:
        print("Server address must be passed as a command line parameter")
        sys.exit(1)

    host = sys.argv[1]

    with socket.create_connection((host, Server_Port)) as sock:
        connection_stream = sock.makefile('rwb', buffering=0)
        print(f"Connected to {host}:{Server_Port}")
        print("Enter one of: " + Valid_Commands)

        while True:
            try:
                cmd = input("yamotd> ").strip()
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
                if not code:
                    print("[Server closed]")
                    break
                print(code)
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
                print(code)

                # Server has authorized MSGSTORE, so now get and send the new MOTD
                if code.upper().startswith('200'):
                    new_message = input("Enter new message of the day: ")
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
                    print(code)
                break

            elif upper == 'SHUTDOWN':
                send_line(connection_stream, 'SHUTDOWN')
                code = read_line(connection_stream)
                if not code:
                    print("[Server closed]")
                    break
                print(code)

                if code.upper().startswith('300'):
                    password = input("Password: ")
                    send_line(connection_stream, password)
                    code = read_line(connection_stream)
                    if code:
                        print(code)

                        # If 200, then server will be closing, so we (the client) can also stop listening
                        if code.upper().startswith('200'):
                            break
                else:
                    # Server rejected the command unexpectedly
                    pass

            else:
                print("Unknown command. Use: " + Valid_Commands)

    print("Disconnected.")


# Entry-point
if __name__ == '__main__':
    main()
