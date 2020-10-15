import sys
from time import sleep

import pygame
import json

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet 
from alien import Alien

class AlienInvation:
	"""Overall class to manage game assets and behaviour"""

	def __init__(self):
		"""Initialize the game and create game resources."""
		pygame.init()
		self.settings = Settings()

		if self.settings.screen_mode == 'Fullscreen':
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
			self.settings.screen_width = self.screen.get_rect().width
			self.settings.screen_height = self.screen.get_rect().height
		else:
			self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))	

		pygame.display.set_caption("Alien Invasion")

		#Create instances to store game statistics
		self.stats = GameStats(self)
		#Create a scorebaord
		self.sb = Scoreboard(self)



		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#Make the Play button
		self.play_button = Button(self, "Play")


	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update() 
				self._update_bullets()
				self._update_aliens()
				
			self._update_screen()

	def _check_events(self):	
		"""Respond to keyboard and mouse events"""
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:
				self._write_high_score()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#Rest game settings
			self.settings.initialize_dynamic_settings()
			#Reset game statistics
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and centre the ship
			self._create_fleet()
			self.ship.center_ship()

			#Hide the mouse pointer
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""Respond to key presses"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self._write_high_score()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Respoond to key releses"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _write_high_score(self):
		"""Write hgih score to file  so it cn be loaded in future"""
		high_score = self.stats.high_score
		persistent_data_file = self.settings.persistent_data_file
		with open(persistent_data_file, 'w') as f:
			json.dump(high_score, f)

	def _fire_bullet(self):
		"""Create a bullet and add to bullets group of sprites"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""
		Update position of bullets and remove bullets 
		that have disappeared from the group of sprites
		"""
		#Update bullet positions
		self.bullets.update()
		#Remove bullets that have disappeared 
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()  

	def _check_bullet_alien_collisions(self):
		#Check for any bullets that have hit aliens
		#Get rid of those bullets and aliens
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		#Update score
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points *len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		#Check if all aliens are destroyed
		#Destroy existing bullets and create new fleet
		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""
		Check if the fleet is at edge of screen 
		Then update positions of all aliens in the fleet
		"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for alien-ship collisions and reset the fleet
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#Look for aliens reaching the bottom and reset the fleet
		self._check_aliens_bottom() 

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in a row""" 
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.y = alien.rect.height + 2 * alien.rect.height * row_number
		alien.rect.x = alien.x
		alien.rect.y = alien.y
		self.aliens.add(alien)

	def _create_fleet(self):
		"""Create a fleet of aliens"""
		#Create an alien and find number of aliens per row

		#Determine number of aliens per row
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#Determine number of rows of aliens that fit on screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - ship_height -
			(3 * alien_height))
		number_rows = available_space_y // (2 * alien_height)
			
		#Create fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _check_fleet_edges(self):
		"""Respond if any aliens reach a screen edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break
			
	def _change_fleet_direction(self):
		"""Drop the entire fleet and change directions"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed 
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""Respond to a ship being hit"""
		#Decrement ships_left
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and centre the ship
			self._create_fleet()
			self.ship.center_ship()

			#Pause to allow user to notice the change
			sleep(0.5)
		else: 
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""Check if an alien hits the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if an alien and ship collide
				self._ship_hit()
				break
 
	def _update_screen(self):
		"""Update images on the screen and flip to new screen"""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Draw the scorebaord
		self.sb.show_score()

		#Draw the Play button if the game is not active
		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()



if __name__ == '__main__':
	#Make a game instance and run the game
	ai = AlienInvation()
	ai.run_game()