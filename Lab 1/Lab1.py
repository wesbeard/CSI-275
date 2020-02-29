
"""
Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 1
Due Date:   1/20/2020

Description:
    This program creates a list populated by data specified by the user.
    The list is then sorted and printed to the console.

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

def build_list():
    """
    Builds list of user provided values. All input validated and only appended if int.
    """

    unsorted_list = []
    while(True):
        try:
            new = input("Enter an integer to add or 'done':")
            if (new == 'done'):
                break
            new = float(new)
            unsorted_list.append(new)
        except ValueError:
            print("Please enter an integer...")
    sort_list(unsorted_list)

def sort_list(user_list):
    """
    Sorts list provided as parameter and prints the sorted list to the console.
    """
    user_list.sort()
    print("Sorted List:")
    print(user_list)


def main():
    build_list()

if __name__ == '__main__':
    main()
