'''
Build up for Nectar instances management functions
'''
import time
#Define instance details
KEY = 'id_app1'
INS_TYPE = 'm2.medium'
SEC_GROUP = ['default','ssh','http/s']
IMAGE = 'ami-c163b887' #NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 (pre-installed murano-agent)
API_REGION = 'melbourne-qh2'

#Define volume details
VOL_SIZE = 20 # in GB
VOL_ZONE = 'melbourne-qh2'
VOL_TYPE = 'melbourne'
VOL_DEVICE = '/dev/vdb'


#list current instances running
def list_current_instances(ec2_conn):
    res = ec2_conn.get_all_reservations()
    # Show instance details

    for id_, reser in enumerate(res, 1):
        print id_,':'
        list_instance_info(reser)


#List the instance info with reservation number
def list_instance_info(res):
    print "The instance has below details:"
    print "Private IP: ", res.instances[0].private_ip_address
    print "Zone: ", res.instances[0].placement
    print "ID: ", res.instances[0].id
    print "Key: ", res.instances[0].key_name
    print res

# create new instance
def create_instance(ec2_conn):
    """
    Creates an instance on the cloud
    """
    return ec2_conn.run_instances(
        IMAGE,
        key_name=KEY,
        instance_type=INS_TYPE,
        security_groups=SEC_GROUP,
        placement=API_REGION)


def terminate_instance(ec2_conn, instance_id):
    '''
    Terminate instance
    '''
    ec2_conn.terminate_instances(instance_ids=[instance_id])

# define instance mangement functions:
def update_res_info(ec2_conn, new_res):
    '''
    Get new instance info
    '''
    res = ec2_conn.get_all_reservations()
    for reser in res:
        if reser.id == new_res.id:
            return reser


def list_images(ec2_conn):
    '''
    List out all images info
    '''
    images = ec2_conn.get_all_images()
    print "The images are:"
    for img in images:
        print('id: ', img.id, 'name: ', img.name)


def list_security_groups(ec2_conn):
    '''
    List out all security groups info
    '''
    grps = ec2_conn.get_all_security_groups()
    print "The security groups are:"
    for gr in grps:
        print('id: ', gr.id, 'name: ', gr.name)


#def change_security_groups(ec2_conn):
    '''
    Change security group settings per needed
    '''

#list out the volumes
def list_volumes(ec2_conn):
    '''
    Prints info on all volumes
    '''
    volumes = ec2_conn.get_all_volumes()
    print "The volume info as:"
    for volume in volumes:
        print volume.id
        print volume.status
        print volume.zone

#Create a new volume and attach it to the existing server
def create_attach_volume(ec2_conn, new_res):
    vol_new = ec2_conn.create_volume(
        VOL_SIZE, VOL_ZONE, volume_type=VOL_TYPE)

    print "Volume created with details:"
    print "Volume: ", vol_new.id
    print "Size: ", vol_new.size, "GB"
    print "Created Zone: ", vol_new.zone

    #wait for some time while instance & vol initialize
    print "Waiting for initialisation..."
    time.sleep(60)

    # Get new instance reservation info
    res = update_res_info(ec2_conn, new_res)

    if ec2_conn.attach_volume(vol_new.id, res.instances[0].id, VOL_DEVICE):
        print "Volume attached successfully to: ", res.instances[0].private_ip_address

    f = open("result.txt",'w')
    result = res.instances[0].private_ip_address
    f.write(str(result))
    f.close()
