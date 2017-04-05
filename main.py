# -*- coding: utf-8 -*-
import os, re
import urllib, urllib2 # Y U NO REQUESTS!? :(
from json import loads

REGEX = re.compile('\[\[(.*?)\]\]')
ALL_CARDS = loads(urllib2.urlopen('https://netrunnerdb.com/api/2.0/public/cards').read())['data']

with file('abbreviations.json', 'r') as f:
  ABBREVIATIONS = loads(f.read())

def lambda_handler(event, context):
    body = loads(event['body'])
    text = body['event']['text']
    channel = body['event']['channel']
    print 'Found: ' + str(text) + ' in channel ' + channel
    matches = REGEX.findall(text)

    if matches:
        print 'matches was some'
        for match in matches:
            print 'working on ' + str(match)
            if match in ABBREVIATIONS:
                print 'match was in ABBREVIATIONS'
                match = ABBREVIATIONS[match]
            print 'checking for ' + match
            for card in ALL_CARDS:
                if all([c in card['title'].lower() for c in match.lower().split()]):
                    print 'all condition was matched'
                    submitResponse(card['code'], card['title'], channel)
                    break
    else:
        print 'matches was None'
    return {
        "statusCode": 200,
        "headers": {"Content-Type":"application/json"},
        "body": 'I hear ya'
    }
    
def submitResponse(card_id, card_name, channel):
    print 'inside submitResponse: ' + str(card_id) + ':' + str(card_name) + ':' + str(channel)
    url = 'https://slack.com/api/chat.postMessage'
    
    data = 'token=' + os.environ['responseToken'] + '&attachments=%5B%7B%27image_url%27%3A+%27https%3A%2F%2Fnetrunnerdb.com%2Fcard_image%2F' + card_id + '.png%27%2C+%27title%27%3A+%27' + card_name + '%27%7D%5D&channel=' + channel
    print 'data: ' + str(data)
    req = urllib2.Request(url, data)
    urllib2.urlopen(req)
