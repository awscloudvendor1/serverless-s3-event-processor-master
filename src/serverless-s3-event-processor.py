
# -*- coding: utf-8 -*-
"""
.. module: Serverless S3 Event Processor
    :platform: AWS
    :copyright: (c) 2019 Mystique.,
    :license: Apache, see LICENSE for more details.
.. moduleauthor:: Mystique
.. contactauthor:: miztiik@github issues
"""

import boto3
import logging

# Initialize Logger
logger = logging.getLogger()
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

def set_global_vars():
    global_vars = {'status': False}
    try:
        global_vars['Owner']                    = "Mystique"
        global_vars['Environment']              = "Prod"
        global_vars['region_name']              = "us-east-1"
        global_vars['tag_name']                 = "serverless-s3-event-processor"
        global_vars['status']                   = True
    except Exception as e:
        logger.error("Unable to set Global Environment variables. Exiting")
        global_vars['error_message']            = str(e)
    return global_vars


def lambda_handler(event, context):
    resp = {'status': False, 'TotalItems': {} , 'Items': [] }
    
    # global_vars = set_global_vars()

    if 'Records' not in event:
        resp = {'status': False, "error_message" : 'No Records found in Event' }
        return resp

    for r in event.get('Records'):
        # Lets skip the records that are Put/Object Create events
        if not ( ( r.get('eventName') == "ObjectCreated:Put" )  and ( 's3' in r ) ) : continue
        d = {}
        d['time']           = r['eventTime']
        d['object_owner']   = r['userIdentity']['principalId']
        d['bucket_name']    = r['s3']['bucket']['name']
        d['key']            = r['s3']['object']['key']
        resp['Items'].append(d)

    if resp.get('Items'):
        resp['status'] = True
        resp['TotalItems'] = { 'Received': len( event.get('Records') ) , 'Processed': len( resp.get('Items') ) }
    
    logger.info(f"resp:{resp}")

    return resp


if __name__ == '__main__':
    lambda_handler(None, None)
