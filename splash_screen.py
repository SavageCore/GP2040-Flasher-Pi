import pygame


class SplashScreen(object):
    def __init__(self, screen, image_file, background_colour=(0, 0, 0), text="", padding_top=20, padding_bottom=20, padding_left=20, padding_right=20):
        self.screen = screen
        self.background_colour = background_colour
        self.image_file = image_file
        self.text = text
        self.padding_top = padding_top
        self.padding_bottom = padding_bottom
        self.padding_left = padding_left
        self.padding_right = padding_right
        self.up_arrow_image = pygame.transform.scale(pygame.image.load(
            "assets/icons/chevron-up-outline.png").convert_alpha(), (16, 16))
        self.down_arrow_image = pygame.transform.scale(pygame.image.load(
            "assets/icons/chevron-down-outline.png").convert_alpha(), (16, 16))

    # Display the splash screen
    def show(self):
        if self.image_file is not None:
            # Load the original PNG image
            original_image = pygame.image.load(self.image_file).convert_alpha()

            # Get the screen dimensions
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()

            # Calculate the desired width and height based on the screen dimensions
            # Adjust the scaling factor as needed
            desired_width = int(screen_width * 0.8)
            desired_height = int(screen_height * 0.8)

            # Calculate the scaling factor based on the image's aspect ratio
            image_width, image_height = original_image.get_rect().size
            width_ratio = desired_width / image_width
            height_ratio = desired_height / image_height
            scaling_factor = min(width_ratio, height_ratio)

            # Scale the image while maintaining the aspect ratio
            scaled_width = int(image_width * scaling_factor)
            scaled_height = int(image_height * scaling_factor)
            scaled_image = pygame.transform.scale(
                original_image, (scaled_width, scaled_height))

            # Calculate the position to center the scaled image
            center_x = (screen_width - scaled_width) // 2

            # Blit the scaled image onto the screen at the top with horizontal center alignment
            self.screen.fill(self.background_colour)
            self.screen.blit(scaled_image, (center_x, self.padding_top))

            # Calculate the maximum width available for the text
            max_text_width = screen_width - 2 * self.padding_left

            # Render the text with the maximum available width
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()

            # Check if the text exceeds the maximum available width
            if text_rect.width > max_text_width:
                # Scale down the font size to fit the available width
                font_size = int(36 * max_text_width / text_rect.width)
                font = pygame.font.Font(None, font_size)
                text_surface = font.render(self.text, True, (255, 255, 255))
                text_rect = text_surface.get_rect()

            # Calculate the position to center the text
            center_y = (screen_height - scaled_height -
                        text_rect.height - self.padding_bottom) // 2

            # Calculate the position for the text
            text_x = (screen_width - text_rect.width) // 2
            text_y = center_y + scaled_height + self.padding_bottom

            # Blit the text onto the screen
            self.screen.blit(text_surface, (text_x, text_y))

            # Calculate the position to blit the arrow images
            arrow_x = screen_width - self.padding_right - self.padding_right
            arrow__up_y = 35
            arrow__down_y = arrow__up_y + self.up_arrow_image.get_height() + 10

            # Blit the arrow images onto the screen
            self.screen.blit(self.up_arrow_image, (arrow_x, arrow__up_y))
            self.screen.blit(self.down_arrow_image,
                             (arrow_x, arrow__down_y + self.up_arrow_image.get_height()))

            pygame.display.update()

    # Remove the splash screen
    def hide(self):
        self.screen.fill(self.background_colour)
        pygame.display.update()

    # Set the text for the splash screen
    def set_text(self, text):
        self.text = text
        self.show()
