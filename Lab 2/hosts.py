"""Student code for Lab1/HW1.

Author:     Wes Beard
Class:      CSI-275
Assignment: Lab 1
Due Date:   1/28/2020

Description:
    The program analyzes host files that contain IP addresses,
    hostnames, and aliases that are validated,
    added to a dictionary and then able to be referenced.

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


class InvalidEntryError(Exception):
    """Exception raised for invalid entries in the hosts file."""

    print("Error: Invalid Entry")


def is_valid_ip_address(ip_address):
    """Return whether the given ip_address is a valid IPv4 address or not.

    Args:
        ip_address (str): ip_address to test

    Returns:
        bool: True if ip_address is valid IPv4 address, False otherwise.

    """
    ip_address = str(ip_address)
    # Checks that there are 4 '.'s in IP
    if ip_address.count('.') == 3:
        # Splits IP into 3 lists
        numbers = ip_address.split('.')
        for i in numbers:
            try:
                int(i)
            except ValueError:
                return False
        # Loops through list and checks that each is a number between 0 and 255
        for i in numbers:
            if not (int(i) in range(0, 255)):
                return False
    else:
        return False

    return True


def is_valid_hostname(hostname):
    """Return whether the given hostname is valid or not.

    Host names may contain only alphanumeric characters, minus signs ("-"),
    and periods (".").  They must begin with an alphabetic character and end
    with an alphanumeric character.

    Args:
        hostname (str): hostname to test

    Returns:
        bool: True if hostname is valid, False otherwise.

    """
    # Checks if hostname begins or ends with an alphanumeric character
    if len(hostname) == 0:
        return False
    if hostname[0].isalpha() and hostname[-1].isalnum():
        for i in hostname:
            # Checks if each letter is either alphanumeric or '-' or '.'
            if i.isalnum() or (i == '-' or i == '.'):
                continue
            else:
                return False
        return True
    else:
        return False


class Hosts:
    """The Hosts class handles translating hostnames to ip addresses."""

    def __init__(self, hostfile):
        """Initialize the class.

        Reads given file and enters contents in dictionary,
        raises error if any invalid entries are found in file.

        Args:
            self
            hostfile (str): file to open

        """
        # Defines dictionary for file contents
        self.hosts_map = {}
        # Opens file and loops through contents
        with open(hostfile, 'r') as fin:
            for entry in fin:
                valid_hosts = []
                ip = ""
                word_list = entry.split()
                # If word list is empty then skip
                if len(word_list) == 0:
                    continue
                # Skip line if it begins with #
                if word_list[0] == "#":
                    continue
                # If the word is a valid IP then add it to the dictionary
                if is_valid_ip_address(word_list[0]):
                    ip = word_list[0]
                else:
                    raise InvalidEntryError
                # Raise error if no hostname exists for IP
                if len(word_list) < 2:
                    raise InvalidEntryError
                for i in word_list[1:]:
                    if is_valid_hostname(i):
                        valid_hosts.append(i)
                    elif "#" in i:
                        break
                    else:
                        raise InvalidEntryError
                self.hosts_map[ip] = valid_hosts

    def contains_entry(self, hostname):
        """Return whether or not an entry is in the dictionary."""
        for hosts in self.hosts_map.values():
            if hostname in hosts:
                return True
        return False

    def get_ip(self, hostname):
        """Return IP if it exists."""
        host_ip = None
        for ip, hosts in self.hosts_map.items():
            if hostname in hosts:
                host_ip = ip
        return host_ip
