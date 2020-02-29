"""Student code for Lab 5.

Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 5
Due Date:   2/17/2020

Description:
A program that uses TCP to receive a list to sort which is analyzed and sorted.
Sorting can be altered depending on the presence of an option.
An error is returned if the received data is in the wrong format.

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket

HOST = "localhost"
PORT = 20000


class SortServer:
    """Server to receive and sort incoming data."""

    def __init__(self, host, port):
        """Initializes class.
            Opens new TCP connection to provided host and port.

        Args:
            host(str): hostname to use
            port(int) port to use

        """

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        full_address = (host, port)
        self.connection.bind(full_address)

    def run_server(self):
        """Receive data from specified host and port.
            Decode and sort data depending on the presence of an option.
            Return either a sorted list or an error.
        """

        self.connection.listen(20)
        cli_connection, address = self.connection.accept()
        i = 1

        # Loops through all tests
        while True:
            print("\n")
            print("TEST #",i)
            # Variables reset for each new message
            sort_list = []
            sort_type = ''
            error_sent = False
            cli_data = cli_connection.recv(4096)
            decoded = cli_data.decode("utf-8")
            print(decoded)

            # Reads all characters
            while not error_sent:
                # Checks if data is preceded by LIST
                if decoded.split(" ")[0] == "LIST":
                    if len(decoded.split(" ")[1:]) <= 0:
                        print("Error: no data")
                        cli_connection.sendall("ERROR".encode("ascii"))
                        error_sent = True
                    if decoded.find("|") != -1:
                        sort_type = decoded.split("|")[1]
                        decoded = decoded.split("|")[0]
                        if not ((sort_type == 'd')
                                or (sort_type == 'a')
                                or (sort_type == 's')):
                            print("ERROR: Invalid option")
                            cli_connection.sendall("ERROR".encode("ascii"))
                            error_sent = True
                    # Reads all data after LIST
                    for entry in decoded.split(" ")[1:]:
                        # Only execute if entry has data
                        if entry != '':
                            try:
                                float(entry)
                                sort_list.append(entry)
                            except ValueError:
                                print("ERROR: Not digit")
                                cli_connection.sendall("ERROR".encode("ascii"))
                                error_sent = True
                        else:
                            break
                    break
                else:
                    print("ERROR: No list")
                    cli_connection.sendall("ERROR".encode("ascii"))
                    error_sent = True
            # Send info from the list to sort is no error has been sent
            if not error_sent:
                # Sort alphabetically
                if sort_type == 's':
                    sort_list.sort()
                # Sort descending
                elif sort_type == 'd':
                    sort_list = [float(x) if '.' in x else
                                 int(x) for x in sort_list]
                    sort_list.sort(reverse=True)
                    sort_list = [str(x) for x in sort_list]
                # Default ascending sort
                else:
                    sort_list = [float(x) if '.' in x else
                                 int(x) for x in sort_list]
                    sort_list.sort()
                    sort_list = [str(x) for x in sort_list]
                # Sends each item in sorted list
                send_string = "SORTED"
                for item in sort_list:
                    send_string += (" " + item)
                print(send_string)
                cli_connection.sendall(send_string.encode("ascii"))
            i += 1


if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()
