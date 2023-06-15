import json
from datetime import datetime, timedelta
from flask import Flask, request, render_template, redirect, url_for, make_response, jsonify
import boto3
from botocore.exceptions import ClientError
from comp_config import *

app = Flask(__name__)
KEY = "AWS_KEY"
SECRET = "AWS_SECRET"

s3 = boto3.client('s3', region_name='eu-central-1', aws_access_key_id=KEY, aws_secret_access_key=SECRET)
iot = boto3.client('iot', region_name='eu-central-1', aws_access_key_id=KEY, aws_secret_access_key=SECRET)
sts = boto3.client('sts', aws_access_key_id=KEY, aws_secret_access_key=SECRET)


# Creates the policy being used for temporary credentials
def get_role(serials):
    role_temp = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iot:Receive",
                    "iot:Subscribe",
                    "iot:Connect",
                    "iot:Publish"
                ],
                "Resource": [
                ]
            }
        ]
    }
    for serial in set(serials):
        role_temp['Statement'][0]['Resource'].extend([f"arn:aws:iot:eu-central-1:ACCOUNT_ID:client/{serial}*",
                                                      f"arn:aws:iot:eu-central-1:ACCOUNT_ID:topic/device/{serial}/*",
                                                      f"arn:aws:iot:eu-central-1:ACCOUNT_ID:topicfilter/device/{serial}/*",
                                                      f"arn:aws:iot:eu-central-1:ACCOUNT_ID:topic/device/{serial}/*",
                                                      f"arn:aws:iot:eu-central-1:ACCOUNT_ID:topic/$aws/things/{serial}*/shadow/update/delta",
                                                      f"arn:aws:iot:eu-central-1:ACCOUNT_ID:topicfilter/$aws/things/{serial}*/shadow/update/delta"])
    return role_temp


# Gets the all devices registered as output by searching with type attribute
def get_output_devices(serial):
    devices = []
    query = f'thingGroupNames:{serial} AND attributes.type:output'
    response = iot.search_index(
        queryString=query,
        indexName='AWS_Things'
    )
    if 'things' in response:
        for thing in response['things']:
            devices.append({thing['thingName'].split('_')[1]: thing['attributes']['model']})
    return devices


# Returns all components connected with the selected device
@app.route('/device/<serial>')
def device(serial):
    try:
        comp_dict = {}
        output_devices = []
        components = iot.list_things_in_thing_group(thingGroupName=serial)
        if components and 'things' in components:
            components = components['things']
            components.remove(serial)
            output_devices = get_output_devices(serial)
            for component in components:
                comp_dict[component] = component.split('_')[1]
            list_of_output = [key for d in output_devices for key in d.keys()]
            return render_template("device.html", components=comp_dict, serial=serial, output=output_devices,
                                   list_of_output=list_of_output)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        text = f"Client Error: {error_code} - {error_message}"
        return redirect(url_for("home"))
    return redirect(url_for("home"))


# Handle adding component to a device
@app.route('/addcomponent', methods=['POST'])
def add_component():
    attributes = request.json
    thing_name = attributes['name'].replace(' ', '')
    serial = attributes['serial']
    if attributes:
        try:
            # Gets all things within specific group related to the device and checks if component with the same name exists
            things = iot.list_things_in_thing_group(thingGroupName=serial)
            thing_name = serial + '_' + thing_name
            if thing_name in things['things']:
                return {'error': 1, 'text': 'Choose a unique name.'}
            thing_attr = {"attributes": {
                "type": comp_configs[attributes['component']]['type'],
                "model": attributes['component'],
                "serial": serial
            }}
            # Create a thing
            thing = iot.create_thing(
                thingName=thing_name,
                attributePayload=thing_attr
            )
            if 'thingArn' in thing:
                # Add the thing to the Thing Group related to the device
                iot.add_thing_to_thing_group(
                    thingGroupName=serial,
                    thingArn=thing['thingArn']
                )
                # Get the certificate ARN attached to the device by reading the cert attribute of the Thing group
                group_disc = iot.describe_thing_group(thingGroupName=serial)
                if 'thingGroupProperties' in group_disc:
                    cert = group_disc['thingGroupProperties']['attributePayload']['attributes']['cert']
                    # Attach the newly created thing to the certificate
                    resp = iot.attach_thing_principal(
                        thingName=thing_name,
                        principal=cert
                    )
                    # Modify the component configuration template and add it the s3 bucket
                    temp_conf = comp_configs[attributes['component']].copy()
                    for key, val in temp_conf['parameters'].items():
                        if key in attributes['parameters']:
                            temp_conf['parameters'][key] = attributes['parameters'][key]
                    temp_conf['name'] = attributes['name'].replace(' ', '')
                    if temp_conf['type'] == 'sensor':
                        temp_conf['data'] = attributes['data']
                        temp_conf['options'] = attributes['options']
                        temp_conf['actions'] = attributes['actions']
                    s3.put_object(Bucket="device-configurations",
                                  Key=serial + '/' + attributes['name'].replace(' ', '') + '.json',
                                  Body=json.dumps(temp_conf).encode("utf-8"))
                    return {'error': 0}

        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            text = f"Client Error: {error_code} - {error_message}"
            return {'error': 1, 'text': text}
    return ''


# Delete a specific component
@app.route('/deletecomponent', methods=['POST'])
def delete_component():
    data = request.json
    try:
        # Get the device certificate by reading the cert attribute and detach it, then delete the thing and delete it's configuration file from s3
        group = iot.describe_thing_group(thingGroupName=data['serial'])
        cert = group['thingGroupProperties']['attributePayload']['attributes']['cert']
        iot.detach_thing_principal(thingName=data['serial'] + '_' + data['component'], principal=cert)
        iot.delete_thing(thingName=data['serial'] + '_' + data['component'])
        s3.delete_object(Bucket='device-configurations', Key=data['serial'] + '/' + data['component'] + '.json')
        return {'error': 0}
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        text = f"Client Error: {error_code} - {error_message}"
        return {'error': 1, 'text': text}


# Home page. It will render the added devices if aws cookies exists, otherwise it will show a form to add device
@app.route('/')
def home():
    aws_id = request.cookies.get('aws_id', None)
    aws_secret = request.cookies.get('aws_secret', None)
    aws_session = request.cookies.get('aws_session', None)
    if aws_id and aws_session and aws_secret:
        return render_template("devices.html", notfound=False, aws_id=aws_id, aws_secret=aws_secret,
                               aws_session=aws_session)
    else:
        return render_template("devices.html", notfound=True)


# Function Handles adding a device
@app.route('/adddevice', methods=['POST'])
def add_device():
    data = request.json
    aws_id = request.cookies.get('aws_id', None)
    aws_secret = request.cookies.get('aws_secret', None)
    aws_session = request.cookies.get('aws_session', None)
    dlist = data['list']
    d = data['device']
    if d:
        # Check if the user already added the device before
        if d in dlist and aws_session and aws_secret and aws_id:
            return {'error': 1, 'text': "Device Already Added"}
        try:
            # Check if the device exists by check if a thing group created with it's serial number
            iot.describe_thing_group(thingGroupName=d)
            dlist.extend([d])
            role = get_role(dlist)
            # Create a temporary credentials
            temp_creds = sts.assume_role(RoleArn='arn:aws:iam::ACCOUNT_ID:role/iot_web', RoleSessionName=d,
                                         Policy=json.dumps(role), DurationSeconds=3600)
            aws_id = temp_creds['Credentials']['AccessKeyId']
            aws_secret = temp_creds['Credentials']['SecretAccessKey']
            aws_session = temp_creds['Credentials']['SessionToken']
            response = make_response(jsonify(error=0))
            expiry = datetime.now() + timedelta(minutes=59)
            # Set cookies
            response.set_cookie('aws_id', aws_id, expires=expiry)
            response.set_cookie('aws_secret', aws_secret, expires=expiry)
            response.set_cookie('aws_session', aws_session, expires=expiry)
            return response
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            text = f"Client Error: {error_code} - {error_message}"
            return {'error': 1, 'text': text}


# Function recreates credentials when a device deleted or the old credentials expires
@app.route('/devicedeleted', methods=['POST'])
def device_deleted():
    data = request.json
    dlist = data['list']
    if not dlist:
        response = make_response(jsonify(error=0))
        response.set_cookie('aws_id', '')
        response.set_cookie('aws_secret', '')
        response.set_cookie('aws_session', '')
        return response
    try:
        role = get_role(dlist)
        temp_creds = sts.assume_role(RoleArn='arn:aws:iam::ACCOUNT_ID:role/iot_web', RoleSessionName=dlist[0],
                                     Policy=json.dumps(role), DurationSeconds=3600)
        aws_id = temp_creds['Credentials']['AccessKeyId']
        aws_secret = temp_creds['Credentials']['SecretAccessKey']
        aws_session = temp_creds['Credentials']['SessionToken']
        response = make_response(jsonify(error=0))
        expiry = datetime.now() + timedelta(minutes=59)
        response.set_cookie('aws_id', aws_id, expires=expiry)
        response.set_cookie('aws_secret', aws_secret, expires=expiry)
        response.set_cookie('aws_session', aws_session, expires=expiry)
        return response
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        text = f"Client Error: {error_code} - {error_message}"
        return {'error': 1, 'text': text}


# Visualize sensors' data
@app.route('/device/<serial>/component/<comp>')
def component(serial, comp):
    try:
        resp = iot.describe_thing(thingName=serial + '_' + comp)
        if resp:
            model = resp['attributes']['model']
            if model == 'camera':
                return render_template("component.html", camera=True)
            else:
                conf = s3.get_object(Bucket='device-configurations', Key=serial + '/' + comp + '.json')
                d = json.loads(conf['Body'].read())
                data_dict = []
                for a in d['data']:
                    data_dict.append(data[a])
                return render_template("component.html", camera=False, data=data_dict, datacount=len(data_dict),
                                       serial=serial, comp=comp)
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        text = f"Client Error: {error_code} - {error_message}"
        return redirect(request.referrer)


if __name__ == '__main__':
    app.run()
