class GameStats:
	"""Track statistics for the game"""

	def __init__(self, ai_game):
		"""Initialize statistics"""
		self.settings = ai_game.settings
		self.reset_stats()
		#Start game in an active state
		self.game_active = False
		self.high_score = 0

	def reset_stats(self):
		"""Initialize statiostics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
