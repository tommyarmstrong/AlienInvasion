import json
import os

from settings import Settings

class PersistentData:
	"""Class to read and save peristent data to file"""
	def __init__(self, ai_game):
		"""Initialize persistent data"""
		self.settings = ai_game.settings
		self.persistent_data_file = self.settings.persistent_data_file

		self._create_persistent_data_dictionary()

	def _create_persistent_data_dictionary(self):
		"""Method to set up dictionary of KVPs to manage persistent data"""
		if os.path.isfile(self.persistent_data_file):
			#Load dictionary with data from JSON
			with open(self.persistent_data_file) as f:
				self.persistent_data_dictionary = json.load(f)	
		else:
			#Load dictionary with default values
			self.persistent_data_dictionary = {
				'high_score'  : 0, 
				'last_player' : 'player_1',
				'last_score'  : 0}


