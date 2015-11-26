#
# Filename: health_threshold.py
#
# Author: /u/CrystalLord
#
#

class HealthThreshold:
	# Class for determining the health of a subreddit.

	def __init__(self, unhealthy=15, critical=5):
		self.unhealthy = unhealthy
		self.critical = critical
	
	def __repr__(self):
		'''
		Representation method
			
			@return
			Returns a representation in the form HealthThreshold(unhealthy,critical)
		'''
		s = "HealthThreshold("+str(self.unhealthy_post_count)+","+str(self.critical_post_count)+")"
		return s
	
	def rate_health(self, value):
		'''
		Rate the health of a certain value
			
			@param
			-value: The value we are rating

			@return
			Returns either 'healthy', 'unhealthy', or 'critical'
		'''
		if value > self.unhealthy:
			return "healthy"
		elif value > self.critical:
			return "unhealthy"
		return "critical"


