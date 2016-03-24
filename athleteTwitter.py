import requests_oauthlib
import test106 as test
import webbrowser
import json

import sys    
reload(sys)   
sys.setdefaultencoding('utf-8')


pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))

    
class Hashtag():
    """object representing status update"""
    def __init__(self, post_dict={}):
        if 'hashtags' in post_dict['entities']:
            self.hashtags= post_dict['entities']['hashtags']
        else:
            self.hashtags = []
      
      
    def pos_tags(self, tag_list):
        word_count=0
        for tag in tag_list:
            if tag.lower() in pos_ws:
               word_count+=1
        return word_count    
        
         
    def neg_tags(self, tag_list):
        word_count=0
        for tag in tag_list:
            if tag.lower() in neg_ws:
               word_count+=1
        return word_count

    def score(self, tag_list):  
       
        pos_count=0
        for tag in tag_list:
            if tag.lower() in pos_ws:
               pos_count+=1   
        
        neg_count=0
        for tag in tag_list:
            if tag.lower() in neg_ws:
               neg_count+=1
            
        return pos_count-neg_count
                       

client_key = 'G16TQJ3kAyoUC9rt0DOIVsrOT' 
client_secret = 'g0RdY92uW9GgrqUoLrwjAkGg4IMeBjo6wDdpuUkjB6oxzw51Ft' 

def get_tokens():
  
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://api.twitter.com/oauth/request_token'
   
    fetch_response = oauth.fetch_request_token(request_token_url)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')


    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
   
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url)

   
    verifier = raw_input('Please input the verifier')

    
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)
                              
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
   
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

try:
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
  
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens
  

protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)


def athlete_hashtags(post_insts):
    tag_dic={}  
   
    for p in post_insts:  
       
        for h in p.hashtags: 
            hashtag= h['text'] 
        
         
            if hashtag not in tag_dic:
                tag_dic[hashtag]=1
            else:
                tag_dic[hashtag]+=1 
            
       
            
    return tag_dic 
               
def big_hashtag_list(tags):
    tag_list=[]
    for tag in tags:
        tag_list.append(tag)
    
    return tag_list
    
def net_score_maker(res, big_tag_list):    
    net_scores=[]
    score=[]
    
    try:
        for post in res['statuses']: 
            s= Hashtag(post)     
        net_scores=[s.score(list) for list in big_tag_list]
    except:
        None  
   
        
    return net_scores
    
def total_positive_scores(res, big_tag_list):
    pos_score=[]
    
    try:
        for post in res['statuses']: 
            s= Hashtag(post)    
    
    
    
        for list in big_tag_list:   
            pos=s.pos_tags(list)     
            pos_score.append(pos) 
  
    except:
        None
        
    return pos_score
    
def total_negative_scores(result, big_tag_list): 
    neg_score= []
    
    try:
        for post in result['statuses']:
            s= Hashtag(post)      
   
        for list in big_tag_list:   
            neg=s.neg_tags(list)     
            neg_score.append(neg)  
 
    except:
       None   
    return neg_score
    
athletes= open('list_of_athletes.txt', 'r')
output= open('results.txt', 'w')

athlete_list= []
last_tags=[]
net_score=[]
positive_score=[]
negative_score=[]

for athlete in athletes.readlines(): 
    post_instances= []
    r = oauth.get("https://api.twitter.com/1.1/search/tweets.json", params = {'q': athlete, 'count' : 200})  
    result = r.json()
    
    try:
        for post in result['statuses']: 
            x= Hashtag(post) 
            post_instances.append(x) 
    except:
        None
    
            
    dict_of_tags= athlete_hashtags(post_instances)                               
    athlete_list.append(athlete[1:-1])                            
    
    net_score= net_score_maker(result, last_tags)   
    positive_score= total_positive_scores(result, last_tags)
    negative_score= total_negative_scores(result, last_tags)
    
    
    sorted_tags= sorted(dict_of_tags, key= lambda x: dict_of_tags[x], reverse= True)
    
    data_tag_list= big_hashtag_list(sorted_tags)
    last_tags.append(data_tag_list)
    
    
    output.write("\n\n%s" % athlete)
    output.write( "***************************\n")
    
    for tag in sorted_tags:
        counts= dict_of_tags[tag]
        
        output.write("%s %d\n" % (tag, counts))


        
test.testEqual(type(athlete_hashtags(post_instances)), type({}))        
test.testEqual(athlete_hashtags(post_instances), dict_of_tags)        


test.testEqual(type(big_hashtag_list([])), type([]))
test.testEqual(big_hashtag_list(sorted_tags), data_tag_list)


for post in result['statuses']:
    class_Test= Hashtag(post)
test.testEqual(type(class_Test.pos_tags([])), type(0))

        
output.close()
athletes.close()    
          
scores= zip(athlete_list, positive_score, negative_score, net_score)

outputfile= open("Data.csv", "w")
outputfile.write("athlete, Positive Counts, Negative Counts, Score\n")

for score in scores:
    outputfile.write("%s, %d, %d, %d\n" % score)

outputfile.close()




         

    