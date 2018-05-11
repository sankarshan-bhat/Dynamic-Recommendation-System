import tweepy
 
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
