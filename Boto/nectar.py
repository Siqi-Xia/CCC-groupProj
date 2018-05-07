#!/usr/bin/env python3.5
"""
Boto script for remote instance management
Team 52
2018
"""
import boto
from boto.ec2.regioninfo import RegionInfo

# import securities
import security_access as se_ac

# NeCTAR account details
ACCESS_KEY_ID = se_ac.GR_ACCESS_KEY_ID
SECRET_ACCESS_KEY = se_ac.GR_SECRET_ACCESS_KEY


#define region
region = RegionInfo(name='melbourne-qh2', endpoint='nova.rc.nectar.org.au')

# Establish connection to API gateway
ec2_conn = boto.connect_ec2(
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        is_secure=True,
        region=region,
        port=8773,
        path='/services/Cloud',
        validate_certs=False)

print("Nectar connected")
