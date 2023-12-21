import sys
from typing import Tuple
import pygame

from constants import PlayersTypes, SelectedPlayer

from gameController import GameController
from player import Player

TITLE_BACKGROUND_COLOR = (255, 255, 255)
UNSELECTED_BUTTON_BACKGROUND_COLOR = (230, 230, 230)
SELECTED_BUTTON_BACKGROUND_COLOR = (200, 200, 200)

class SelectPlayersScreen:
    def create_component(self, label: str, label_color: str, label_size: int = 14, component_position: Tuple[int, int] = (0,0), component_size: Tuple[int, int] = (0,0)) -> Tuple[pygame.Rect, pygame.Surface]:
        """Creates component for the pygame

        Args:
            label (str): the text of the component.
            label_color (str): color of button component.
            label_size (int, optional): the size of the component text. Defaults to 14. 
            component_position (Tuple[int, int], optional): tuple contains the position of the component defined as position from top then from left. Defaults to (0,0).
            component_size (Tuple[int, int], optional): tuple contains the size of the component defined as its width then its height. Defaults to (0,0).

        Returns:
            Tuple[pygame.Rect, pygame.Surface]: return the component and the surf contains text, the only thing left is to bind them using blit function in the while loop of the game 
        """
        # Extracts the top and left positions
        top, left = component_position

        # Extracts the button sizes
        width, height = component_size

        # Defines the font size
        font = pygame.font.SysFont(name="Georgia", size=label_size, bold=True)

        # Defines the label and text color
        surf = font.render(label, True, label_color)

        # Defines the component position and size
        component = pygame.Rect(left, top, width, height)

        return component, surf
    
    def integrate_button_to_screen(self, screen: pygame.Surface, component: pygame.Rect, label_surf: pygame.Surface, is_selected: bool, label_position: Tuple[float, float]) -> None:
        """Integrates the button into the screen

        Args:
            screen (pygame.Surface): screen to be integrated with.
            component (pygame.Rect): the component need to be integrated.
            label_surf (pygame.Surface): the label surf of the component.
            is_selected (bool): boolean variable indicates if the button is selected.
            label_position (Tuple[float, float]): the offset of the label from the component where it is defined as, position from top first then from left.
        """
        # Extracts the label position from position tuple
        y, x = label_position

        # Checks if the button is selected
        if is_selected:
            pygame.draw.rect(screen, SELECTED_BUTTON_BACKGROUND_COLOR, component)
        else:
            pygame.draw.rect(screen, UNSELECTED_BUTTON_BACKGROUND_COLOR, component)
        
        # Binds the label surf to the component
        screen.blit(label_surf, (component.x+ x, component.y + y))
    
    def show_result_screen(self, game_message: str):
        screen = pygame.display.set_mode((396, 396))
        result_component, result_text_surf = self.create_component(label= game_message, label_color="black", label_size=20, component_position=(100,98), component_size=(200,60))
        play_again_button, play_again_text_surf = self.create_component(label= "play again", label_color="black",component_position=(150,98), component_size=(200,60))

        # Variable to keep our game loop running 
        running = True
        
        # game loop 
        while running: 
            screen.fill('White')
            # for loop through the event queue   
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handles play again button
                    if play_again_button.collidepoint(event.pos):
                        return
  
            # Integrates `Select First Screen` title to the screen
            pygame.draw.rect(screen, TITLE_BACKGROUND_COLOR, result_component)
            screen.blit(result_text_surf, (result_component.x + 7, result_component.y + 7))
            
            self.integrate_button_to_screen(screen=screen, component=play_again_button, label_surf=play_again_text_surf, is_selected=True, label_position=(20,65))
            
            pygame.display.flip()

    def create_gambet_game(self, first_player_type: int, second_player_type: int):
        first_player: Player
        second_player: Player

        if first_player_type == SelectedPlayer.HUMAN.value:
            first_player = Player(player_name="First", player_type=PlayersTypes.HUMAN.value, symbol='X', color='W', algo="alpha_beta_pruning")
        else:
            first_player = Player(player_name="First", player_type=PlayersTypes.COMPUTER_1.value, symbol='X', color='W', algo="alpha_beta_pruning")
            first_player.difficulty = first_player_type
        
        if second_player_type == SelectedPlayer.HUMAN.value:
            second_player = Player(player_name="Second", player_type=PlayersTypes.HUMAN.value, symbol='Y', color='blue', algo="alpha_beta_pruning")
        else:
            second_player = Player(player_name="Second", player_type=PlayersTypes.COMPUTER_2.value, symbol='Y', color='blue', algo="alpha_beta_pruning")
            second_player.difficulty = second_player_type
        
        game_controller = GameController(player1=first_player, player2=second_player)
        game_message: str = game_controller.play_game()

        self.show_result_screen(game_message=game_message)
    
    def show_select_players_screen(self):
        screen = pygame.display.set_mode((396, 600))
        pygame.display.set_caption("Select Players")

        first_player_type: int = SelectedPlayer.UNSELECTED.value
        second_player_type: int = SelectedPlayer.UNSELECTED.value

        # Creates `Select First Player` title
        select_first_player_component, select_first_player_text_surf = self.create_component(label="Select First Player", label_color="black", label_size=20, component_position=(0,0), component_size=(200,60))

        # Creates first player buttons
        human_button_for_first_player, human_text_surf_for_first_player  = self.create_component(label="Human", label_color="red", component_position=(50,123), component_size=(150,40))
        easy_computer_button_for_first_player, easy_computer_text_surf_for_first_player  = self.create_component(label="Easy Computer", label_color="red", component_position=(100,123), component_size=(150,40))
        normal_computer_button_for_first_player, normal_computer_text_surf_for_first_player  = self.create_component(label="Normal Computer", label_color="red", component_position=(150,123), component_size=(150,40))
        hard_computer_button_for_first_player, hard_computer_text_surf_for_first_player  = self.create_component(label="Hard Computer", label_color="red", component_position=(200,123), component_size=(150,40))

        # Creates `Select Second Player` title
        select_second_player_component, select_second_player_text_surf = self.create_component(label="Select Second Player", label_color="black", label_size=20, component_position=(250,0), component_size=(200,60))

        # Creates second player buttons
        human_button_for_second_player, human_text_surf_for_second_player  = self.create_component(label="Human", label_color="blue", component_position=(300,123), component_size=(150,40))
        easy_computer_button_for_second_player, easy_computer_text_surf_for_second_player  = self.create_component(label="Easy Computer", label_color="blue", component_position=(350,123), component_size=(150,40))
        normal_computer_button_for_second_player, normal_computer_text_surf_for_second_player  = self.create_component(label="Normal Computer", label_color="blue", component_position=(400,123), component_size=(150,40))
        hard_computer_button_for_second_player, hard_computer_text_surf_for_second_player  = self.create_component(label="Hard Computer", label_color="blue", component_position=(450,123), component_size=(150,40))

        # Creates next button
        next_button, next_text_surf = self.create_component(label="Next", label_color="black", component_position=(530,123), component_size=(150,40))

        # Variable to keep our game loop running 
        running = True
        
        # game loop 
        while running: 
            screen.fill('White')
            # for loop through the event queue   
            for event in pygame.event.get(): 
                # Check for QUIT event       
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handles first player action
                    if human_button_for_first_player.collidepoint(event.pos):
                        first_player_type = SelectedPlayer.HUMAN.value
                    if easy_computer_button_for_first_player.collidepoint(event.pos):
                        first_player_type = SelectedPlayer.EASY_COMPUTER.value
                    if normal_computer_button_for_first_player.collidepoint(event.pos):
                        first_player_type = SelectedPlayer.NORMAL_COMPUTER.value
                    if hard_computer_button_for_first_player.collidepoint(event.pos):
                        first_player_type = SelectedPlayer.HARD_COMPUTER.value
                    
                    # Handles second player action
                    if human_button_for_second_player.collidepoint(event.pos):
                        second_player_type = SelectedPlayer.HUMAN.value
                    if easy_computer_button_for_second_player.collidepoint(event.pos):
                        second_player_type = SelectedPlayer.EASY_COMPUTER.value
                    if normal_computer_button_for_second_player.collidepoint(event.pos):
                        second_player_type = SelectedPlayer.NORMAL_COMPUTER.value
                    if hard_computer_button_for_second_player.collidepoint(event.pos):
                        second_player_type = SelectedPlayer.HARD_COMPUTER.value

                    if next_button.collidepoint(event.pos):
                        if first_player_type != SelectedPlayer.UNSELECTED.value and second_player_type != SelectedPlayer.UNSELECTED.value:
                            self.create_gambet_game(first_player_type, second_player_type)
                            screen = pygame.display.set_mode((396,600))

            # Integrates `Select First Screen` title to the screen
            pygame.draw.rect(screen, TITLE_BACKGROUND_COLOR, select_first_player_component)
            screen.blit(select_first_player_text_surf, (select_first_player_component.x+ 5, select_first_player_component.y + 5))
            
            # Integrates human button for the first player to the screen
            self.integrate_button_to_screen(screen=screen, component=human_button_for_first_player, label_surf=human_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.HUMAN.value, label_position=(9,48))

            # Integrates easy computer button for the first player to the screen
            self.integrate_button_to_screen(screen=screen, component=easy_computer_button_for_first_player, label_surf=easy_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.EASY_COMPUTER.value, label_position=(9,23))

            # Integrates normal computer button for the first player to the screen
            self.integrate_button_to_screen(screen=screen, component=normal_computer_button_for_first_player, label_surf=normal_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.NORMAL_COMPUTER.value, label_position=(9,10))

            # Integrates hard computer button for the first player to the screen
            self.integrate_button_to_screen(screen=screen, component=hard_computer_button_for_first_player, label_surf=hard_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.HARD_COMPUTER.value, label_position=(9,23))
      
            # Integrates `Select Second Screen` title to the screen
            pygame.draw.rect(screen, TITLE_BACKGROUND_COLOR, select_second_player_component)
            screen.blit(select_second_player_text_surf, (select_second_player_component.x+ 5, select_second_player_component.y + 5))

            # Integrates human button for the second player to the screen
            self.integrate_button_to_screen(screen=screen, component=human_button_for_second_player, label_surf=human_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.HUMAN.value, label_position=(9,48))

            # Integrates easy computer button for the second player to the screen
            self.integrate_button_to_screen(screen=screen, component=easy_computer_button_for_second_player, label_surf=easy_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.EASY_COMPUTER.value, label_position=(9,23))

            # Integrates normal computer button for the second player to the screen
            self.integrate_button_to_screen(screen=screen, component=normal_computer_button_for_second_player, label_surf=normal_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.NORMAL_COMPUTER.value, label_position=(9,10))

            # Integrates hard computer button for the second player to the screen
            self.integrate_button_to_screen(screen=screen, component=hard_computer_button_for_second_player, label_surf=hard_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.HARD_COMPUTER.value, label_position=(9,23))

            # Integrates Next Button
            self.integrate_button_to_screen(screen=screen, component=next_button, label_surf=next_text_surf, is_selected= first_player_type != SelectedPlayer.UNSELECTED.value and second_player_type != SelectedPlayer.UNSELECTED.value, label_position=(9,56))

            pygame.display.update()

    def start(self) -> None:
        """Starts the Game
        """
        pygame.init()
        self.show_select_players_screen()