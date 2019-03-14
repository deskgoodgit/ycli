import requests
import csv
import time
import pytz
import datetime


host = 'https://www.yammer.com'
proxies = {
    'http': '',
    'https': ''
}
sleep_time = 10

def get_group(token, groupID):
        with open ('group.csv', 'w+', newline='',  encoding="utf-8") as csvfile:
                writer =  csv.writer(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
                endpoint = '{}/api/v1/messages/in_group/{}.json?threaded=true'.format(host,groupID)
                headers = {'Authorization' : 'Bearer {}'.format(token),
                        "Content-Type": "application/json"
                }
                params = {'older_than': ''}

                while True :
                        response = requests.get( endpoint , headers=headers, proxies=proxies, params=params if params['older_than'] != '' else None)                
                        json = response.json()

                        if 'messages' in json:
                                if len(json['messages']) == 0:
                                        break
                                for message in json['messages']:                                        
                                        writer.writerow([message['id'], message['created_at'], message['liked_by']['count'], message['web_url'], message['id']])
                                        params['older_than'] = message["id"]
                        else:                                                               
                                break
                        time.sleep(sleep_time)


def get_thread_meta(token, threadID):
        endpoint = 'https://www.yammer.com/api/v1/threads/{}.json'.format(threadID)
        headers = {'Authorization' : 'Bearer {}'.format(token),
                "Content-Type": "application/json"
        }
        response = requests.get( endpoint , headers=headers, proxies=proxies)      
        if response.json() is not None:
                return response.json()


def get_replyCount(token, threadID, msgID):
        
        return get_thread_meta(token, threadID)['stats']['updates']-1
        
        # endpoint = 'https://www.yammer.com/api/v1/messages/in_thread/{}.json'.format(threadID)
        # headers = {'Authorization' : 'Bearer {}'.format(token),
        #         "Content-Type": "application/json"
        # }
        # params = {'older_than': ''}

        # replyCount = 0        

        # while True :
        #         response = requests.get( endpoint , headers=headers, proxies=proxies, params=params if params['older_than'] != '' else None)                
        #         json = response.json()
                                       
        #         if threadID == msgID and len(json['messages'])>0:
        #                 replyCount += len(json['messages'])                                        
        #                 params['older_than'] = json['messages'][-1]['id']                        
        #         else:
        #                 break
                
        #         time.sleep(15)

        # if replyCount == 0:
        #         return replyCount
        # else:
        #         return replyCount-1

def _get_current_user(token):
        endpoint = '{}/api/v1/users/current.json'.format(host)
        headers = {'Authorization' : 'Bearer {}'.format(token),
                "Content-Type": "application/json"
                }
        response = requests.get( endpoint , headers=headers, proxies=proxies)                        
        return response.json()  
                


def get_own_messages(token):
        current_user = _get_current_user(token)
        current_user_id = current_user['id']
        current_user_email = current_user['email']
        with open('own_messages.csv', 'w+', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
                writer.writerow(['sender_id', 'id', 'date', 'privacy','web_url', '#likes', '#replies']) #Header
                endpoint = '{}/api/v1/search.json'.format(host)
                headers = {'Authorization' : 'Bearer {}'.format(token),
                       "Content-Type": "application/json"
                }
                params = {'page': 1, 
                        'search': current_user_email}
                hktz = pytz.timezone('Asia/Hong_Kong')


                while True:
                        response = requests.get( endpoint , headers=headers, proxies=proxies, params=params)                
                        json = response.json()  
                        if len(json["messages"]["messages"]) == 0 :
                                break

                        for message in json['messages']['messages']:
                                if message['sender_id'] == current_user_id:
                                        createdAt = datetime.datetime.strptime(message['created_at'], '%Y/%m/%d %H:%M:%S %z')
                                        hktzCreatedAt = createdAt.astimezone(hktz)
                                        hktzCreatedAt_F =  hktzCreatedAt.strftime("%Y/%m/%d %H:%M:%S")
                                        writer.writerow([message['sender_id'], message['id'], hktzCreatedAt_F, message['privacy'], message['web_url'], message['liked_by']['count'], get_replyCount(token, message['thread_id'], message['id'])])                                                                                                
                                        
                        params['page'] = params['page']+1
                        time.sleep(sleep_time)
                # if 'messages' in json:
                #         if len(json['messages']) == 0:
                #                 break
                #         for message in json['messages']:
                #                 print(message['id'])
                #                 if message['sender_id'] == json['meta']['current_user_id']:
                #                         createdAt = datetime.datetime.strptime(message['created_at'], '%Y/%m/%d %H:%M:%S %z')
                #                         hktzCreatedAt = createdAt.astimezone(hktz)
                #                         hktzCreatedAt_F = hktzCreatedAt.strftime("%Y/%m/%d %H:%M:%S")
                #                         writer.writerow([message['sender_id'], message['id'], hktzCreatedAt_F, message['privacy'], message['web_url'], message['liked_by']['count'], get_replyCount(token, message['thread_id'], message['id'])])                                                                                                
                #                 params['older_than'] = message["id"]
                # else:
                #         break
                # print('older_than')        
                # print(params['older_than'])
                #time.sleep(15)
                

#deprecated 
def get_sent(token):
        with open ('sent_messages.csv', 'w+', newline='',  encoding="utf-8") as csvfile:
               writer =  csv.writer(csvfile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
               writer.writerow(['sender_id', 'id', 'date', 'privacy','web_url', '#likes', '#replies']) #Header
               endpoint = '{}/api/v1/messages/sent.json'.format(host)
               headers = {'Authorization' : 'Bearer {}'.format(token),
                       "Content-Type": "application/json"
               }
               params = {'older_than': ''}
               hktz = pytz.timezone('Asia/Hong_Kong')                

               while True :
                        response = requests.get( endpoint , headers=headers, proxies=proxies, params=params if params['older_than'] != '' else None)                
                        json = response.json()
              
                        if 'messages' in json:
                                if len(json['messages']) == 0:
                                        break
                                for message in json['messages']:
                                        print(message['id'])
                                        if message['sender_id'] == json['meta']['current_user_id']:
                                                createdAt = datetime.datetime.strptime(message['created_at'], '%Y/%m/%d %H:%M:%S %z')
                                                hktzCreatedAt = createdAt.astimezone(hktz)
                                                hktzCreatedAt_F = hktzCreatedAt.strftime("%Y/%m/%d %H:%M:%S")
                                                writer.writerow([message['sender_id'], message['id'], hktzCreatedAt_F, message['privacy'], message['web_url'], message['liked_by']['count'], get_replyCount(token, message['thread_id'], message['id'])])                                                                                                
                                        params['older_than'] = message["id"]
                        else:
                                break
                        print('older_than')        
                        print(params['older_than'])
                        time.sleep(sleep_time)


def main(argv):

        import configparser
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        if len(argv) < 2 :
                print( "Error: Usage ycli Token Command [Parameters]")
                return -1
       
        token = argv[0]         
        command = argv[1]

        proxies['https'] = config['DEFAULT']['HTTPS_PROXY']
        proxies['http'] = config['DEFAULT']['HTTP_PROXY']  

        if command == 'get_sent':
                print('Getting Sent Messages...')
                get_sent(token)
                print('Done Getting Sent Messages!')
        elif command == 'get_group':
                print('Getting Group Messages...')
                get_group(token, argv[2])
                print('Done Getting Group Messages!')       
        elif command == 'get_own_messages':
                print('Getting Own Messages...')
                get_own_messages(token)
                print('Done Getting Own Messages!')
                                              
        else:
                print('Command: {} is not a valid command.'.format(command))