from redis_operations import RedisOperations
import json

class MergeProfiles():

	r = None

	def __init__(self):
		self.r = RedisOperations()

	def updateStaticProfile(user_id="994457489709125632"):
		static_profile = self.r.get_static_profile(user_id)
		if static_profile:
			static_profile_json = json.loads(static_profile)
		
		dynamic_profile = self.r.get_dynamic_profile(user_id)
		if dynamic_profile:
			dynamic_profile_json = json.loads(dynamic_profile)

		updated_static_profile_json = self.getUpdatedProfile(static_profile_json, dynamic_profile_json, True)

		self.r.set(user_id+"_static", updated_static_profile_json)

	
	def updateProfiles(self, json_data, user_id="994457489709125632"):
				
		dynamic_profile = self.r.get_dynamic_profile(user_id)
		if dynamic_profile:
			dynamic_profile_json = json.loads(dynamic_profile)
		else:
			static_profile = self.r.get_static_profile(user_id)
			if static_profile:
				dynamic_profile_json = json.loads(static_profile)

		tweet_profile_json = self.getUpdatedProfile(dynamic_profile_json, json_data, False)
		updated_dynamic_profile_json = self.getUpdatedProfile(dynamic_profile_json, json_data, True)

		self.r.set(user_id+"_dynamic", updated_dynamic_profile_json)


	def getUpdatedProfile(self, dynamic_profile_json, json_data, gen_dynamic_profile=False):
		
		tweet_profile_json = dynamic_profile_json
		
		for key, json_data_value in json_data.iteritems():

			if json_data_value:
				json_data_dist = json_data_value.get("distribution")
				if json_data_dist:
					
					for json_data_item_name, json_data_item_value in json_data_dist.iteritems():
						
						tweet_profile_value = tweet_profile_json.get(key).get("distribution").get(json_data_item_name)

						if not tweet_profile_value:
							tweet_profile_json.get(key).get("distribution")[json_data_item_name] = json_data_item_value
						else:
							if json_data_item_value.get("pct") > 0 or gen_dynamic_profile:
								total_count = tweet_profile_value.get("count") + json_data_item_value.get("count")
								tweet_profile_value["count"] = total_count
								tweet_profile_value["pct"] = tweet_profile_value.get("pct") + json_data_item_value.get("pct") / total_count

								total_factor_count = tweet_profile_json.get(key).get("factor",{}).get("count") + json_data_item_value.get("count")
								tweet_profile_json.get(key).get("factor",{})["count"] = total_factor_count
								tweet_profile_json.get(key).get("factor",{})["pct"] = tweet_profile_json.get(key).get("factor",{}).get("pct") + json_data_item_value.get("pct") / total_factor_count

							else:
								del tweet_profile_json.get(key).get("distribution")[json_data_item_name]

		return tweet_profile_json



# TEST

json_data1 = {
	"genre": {
		"distribution": {
			"comedy": {
				"pct": 70,
				"count": 1
			}
		}
	},
	"cast": {
		"distribution": {
			"shahrukh khan": {
				"pct": 60,
				"count": 1
			},
			"deepika padukone": {
				"pct": -20,
				"count": 1
			}
		}
	}
}

mp = MergeProfiles()
print mp.updateProfiles(json_data1)