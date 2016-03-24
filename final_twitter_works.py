import requests_oauthlib
import test106 as test
import webbrowser
import json

import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
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


class Post():
    """object representing status update"""
    def __init__(self, post_dict={}):
        if 'hashtags' in post_dict['entities']:
            self.hashtags= post_dict['entities']['hashtags']
        else:
            self.hashtags = []
        # if the post dictionary has a 'comments' key, set an instance variable self.comments
        # to the list of comment dictionaries you extract from post_dict. 
        # Otherwise, set self.comments to be an empty list: []
   
        # Something similar has already been done for the contents (message) of the original post, 
        # which is the value of the 'message' key in the dictionary, when it is present 
        # (photo posts don't have a message). See above for that code, which you can model the rest after!

        
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

    def score(self, tag_list):  #creates a score for each search
       
        pos_count=0
        for tag in tag_list:
            if tag.lower() in pos_ws:
               pos_count+=1   
        
        neg_count=0
        for tag in tag_list:
            if tag.lower() in neg_ws:
               neg_count+=1
            
        return pos_count-neg_count
       
                
                

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)
    
# Get these from the Twitter website, by going to
# https://apps.twitter.com/ and creating an "app"
# Don't fill in a callback_url and put in a placeholder for the website
# Visit the Keys and Access Tokens tab for your app and grab the following two values

client_key = 'u3Sz6Ros93XAzifph2znB2mFz' # what Twitter calls Consumer Key
client_secret = 'Kcv8YErgGKlwgRstiCyz8VJDAnYE8pUwuSt6EnpmupTqoIvINk' # What Twitter calls Consumer Secret


def get_tokens():
    ## Step 1. Obtain a request token which will identify you (the client) in the next step. At this stage you will only need your client key and secret

    # OAuth1Session is a class defined in the requests_oauthlib module
    # Two values are passed to the __init__ method of OAuth1Session
    # -- the value of client_key is passed as the value of the first parameter (whose name we don't know)
    # -- the value of client_secret is passed as the value of the parameter that is also called client_secret
    # after this line executes, oauth will now be an instance of the class OAuth1Session
    oauth = requests_oauthlib.OAuth1Session(client_key, client_secret=client_secret)

    request_token_url = 'https://api.twitter.com/oauth/request_token'

    # invoke the fetch_request_token method
    # it returns a dictionary that might look like this:
    # {
    #     "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #     "oauth_token_secret": "Kd75W4OQfb2oJTV0vzGzeXftVAwgMnEK9MumzYcM"
    # }
    # It also saves the oauth_token as an instance variable of the object
    # oauth is bound to, so it can be used in later steps
    fetch_response = oauth.fetch_request_token(request_token_url)

    # pull the two values out of the dictionary and store them in variable for later use
    # note that d.get('somekey') is another way of writing d['somekey']
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')


    ## Step 2. Obtain authorization from the user (resource owner) to access their protected resources (images, tweets, etc.). This is commonly done by redirecting the user to a specific url to which you add the request token as a query parameter. Note that not all services will give you a verifier even if they should. Also the oauth_token given here will be the same as the one in the previous step.

    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    # append the query parameters need to make it a full url.
    # they will include the resource_owner_key from the previus step,
    # which was stored in the oauth object above as an instance variable
    # when fetch_request_token was invoked
    authorization_url = oauth.authorization_url(base_authorization_url)

    webbrowser.open(authorization_url)

    # After the user authenticates at Twitter, it would normally "redirect"
    # the browser back to our website. But we aren't running a website.
    # Some services, like Twitter, will let you configure the app to 
    # display a verifier, or the entire redirect url, rather than actually
    # redirecting to it.
    # User will have to cut and paste the verifier or the whole redirect url

    # version where the website provides a verifier
    verifier = raw_input('Please input the verifier')

    # version where the website provides the entire redirect url
    # redirect_response = raw_input('Paste the full redirect URL here: ')
    # oauth_response = oauth.parse_authorization_response(redirect_response)
    # get back something like this
    #{
    #    "oauth_token": "Z6eEdO8MOmk394WozF5oKyuAv855l4Mlqo7hhlSLik",
    #    "oauth_verifier": "sdflk3450FASDLJasd2349dfs"
    #}
    # verifier = oauth_response.get('oauth_verifier')

    ## Step 3. Obtain an access token from the OAuth provider. Save this token as it can be re-used later. In this step we will re-use most of the credentials obtained uptil this point.

    # make a new instance of OAuth1Session, with several more parameters filled in
    oauth = requests_oauthlib.OAuth1Session(client_key,
                              client_secret=client_secret,
                              resource_owner_key=resource_owner_key,
                              resource_owner_secret=resource_owner_secret,
                              verifier=verifier)
                              
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    # get back something like this
    #{
    #    "oauth_token": "6253282-eWudHldSbIaelX7swmsiHImEL4KinwaGloHANdrY",
    #    "oauth_token_secret": "2EEfA6BG3ly3sR3RjE0IBSnlQu4ZrUzPiYKmrkVU"
    #}
    resource_owner_key = oauth_tokens.get('oauth_token')
    resource_owner_secret = oauth_tokens.get('oauth_token_secret')
    
    return (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier)

try:
    # See if you can read the credentials from the file
    # (If you have credentials for the wrong user, or expired credentials
    # just delete the file creds.txt
    f = open("creds.txt", 'r')
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = json.loads(f.read())
    f.close()
except:
    # If not, you'll have to get them
    # and then save them in creds.txt
    tokens = get_tokens()
    f = open("creds.txt", 'w')
    f.write(json.dumps(tokens))
    f.close()
    (client_key, client_secret, resource_owner_key, resource_owner_secret, verifier) = tokens
  
## Step 4. Access protected resources. 

# For endpoints that might be interesting to try, see
# https://dev.twitter.com/rest/tools/console and
# https://dev.twitter.com/rest/public
protected_url = 'https://api.twitter.com/1.1/account/settings.json'
oauth = requests_oauthlib.OAuth1Session(client_key,
                        client_secret=client_secret,
                        resource_owner_key=resource_owner_key,
                        resource_owner_secret=resource_owner_secret)

# Call the get method. The work of encoding the client_secret 
# and "signing" the request is taken care of behind the scenes.
# The results are also processed for you, including calling .read() and 
# encoding as json.
#r = oauth.get(protected_url)
# r is now an instance of the Response class in the requests module
# documentation at 
# http://docs.python-requests.org/en/latest/user/quickstart/#response-content

# Of particular interest to us is the json() method of the Response class
#print pretty(r.json())


####PAGING
# Getting multiple pages of results can be tricky. See Twitter's explanation at
# https://dev.twitter.com/rest/public/timelines
# (Other sites handle paging slightly differently; you'll have to read the documentation)

# Let's get my last 25 tweets, 5 at a time, accumulating all the tweet ids.
# Twitter actually lets you get 25 at a time, but not more than 200, so this
# is practice for when you want to get more than 200.

# To pass parameters using the requests_oauthlib module, we use the same 
# get() method used in the requests module. It combines some of the functions
# we were doing separately before with urllib2.urlopen and urllib.urlencode.
# see documentation at 
# http://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls



def celebrity_tags(post_insts):
    tag_dic={}  
   
    for p in post_insts:  #for every post of each celebrity search
       
        for h in p.hashtags: # for every hashtag in that post
            hashtag= h['text'] #get that hashtag
        
         
            if hashtag not in tag_dic:
                tag_dic[hashtag]=1
            else:
                tag_dic[hashtag]+=1 
            
       
            
    return tag_dic #returns a dictionary of tags for all 100 tweets
               
 
#open file and keep a list of post instances

def tag_list_maker(tags):
    tag_list=[]
    for tag in tags:
        tag_list.append(tag)
    
    return tag_list
    
def search_score_maker(res, big_tag_list):    #we want to take in all 100 tweets and create a score for that search based on their hashtags
    search_scores=[]
    score=[]
    
    try:
        for post in res['statuses']: #for every tweet in feed
            s= Post(post)      # create an instance 
        search_scores=[s.score(list) for list in big_tag_list]
    except:
        print "error"
   
    # for list in big_tag_list:   #for list of hashtags for each search (all of Beyonce's hashatags, all of Madonna's)
       
        # score= s.score(list)    # create a score for each search
        # search_scores.append(score) #append to our list of each search score
        
        
   
        
    return search_scores
    
 
def pos_search_maker(res, big_tag_list):
    pos_score=[]
    
    try:
        for post in res['statuses']: #for every tweet in feed
            s= Post(post)      # create an instance 
    
    
    
        for list in big_tag_list:   #for list of hashtags for each search (all of Beyonce's hashatags, all of Madonna's)
            pos=s.pos_tags(list)     
            pos_score.append(pos)  #pos total for that search
  
    except:
        print "error"
        
    return pos_score
    

def neg_search_maker(res, big_tag_list): 
    neg_score= []
    
    try:
        for post in res['statuses']: #for every tweet in feed
            s= Post(post)      # create an instance 
   
        for list in big_tag_list:   #for list of hashtags for each search (all of Beyonce's hashatags, all of Madonna's)
            neg=s.neg_tags(list)     
            neg_score.append(neg)  #pos total for that search
 
    except:
       print "error"   
    return neg_score
    
    
            
#pass every name in the list as a search parameter (q)
names= open('little_list.txt', 'r')
out= open('candidates.txt', 'w')

name_list= []
top_tag_list=[]
search_score=[]
pos_search=[]
neg_search=[]

for name in names.readlines()[0]: #for each name
    post_insts= []
    r = oauth.get("https://api.twitter.com/1.1/search/tweets.json", params = {'q': name, 'count' : 1})  #get 10 tweets
    res = r.json()

    print pretty(res['text'])
    
    try:
        for post in res['statuses']: #for every post                        #for every Tweet in the 100
            x= Post(post) #create an instance                               #create an instance of each one to get hashtag and score(s)
            post_insts.append(x) #append to list of instances               #we should have a list of 100 instances
           
    except:
        print "error"
    
            
    tag_dic= celebrity_tags(post_insts)                      #create a dictionary of all the tags in the 100 tweets           
    name_list.append(name[1:-1])                             #list of names
    
    search_score= search_score_maker(res, top_tag_list)    #assigns list of each search score  to search_score
    pos_search= pos_search_maker(res, top_tag_list)
    neg_search= neg_search_maker(res, top_tag_list)
    
    
    sorted_tags= sorted(tag_dic, key= lambda x: tag_dic[x], reverse= True)
    
    tag_zip_list= tag_list_maker(sorted_tags)
    top_tag_list.append(tag_zip_list)
    
    # for tag in sorted_tags: 
        # counts= tweets[tag]
        # count_zip_list= count_list_maker(counts)
    # top_count_list.append(count_zip_list[0])
    
    out.write("\n\n%s" % name)
    out.write( "***************************\n")
    # print "\n", name
    for tag in sorted_tags:
        counts= tag_dic[tag]
        
        out.write("%s %d\n" % (tag, counts))

print "Function 1"
print "Testing celebrity_tags...\n"
test.testEqual(type(celebrity_tags(post_insts)), type({}))        
test.testEqual(celebrity_tags(post_insts), tag_dic)        

print "\nFunction 2"
print "Testing tag_list_maker...\n"

test.testEqual(type(tag_list_maker([])), type([]))
test.testEqual(tag_list_maker(sorted_tags), tag_zip_list)

 

print "\nFunction 3"
print "Testing ...\n"


for post in res['statuses']:
    class_Test= Post(post)
    test.testEqual(type(class_Test.pos_tags([])), type(0))
    #test.testEqual()

for post in res['statuses']:
    print pretty(res['statuses'][1]['text'])

        
out.close()
names.close()    
          



#zip a dee doo dah
scores= zip(name_list, pos_search, neg_search, search_score)

#print scores
# print len(scores)
    

outfile= open("PoliticalCandidates.csv", "w")
outfile.write("Name, Positive Counts, Negative Counts, Score\n")

for score in scores:
    outfile.write("%s, %d, %d, %d\n" % score)

outfile.close()




         

