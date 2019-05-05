import requests
import json
import re

#FEEDLY REQUESTS:
user_id = '3a01f33e-d2f7-4cfe-9a2f-61f602a305fa'
access_token = 'A3aWNtW9aW5wRELjxNyJDscXzlGh6FNqEFHPNbfJICJHkRcu72g9I2GSaN8zveI2Elbgn6tm4IL4XUqOZ55XWouenDIJOThrxRgcQqZQcjLXeT-F5nx4l4hMvE7y1BR8X_n4Aht4BikdsLqe1q7bOx17aIuV6uY9YAOakHUKQNlA86bipfb_l14k6TCD_j06HyveGr4PxESornr1V_YtRgGCyqo2ASaSLqcLFmolKZhw_RxanilQsZdeqMiZkEo:feedlydev'
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
            export_list.append({'title': item['title'], 'link': item['canonicalUrl'], 'content': (item['summary']['content']).rsplit('. ', 1)[0] + '. ' + '#' + hashtag, 'image': item['visual']['url'], 'id': item['id']})
            #MARK ARTICLES AS READ SO WON'T BE SCRAPED ON NEXT RUN:
            #requests.post('{}'.format(markers_url), data=json.dumps({"action": "markAsRead", "type": "entries", "entryIds": ["{}".format(item['id'])]}), headers = headers)
    return export_list


#--------------------------


#BUFFER POSTS:

buffer_client_id = '5cc5ade2c2de1b657a081858'
buffer_access_token = '1/a54ba90e93b1ea8d54c460eb179a497c'
buffer_client_secret = '0dad187436b977f44068a61dffc6a16c'
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


#POST NEW ARTICLES TO BUFFER ACCOUNT:

#SET DATA TO BE POSTED:
#def buff_data_set():
#    buff_data_update = {
#        "profile_ids": ["{}".format(buff_profile[ids]['id'])],
#        "text": "This is an update example...",
#        "media": {
#            "link": "http://google.com",
#            "title": "Google",
#            "description": "The google homepage",
#            "picture": None,
#            "photo": None,
#            "thumbnail": None,
#        },
#
#    }


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



#requests.post('https://api.bufferapp.com/1/updates/create.json?access_token=1/a54ba90e93b1ea8d54c460eb179a497c', data=(buff_data_update))

#buff_post()
#POST Data
#text=This%20is%20an%20example%20update&
#profile_ids[]=4eb854340acb04e870000010&
#profile_ids[]=4eb9276e0acb04bb81000067&
#media[link]=http%3A%2F%2Fgoogle.com&
#media[description]=The%20google%20homepage


#print(buff_ids())

#print(buff_profile)

#RUN WHOLE PROCESS:

#def start_run():



buff_post()
