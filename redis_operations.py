import redis

class RedisOperations():

	r = None

	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def get_static_profile(self, user_id):
		return self.r.get(user_id+"_static")

	def get_dynamic_profile(self, user_id):
		return self.r.get(user_id+"_dynamic")


#get_static_profile("994457489709125632")
#get_dynamic_profile("994457489709125632")