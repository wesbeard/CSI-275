"""
Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 3-2
Due Date:   2/3/2020

Description:
    This program creates a list populated by data specified by the user,
    which is then sent to a server to be sorted and return to be printed.

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

def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if user_input != "done":
                    print("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Open socket to server IP, convert unsorted list to string and sort through server."""

    # Initializes connection to server IP and port
    connection = socket.socket()
    connection.connect(('192.168.3.122', 7778))
    # Creates string to fill with list data
    string_list = "LIST "

    # Loops through unsorted list and adds contents to a string
    for item in unsorted_list:
        string_list += str(item) + ' '

    # Sends and receives string from server after encoding and decoding from ascii
    request = string_list.encode('ascii')
    connection.sendall(request)
    received = connection.recv(4096)
    print(received.decode('ascii'))


def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    sort_list(number_list)

if __name__ == "__main__":
    main()
