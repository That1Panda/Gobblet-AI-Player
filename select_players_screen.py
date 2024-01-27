import sys
import pygame

from constants import PlayersTypes, SelectedPlayer, GUIStyles
from gameController import GameController
from helper_functions import create_component, integrate_button_to_screen
from player import Player

GAME_TITLE_FONT_FAMILY = "bahnschrift"

class SelectPlayersScreen:
    def create_gambet_game(self, first_player_type: int, second_player_type: int):
        first_player: Player
        second_player: Player

        if first_player_type == SelectedPlayer.HUMAN.value:
            first_player = Player(player_name="First", player_type=PlayersTypes.HUMAN.value, symbol='X', color='W', color_rgb= (255,0,0), algo="alpha_beta_pruning")
        else:
            first_player = Player(player_name="First", player_type=PlayersTypes.COMPUTER_1.value, symbol='X', color='W', color_rgb= (255,0,0), algo="alpha_beta_pruning")
            first_player.difficulty = first_player_type
        
        if second_player_type == SelectedPlayer.HUMAN.value:
            second_player = Player(player_name="Second", player_type=PlayersTypes.HUMAN.value, symbol='Y', color='blue', color_rgb= (0,0,255), algo="alpha_beta_pruning")
        else:
            second_player = Player(player_name="Second", player_type=PlayersTypes.COMPUTER_2.value, symbol='Y', color='blue', color_rgb= (0,0,255), algo="alpha_beta_pruning")
            second_player.difficulty = second_player_type
        
        game_controller = GameController(player1=first_player, player2=second_player)
        game_controller.play_game()
    
    def show_select_players_screen(self):
        screen = pygame.display.set_mode((730, 350))
        pygame.display.set_caption("Select Players")

        first_player_type: int = SelectedPlayer.UNSELECTED.value
        second_player_type: int = SelectedPlayer.UNSELECTED.value

        # Creates `Gambit Game` title
        gambit_game_title_component, gambit_game_text_surf = create_component(label="Gambit Game", label_color="Orange", label_size=60, font_family= GAME_TITLE_FONT_FAMILY , component_position=(15,180), component_size=(200,60))

        # Creates `Select First Player` title
        select_first_player_component, select_first_player_text_surf = create_component(label="Select First Player", label_color="red", label_size=25, component_position=(120,90), component_size=(170,60))

        # Creates first player buttons
        human_button_for_first_player, human_text_surf_for_first_player  = create_component(label="Human", label_color="red", component_position=(170,40), component_size=(150,40))
        easy_computer_button_for_first_player, easy_computer_text_surf_for_first_player  = create_component(label="Easy Computer", label_color="red", component_position=(170,200), component_size=(150,40))
        normal_computer_button_for_first_player, normal_computer_text_surf_for_first_player  = create_component(label="Normal Computer", label_color="red", component_position=(220,40), component_size=(150,40))
        hard_computer_button_for_first_player, hard_computer_text_surf_for_first_player  = create_component(label="Hard Computer", label_color="red", component_position=(220,200), component_size=(150,40))

        # Creates `Select Second Player` title
        select_second_player_component, select_second_player_text_surf = create_component(label="Select Second Player", label_color="blue", label_size=25, component_position=(120,430), component_size=(200,60))

        # Creates second player buttons
        human_button_for_second_player, human_text_surf_for_second_player  = create_component(label="Human", label_color="blue", component_position = (170,380), component_size=(150,40))
        easy_computer_button_for_second_player, easy_computer_text_surf_for_second_player  = create_component(label="Easy Computer", label_color="blue", component_position=(170,540), component_size=(150,40))
        normal_computer_button_for_second_player, normal_computer_text_surf_for_second_player  = create_component(label="Normal Computer", label_color="blue", component_position=(220,380), component_size=(150,40))
        hard_computer_button_for_second_player, hard_computer_text_surf_for_second_player  = create_component(label="Hard Computer", label_color="blue", component_position=(220,540), component_size=(150,40))

        # Creates next button
        next_button, next_text_surf = create_component(label="Next", label_color="Black", label_size= 25, component_position=(300,290), component_size=(150,40))

        # Variable to keep our game loop running 
        running = True
        
        # game loop 
        while running: 
            screen.fill(GUIStyles.BACKGROUND_COLOR.value)
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
                            screen = pygame.display.set_mode((730, 350))
                            first_player_type = SelectedPlayer.UNSELECTED.value
                            second_player_type = SelectedPlayer.UNSELECTED.value

            # Integrates `Gambit game` title to the screen
            pygame.draw.rect(screen, GUIStyles.BACKGROUND_COLOR.value, gambit_game_title_component)
            screen.blit(gambit_game_text_surf, (gambit_game_title_component.x, gambit_game_title_component.y))

            for side_index in range(4):
                pygame.draw.rect(screen, (255,165,0), (30-side_index,110-side_index,330,170), 2,10)

            # Integrates `Select First Screen` title to the screen
            pygame.draw.rect(screen, GUIStyles.BACKGROUND_COLOR.value, select_first_player_component, width=1)
            screen.blit(select_first_player_text_surf, (select_first_player_component.x+ 5, select_first_player_component.y + 5))
                        
            opacity_surface = pygame.Surface((330, 170))
            opacity_surface.fill((255, 255, 255))
            opacity_surface.set_alpha(255 * 0.1)
            screen.blit(opacity_surface, (30, 110))

            # Integrates human button for the first player to the screen
            integrate_button_to_screen(screen=screen, component=human_button_for_first_player, label_surf=human_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.HUMAN.value, label_position=(9,48))

            # Integrates easy computer button for the first player to the screen
            integrate_button_to_screen(screen=screen, component=easy_computer_button_for_first_player, label_surf=easy_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.EASY_COMPUTER.value, label_position=(9,23))

            # Integrates normal computer button for the first player to the screen
            integrate_button_to_screen(screen=screen, component=normal_computer_button_for_first_player, label_surf=normal_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.NORMAL_COMPUTER.value, label_position=(9,10))

            # Integrates hard computer button for the first player to the screen
            integrate_button_to_screen(screen=screen, component=hard_computer_button_for_first_player, label_surf=hard_computer_text_surf_for_first_player,is_selected=first_player_type == SelectedPlayer.HARD_COMPUTER.value, label_position=(9,23))

            for side_index in range(4):
                pygame.draw.rect(screen, (255,165,0), (370-side_index,110-side_index,330,170), 2,10)

            # Integrates `Select Second Screen` title to the screen
            pygame.draw.rect(screen, GUIStyles.BACKGROUND_COLOR.value, select_second_player_component)
            screen.blit(select_second_player_text_surf, (select_second_player_component.x+ 5, select_second_player_component.y + 5))
            screen.blit(opacity_surface, (370, 110))

            # Integrates human button for the second player to the screen
            integrate_button_to_screen(screen=screen, component=human_button_for_second_player, label_surf=human_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.HUMAN.value, label_position=(9,48))

            # Integrates easy computer button for the second player to the screen
            integrate_button_to_screen(screen=screen, component=easy_computer_button_for_second_player, label_surf=easy_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.EASY_COMPUTER.value, label_position=(9,23))

            # Integrates normal computer button for the second player to the screen
            integrate_button_to_screen(screen=screen, component=normal_computer_button_for_second_player, label_surf=normal_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.NORMAL_COMPUTER.value, label_position=(9,10))

            # Integrates hard computer button for the second player to the screen
            integrate_button_to_screen(screen=screen, component=hard_computer_button_for_second_player, label_surf=hard_computer_text_surf_for_second_player,is_selected=second_player_type == SelectedPlayer.HARD_COMPUTER.value, label_position=(9,23))

            # Integrates Next Button
            if first_player_type != SelectedPlayer.UNSELECTED.value and second_player_type != SelectedPlayer.UNSELECTED.value:
                integrate_button_to_screen(screen=screen, component=next_button, label_surf=next_text_surf, is_selected= False, label_position=(6,49))

            pygame.display.update()

    def start(self) -> None:
        """Starts the Game
        """
        pygame.init()
        self.show_select_players_screen()