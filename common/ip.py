#import libraries
import re
import argparse

# error messages
INVALID_IP_MSG = "Error: Invalid IP address.\n%s is not a correct IP address."
REPEATED_SERVER_MSG = "Error: %s is already a File Server."
FILE_NOT_FOUND_MSG = "Error: Configuration file does not exist. Run ssoftp --setup"
SERVER_NOT_FOUND_MSG = "Error: File Server does not exist"

#path of configuration file
PATH_CONF = "config.json"

def validate_ip(ip):
    '''
    validate ip address
    '''
    if not valid_ip(ip):
        print(INVALID_IP_MSG%(ip))
        quit()
    return
    
def valid_ip(ip):
    # validate ip address
    regex =  "(((1[0-9]|[1-9]?)[0-9]|2([0-4][0-9]|5[0-5]))\.){3}((1[0-9]|[1-9]?)[0-9]|2([0-4][0-9]|5[0-5]))"
    return re.search(regex, ip)
