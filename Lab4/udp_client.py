"""Student code for Lab4.

Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 4
Due Date:   2/10/2020

Description:
A program that creates a UDP socket connection from host and port info,
then sends an ascii encoded message through the connection.
A response is then received and decoded.

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
import constants
import random


class TimeOutError(Exception):
    """Throws a timeout error when raised."""

    pass


class UDPClient:
    """Makes a UDP connection with given information."""

    def __init__(self, host, port, id_status=False):
        """Initialize class.

        Args:
            host(str): hostname to test
            port(int): port to test
            id_status(bool): if message should have an ID

        """
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.destination = (host, port)
        self.request_id_status = id_status

    def send_message_by_character(self, message):
        """Open UDP connection to send specified data and receive from destination.

        Args:
            message(str): message to be sent

        """
        wait_time = constants.INITIAL_TIMEOUT
        returned = ""
        # Loop through all characters in message parameter
        for character in message:
            # Generate a random integer to use as a request ID
            rand_id = random.randint(0, constants.MAX_ID)
            self.connection.settimeout(wait_time)
            # Reset the char to equal the current character
            app_char = character
            # Loop until success or timeout is reached
            while True:
                try:
                    # If there is a request ID then
                    # append the random ID to the character
                    if self.request_id_status:
                        app_char = (str(rand_id) + "|" + character)
                    # Encode current message into ascii
                    self.connection.sendto(app_char.encode("ascii"),
                                           self.destination)
                    # Receive from server
                    received, address = self.connection.recvfrom(4096)
                    # Check if request ID should exist
                    # and if it matches the one sent
                    if self.request_id_status:
                        if int((received.decode("utf-8")).split(
                                "|")[0]) == rand_id:
                            returned += (received.decode("utf-8")).split(
                                "|")[1]
                            print(returned)
                            wait_time = constants.INITIAL_TIMEOUT
                            break
                        else:
                            continue
                    else:
                        returned += received.decode("utf-8")
                        print(returned)
                        wait_time = constants.INITIAL_TIMEOUT
                        break
                # If timeout then increase wait time or raise exception
                # if the wait time is greater than the max timeout
                except socket.timeout:
                    wait_time *= 2
                    self.connection.settimeout(wait_time)
                    if wait_time >= constants.MAX_TIMEOUT:
                        raise TimeOutError
        return returned


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
