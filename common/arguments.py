#import libraries
import re
import os
import argparse
import csv

# error messages
INVALID_IP_MSG = "Error: Invalid IP address.\n%s is not a correct IP address."
REPEATED_SERVER_MSG = "Error: %s is already a File Server."
FILE_NOT_FOUND_MSG = "Error: Configuration file does not exist. Run ssoftp --setup"
SERVER_NOT_FOUND_MSG = "Error: File Server does not exist"

#path of configuration file
PATH_CONF = "config.json"


def get_arguments():
    # create parser object
    parser = argparse.ArgumentParser(description = "Manage the SOFTP Core Server")

    # defining arguments for parser object
    parser.add_argument("-i", "--init", action = 'store_true',
                        help = "Initialize the SOFTP server.")
    parser.add_argument("-p", "--port", action = 'store',
                        help = "Starts server with the selected port.")
    parser.add_argument("-st", "--setup", action = 'store_true',
                        help = "Initialize the setup of the SOFTP file server.")
    parser.add_argument("-add", "--add", type = str, nargs = 1,
                        metavar = ('bind_address:port'), default = None,
                        help = "add IPv4 and port to the SOFTP file server.")
    parser.add_argument("-rm", "--remove", type = str, nargs = 1,
                        metavar = ('bind_address'), default = None,
                        help = "Remove IPv4 and port from the SOFTP file server.")    

    # parse the arguments from standard input
    args = parser.parse_args()
    return args