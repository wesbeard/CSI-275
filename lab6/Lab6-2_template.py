"""Student code for Lab 6.

Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 6
Due Date:   2/24/2020

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
PORT = 45000


def recvall(sock, length):
    """Receive and return data from client"""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            print("Length Error")
            return ""
            # raise EOFError('was expecting %d bytes but only received'
                           # ' %d bytes before the socket closed'
                           # % (length, len(data)))
        data += more
    return data


class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """Initialize the class and create a TCP connection."""

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        full_address = (host, port)
        self.connection.bind(full_address)

    def calc_length(self):
        """Get length of message in the form of first four bytes,
        then call recvall function to get message from client
        and send back length of received message in appropriate format.
        """

        self.connection.listen(20)
        while True:
            cli_connection, address = self.connection.accept()

            # Read in and decode first 4 bytes to
            # use as length of incoming message
            initial_data = (cli_connection.recv(4))
            length = int.from_bytes(initial_data, 'big')
            print(length)

            # Calls recvall function and determines length of sent data
            return_data = recvall(cli_connection, length)
            returned_length = len(return_data)
            print(returned_length)

            # Creates message to send which is converted into bytes
            if returned_length < length:
                send_message = "Length Error"
            else:
                send_message = "I received {} bytes.".format(length)
            send_message = send_message.encode("ascii")
            send_length = len(send_message).to_bytes(4, 'big')
            send_message = send_length + send_message
            print(send_message)
            cli_connection.sendall(send_message)


if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()
