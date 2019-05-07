import requests
import json
import re
import random

#Construct Key phrases from text file (assumes in same folder as .py file):
key_phrases = open('keyphrase.txt')
keylist = [i.strip() for i in key_phrases.readlines()]


#FEEDLY REQUESTS:
user_id = ##user-id (optional)
access_token = ##your-access-token
tags_url = 'https://cloud.feedly.com/v3/tags'
streams_url = 'https://cloud.feedly.com/v3/streams/contents?streamId='
markers_url = 'https://cloud.feedly.com/v3/markers'
headers = {'Authorization': access_token}




#ACCESS TAGS (LIST OF DIFFERENT BOARDS) DATA FOR PROFILE AND CONVERT TO JSON LIST
tags_http = requests.get('{}'.format(tags_url), headers = headers)
tags_list = json.loads(tags_http.text)


#CHOOSE THE BOARD TO SCRAPE:
def tags_ids():
    for x, v in enumerate(tags_list):
        print(x, v['label'],'\n')
    ids = input('Enter the board number from this list.')
    return int(ids)

#GET THE ITEMS ON THE BOARD:
def get_board_items():
    board = tags_ids()
    board_http = requests.get('{}{}'.format(streams_url, tags_list[board]['id']), headers = headers)
    #print(json.loads(board_http.text)['items'])
    return json.loads(board_http.text)['items']

#CONSTRUCT THE ARTICLES:
def construct_articles():
    new_articles = get_board_items()
    export_list = []
    for item in new_articles:
        hashtag = item['tags'][0]['label']
        if item['unread'] == True:
            #ACTION TO PRODUCE ARTICLE STRUCTURE:
            export_list.append({'title': item['title'], 'link': item['canonicalUrl'], 'content': (item['summary']['content']).rsplit('. ', 1)[0] + '. ' + keylist[random.randint(1,len(keylist))] + ' #' + hashtag, 'image': item['visual']['url'], 'id': item['id']})
            #MARK ARTICLES AS READ SO WON'T BE SCRAPED ON NEXT RUN:
            #requests.post('{}'.format(markers_url), data=json.dumps({"action": "markAsRead", "type": "entries", "entryIds": ["{}".format(item['id'])]}), headers = headers)
    return export_list


#--------------------------


#BUFFER POSTS:

buffer_client_id = ##your-id (optional)
buffer_access_token = ##your-access-token (required)
buffer_client_secret = ##your-client-secret (optional)
buffer_redirect_url = 'urn:ietf:wg:oauth:2.0:oob'
buff_header = {'Authorization': buffer_access_token}
buffer_profile_url = 'https://api.bufferapp.com/1/profiles.json'
buffer_create_url = 'https://api.bufferapp.com/1/updates/create.json'

#ACCESS SOCIAL ACCOUNTS DATA FOR PROFILE AND CONVERT TO JSON LIST
buff_http = requests.get('{}?access_token={}'.format(buffer_profile_url, buffer_access_token))
buff_profile = json.loads(buff_http.text)

#GET SOCIAL ACCOUNT TO POST TO:
def buff_ids():
    for x, v in enumerate(buff_profile):
        print(x, v['service'], '-',v['service_username'],'\n')
    ids = input('Choose the account number from this list.')
    return int(ids)




#RUN UPLOAD TO BUFFER:
def buff_post():
    my_list = construct_articles()
    ids = buff_ids()
    for article in my_list:
        buff_data_update = {
            "profile_ids": ["{}".format(buff_profile[ids]['id'])],
            "text": article['content'],
            "media[photo]": article['image'],
            "media[link]": article['link'],
            "media[title]": article['title'],
            "media[description]": article['content'],
            #"picture": None,
            #"thumbnail": None,


        }
        requests.post('{}?access_token={}'.format(buffer_create_url, buffer_access_token), data=(buff_data_update))





buff_post()
