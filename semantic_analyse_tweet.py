import spacy
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import requests

#from spacy.en import English
#nlp = English()

class MyListener(StreamListener):
 
	def on_data(self, data):
		print ("inside on_data")
		try:
			print (type(data))
			tweet_text = json.loads(data)
			print (tweet_text)
			tweet_text = tweet_text["text"]

			print(tweet_text)
			pouplate_profile(tweet_text)
			return True
		except BaseException as e:
		    print("Error on_data: %s" % str(e))
		return True
 
	def on_error(self, status):
		print(status)
		return True

def getKeywords(st):
	nlp = spacy.load('en')
	doc = nlp(st)

	'''
	print (doc)
	for np in doc.noun_chunks:
		print ("np",np.text)
	'''
	noun_adj_pairs = []
	for i,token in enumerate(doc):
	    if token.pos_ not in ('NOUN','PROPN'):
	        continue

	    for j in range(i-1,len(doc)):
	        if doc[j].pos_ == 'ADJ':
	            noun_adj_pairs.append((token,doc[j]))
	            break

	return noun_adj_pairs

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def extract_tweet():
	consumer_key ="pUVDi94pxaNgc214PQrhpPUwa"
	consumer_secret ="U8juTSRI2RazqQRIqlqp1qoWcaYVxH7bi2Ka3BKhdk5rPYcIVD"
	access_token ="994457489709125632-7jsHa4jzK2lN7ZoEi6Muv7aeNIWPDmp"
	access_token_secret ="FiJ0Budbxd3bvXi596vSK8Gc2ShmwoCeVTvtPDxLZTBo1"
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	twitter_stream = Stream(auth, MyListener())
	twitter_stream.filter(follow=["994457489709125632"])
	'''
	consumer_key ="pUVDi94pxaNgc214PQrhpPUwa"
	consumer_secret ="U8juTSRI2RazqQRIqlqp1qoWcaYVxH7bi2Ka3BKhdk5rPYcIVD"
	access_token ="994457489709125632-7jsHa4jzK2lN7ZoEi6Muv7aeNIWPDmp"
	access_token_secret ="FiJ0Budbxd3bvXi596vSK8Gc2ShmwoCeVTvtPDxLZTBo1"
	 
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	 
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	 
	statuses = api.user_timeline()
	for status in statuses:
		print status.text
	'''

def pouplate_profile(tweet):
	#print (tweet)
	#inputs = [u'Aa is good movie But Bb was bad in it.', u'Aa might be good actor but his acting in movie Picku is very bad', u'Aa is good movie But Bb was bad in it.', u'Aa is good movie But Bb was bad in it.']
	noun_adjective_pairs = getKeywords(tweet)
	print (noun_adjective_pairs)
	for noun,adjective  in noun_adjective_pairs:
		criteria = noun
		payload = 'text='+ str(adjective)
		print (payload)
		r = requests.post("http://text-processing.com/api/sentiment/", data=payload)
		resp= json.loads(r.text)
		print (resp)

	#for inp in inputs:
		#print (inp, getKeywords(inp))



extract_tweet()