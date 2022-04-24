import requests
import json


def check_line_token(db, line_channel):
    status_code, response_data = verify_token(line_channel.line_channel_access_token)
    if status_code != 200:
        status_code, response_data = generate_token(
            line_channel.line_channel_id, line_channel.line_channel_secret)
        if status_code == 200:
            line_channel_access_token = response_data['access_token']
            line_token_expires_in = response_data['expires_in']
            line_channel.line_channel_access_token  = line_channel_access_token
            db.add(line_channel)
            db.commit()

    return line_channel


def verify_token(line_channel_access_token):
    url = 'https://api.line.me/v2/oauth/verify'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'access_token': line_channel_access_token}

    response = requests.post(url, data=data, headers=header)
    return response.status_code, json.loads(response.content)


def generate_token(line_channel_id, line_channel_secret):
    url = 'https://api.line.me/v2/oauth/accessToken'
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials',
            'client_id': line_channel_id,
            'client_secret': line_channel_secret}
    response = requests.post(url, data=data, headers=header)
    return response.status_code, json.loads(response.content)