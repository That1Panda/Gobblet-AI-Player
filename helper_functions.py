import pygame
from typing import Tuple

from constants import GUIStyles

def create_component(label: str, label_color: str, label_size: int = 14, font_family: str = "cambriamath", component_position: Tuple[int, int] = (0,0), component_size: Tuple[int, int] = (0,0)) -> Tuple[pygame.Rect, pygame.Surface]:
        """Creates component for the pygame

        Args:
            label (str): the text of the component.
            label_color (str): color of button component.
            label_size (int, optional): the size of the component text. Defaults to 14.
            font_family (str, optional): the font family of the label. Defaults to "Georgia".
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
        font = pygame.font.SysFont(name=font_family, size=label_size, bold=True)

        # Defines the label and text color
        surf = font.render(label, True, label_color)

        # Defines the component position and size
        component = pygame.Rect(left, top, width, height)

        return component, surf
    
def integrate_button_to_screen(screen: pygame.Surface, component: pygame.Rect, label_surf: pygame.Surface, is_selected: bool, label_position: Tuple[float, float], opacity: float = GUIStyles.OPACITY.value) -> None:
        """Integrates the button into the screen

        Args:
            screen (pygame.Surface): screen to be integrated with.
            component (pygame.Rect): the component need to be integrated.
            label_surf (pygame.Surface): the label surf of the component.
            is_selected (bool): boolean variable indicates if the button is selected.
            label_position (Tuple[float, float]): the offset of the label from the component where it is defined as, position from top first then from left.
            opacity (float): the background opacity. Default to OPACITY. 
        """
        # Extracts the label position from position tuple
        y, x = label_position
        
        opacity_surface = pygame.Surface(component.size)
        opacity_surface.set_alpha(opacity)

        # Checks if the button is selected
        if is_selected:
            opacity_surface.fill(GUIStyles.SELECTED_BUTTON_BACKGROUND_COLOR.value)
            pygame.draw.rect(screen, GUIStyles.BACKGROUND_COLOR.value, component, 1)
        else:
            opacity_surface.fill(GUIStyles.UNSELECTED_BUTTON_BACKGROUND_COLOR.value)
            pygame.draw.rect(screen, GUIStyles.BACKGROUND_COLOR.value, component)
        
        # Binds the label surf to the component
        screen.blit(opacity_surface, (component.x, component.y))
        screen.blit(label_surf, (component.x+ x, component.y + y))