class Settings:
	"""A class to store all settings for the Alien Invasion"""

	def __init__(self):
		"""Initialize the game's static settings"""
		#Screen settings
		#Set screen_mode to 'Fullscreen' for fullscreen mode
		self.screen_mode = 'Window'  
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#Ship settings
		self.ship_limit = 3

		#Bullet settings
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 70

		#Alien Settings
		self.fleet_drop_speed = 10

		#How quickly the game speeds up
		self.speed_up_scale = 1.1

		#How quickly points increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change inside the game"""
		self.ship_speed = 30
		self.bullet_speed = 30
		self.alien_speed = 1.0

		#Scoring
		self.alien_points = 50

		#Right is fleet_direction = 1 and left is fleet_direction = -1
		self.fleet_direction = 1

	def increase_speed(self):
		"""Method to increase speeds and points scored"""
		self.ship_speed *= self.speed_up_scale
		self.bullet_speed *= self.speed_up_scale
		self.alien_speed *= self.speed_up_scale
		self .alien_points = int(self.alien_points * self.score_scale)




