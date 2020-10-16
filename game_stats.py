import 	json
import os

class GameStats:
	"""Track statistics for the game"""

	def __init__(self, ai_game):
		"""Initialize statistics"""
		self.settings = ai_game.settings
		self.persistent_data = ai_game.persistent_data
		self.reset_stats()
		#Start game in an active state
		self.game_active = False
		self._read_high_score()

	def reset_stats(self):
		"""Initialize statiostics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1

	def _read_high_score(self):
		"""Read high score from persistent data dictionary"""
		self.high_score = self.persistent_data.persistent_data_dictionary['high_score']

		"""	
		filename = self.settings.persistent_data_file
		if os.path.isfile(filename):
			with open(filename) as f:
				self.high_score = json.load(f)
		else:
			self.high_score = 0
		"""