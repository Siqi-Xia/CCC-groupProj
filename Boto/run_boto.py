#!/usr/bin/env python3.5

'''
Boto execution main function
'''

import time
from nectar import ec2_conn
import build as build

def main():
    """
    Main func
    """

    print "Action started!!!"
    print '---------------------------------------------------------'

    #print all instances info
    build.list_current_instances(ec2_conn)
    print '---------------------------------------------------------'

    #print all images info
    build.list_images(ec2_conn)
    print '---------------------------------------------------------'


    #list all security groups
    build.list_security_groups(ec2_conn)
    print '---------------------------------------------------------'

    # Create a new instance;
    new_res = build.create_instance(ec2_conn)
    print "Instance launched."
    build.list_instance_info(new_res)
    print '---------------------------------------------------------'

    #print all volumn info
    build.list_volumes(ec2_conn)
    print '---------------------------------------------------------'

    #create and attach volume to new instance
    build.create_attach_volume(ec2_conn, new_res)
    print '---------------------------------------------------------'
    print "All action finished!!!"




if __name__ == '__main__':
    main()