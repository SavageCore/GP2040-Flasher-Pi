import pygame
import pyudev
import os
from splash_screen import SplashScreen
from button import Button
from picotool import Picotool
from github import Github
from state_manager import StateManager

# Hide pygame message
os.putenv('PYGAME_HIDE_SUPPORT_PROMPT', '1')
# Output to PiTFT screen
os.putenv('SDL_FBDEV', '/dev/fb1')

# Load selected firmware from state file or default to 0
state_manager = StateManager()
selected_firmware = state_manager.get_value("selected_firmware") or 0

github = Github()
version, release_date, firmware_files = github.get_latest_release_info()

# Initialise the pygame library
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240), 0, 16)
screen.fill((0, 0, 0))
pygame.display.update()

# If no firmware files are found, exit
if firmware_files is None:  # None is returned if the API request fails
    print("Error looking up GitHub releases")
    exit()


def clear_screen(screen):
    screen.fill((0, 0, 0))
    pygame.display.update()


def render_text(screen, text, font, color, padding=5):
    # Calculate the maximum font size that fits within the screen dimensions
    max_font_size = 100
    text_width, text_height = font.size(text)
    while text_width + (2 * padding) > screen.get_width() or text_height + (2 * padding) > screen.get_height():
        max_font_size -= 1
        font = pygame.font.Font(None, max_font_size)
        text_width, text_height = font.size(text)

    text_surface = font.render(text, True, color)

    # Calculate the position with padding
    x = (screen.get_width() - text_width - (2 * padding)) // 2
    y = (screen.get_height() - text_height - (2 * padding)) // 2

    # Apply padding to the text position
    text_rect = text_surface.get_rect(x=x + padding, y=y + padding)

    screen.blit(text_surface, text_rect)
    pygame.display.update()


def flash_drive_handler(action, device):
    global selected_firmware
    global splash

    device_name = device.sys_name.split('/')[-1]
    if action == 'add' and device_name == "sda" and device.get('ID_VENDOR') == 'RPI' and device.get('ID_MODEL') == 'RP2':
        picotool = Picotool()
        splash.set_text("Pico detected")

        download_url = firmware_files[selected_firmware]["browser_download_url"]
        firmware_file = github.download_file(download_url)

        # If the firmware file is downloaded successfully, flash it to the Pico
        if firmware_file is not None:
            if picotool.get_program_name() is None:
                splash.set_text("Flashing...")
                result = picotool.flash_firmware(firmware_file)
                if result:
                    screen.fill((0, 255, 0))
                    render_text(screen, "Firmware flashed successfully",
                                pygame.font.Font(None, 100), (255, 255, 255))

                    pygame.time.wait(3000)
                    splash.set_text("Waiting for Pico...")
                    splash.show()
                else:
                    screen.fill((255, 0, 0))
                    pygame.display.update()

                    render_text(screen, "Error flashing firmware",
                                pygame.font.Font(None, 100), (255, 255, 255))
                    print("Error flashing firmware")
            else:
                splash.set_text("Nuking...")
                result = picotool.nuke_firmware()
                if result:
                    splash.set_text("Nuked. Waiting for Pico...")
                else:
                    print("Error flashing firmware")
                    render_text(screen, "Error flashing firmware",
                                pygame.font.Font(None, 100), (255, 255, 255))
        else:
            print("Error downloading firmware file")

def get_info_from_firmware_file(firmware_file):
    # Example names:
    # GP2040-CE_0.7.2_Stress.uf2
    # GP2040-CE_0.7.2_RP2040AdvancedBreakoutBoard.uf2
    # I want to return:
    # 0.7.2
    # Stress

    firmware_file = firmware_file.replace(".uf2", "")
    firmware_file = firmware_file.split("_")

    version = firmware_file[1].split(".")
    version = ".".join(version)

    name = firmware_file[2].split(".")
    name = ".".join(name)

    return version, name

def main():
    global selected_firmware
    global splash
    global screen

    splash.show()

    button1 = Button(17)
    button2 = Button(22)
    button3 = Button(23)
    button4 = Button(27)

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by('block')
    observer = pyudev.MonitorObserver(monitor, flash_drive_handler)
    observer.start()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check for button presses
        if button1.is_button_pressed():
            selected_firmware = (
                selected_firmware + 1) % len(firmware_files)

            state_manager.set_value("selected_firmware", selected_firmware)

            version, name = get_info_from_firmware_file(firmware_files[selected_firmware]["name"])

            splash.set_text(name + " (" + version + ")")
            # Small delay to prevent button bounce
            pygame.time.delay(200)
        if button2.is_button_pressed():
            selected_firmware = (
                selected_firmware - 1) % len(firmware_files)

            state_manager.set_value("selected_firmware", selected_firmware)

            version, name = get_info_from_firmware_file(firmware_files[selected_firmware]["name"])
            splash.set_text(name + " (" + version + ")")
            # Small delay to prevent button bounce
            pygame.time.delay(200)
        if button3.is_button_pressed():
            splash.set_text("Button 3")
        b4result = button4.is_button_pressed()
        if b4result == True:
            splash.set_text("Button 4")
        elif b4result == "double_press":
            running = False

    # Clean up
    observer.stop()
    pygame.quit()


if __name__ == '__main__':
    initial_text = "Select firmware to flash"
    if selected_firmware is not 0:
        version, name = get_info_from_firmware_file(firmware_files[selected_firmware]["name"])
        initial_text = "Firmware {} selected".format(name + " (" + version + ")")

    splash = SplashScreen(
        screen, 'assets/images/gp2040-ce-logo-inside-no-background.png', (0, 0, 0), initial_text)

    main()
