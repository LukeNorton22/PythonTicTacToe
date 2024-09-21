import pygame
import random

def play_sound(sound, loop=False, volume=1.0):
    """Plays a given sound. If loop is True, loops the sound indefinitely. Adjust volume."""
    if isinstance(sound, pygame.mixer.Sound):
        sound.set_volume(volume)  # Adjust volume
        if loop:
            sound.play(loops=-1)  # Loop indefinitely
        else:
            sound.play()
    elif sound == "music":
        pygame.mixer.music.set_volume(volume)
        if loop:
            pygame.mixer.music.play(-1)  # Loop indefinitely
        else:
            pygame.mixer.music.play()

def stop_sound(sound):
    """Stops the given sound or soundtrack."""
    if isinstance(sound, pygame.mixer.Sound):
        sound.stop()  # Stop sound effect
    elif sound == "music":
        pygame.mixer.music.stop()  # Stop background music

def init_sounds():
    """Initializes and returns all necessary sounds."""
    win_sound = pygame.mixer.Sound('win_sound.wav')
    click_sound = pygame.mixer.Sound('click_sound.wav')
    draw_sound = pygame.mixer.Sound('draw_sound.wav')
    soundtrack = pygame.mixer.Sound('soundtrack.wav')  # Ensure it's a .wav if using Sound

    return win_sound, click_sound, draw_sound, soundtrack

def win_animation(screen, winner_text_top, winner_text_bottom, WIDTH, HEIGHT, confetti_stop=False):
    # Define colors for confetti
    confetti_colors = [pygame.Color(255, 0, 0), pygame.Color(0, 0, 255), pygame.Color(0, 255, 0),
                       pygame.Color(255, 255, 0), pygame.Color(255, 165, 0)]  # Red, Blue, Green, Yellow, Orange

    # Define the font for the winner text
    winner_font_size = int(HEIGHT * 0.1)  # 10% of the screen height
    winner_font = pygame.font.Font(None, winner_font_size)

    # Run the animation for a few seconds
    start_time = pygame.time.get_ticks()  # Track time to stop after a few seconds
    confetti_duration = 3000  # Confetti duration (in milliseconds)
    while pygame.time.get_ticks() - start_time < confetti_duration:  # Run for 3 seconds
        screen.fill(pygame.Color(50, 50, 50))  # Dark background

        # Render both lines separately
        winner_message_top = winner_font.render(winner_text_top, True, pygame.Color(255, 255, 255))  # White text
        winner_message_bottom = winner_font.render(winner_text_bottom, True, pygame.Color(255, 255, 255))

        # Display the first line ("WINNER") at the center of the screen
        screen.blit(winner_message_top, (
            WIDTH // 2 - winner_message_top.get_width() // 2, HEIGHT // 3 - winner_message_top.get_height() // 2))

        # Display the second line (e.g., "PLAYER 1" or "AI") below the first line
        screen.blit(winner_message_bottom, (
            WIDTH // 2 - winner_message_bottom.get_width() // 2, HEIGHT // 3 + winner_message_top.get_height()))

        # Simulate falling confetti only if confetti_stop is False
        if not confetti_stop:
            for _ in range(100):  # 100 confetti pieces per frame
                confetti_x = random.randint(0, WIDTH)
                confetti_y = random.randint(0, HEIGHT)
                confetti_color = random.choice(confetti_colors)
                confetti_size = random.randint(5, 10)
                pygame.draw.rect(screen, confetti_color, (confetti_x, confetti_y, confetti_size, confetti_size))

        pygame.display.update()  # Update the screen
        pygame.time.delay(100)  # Delay to control the speed of the animation

def draw_screen_animation(screen, WIDTH, HEIGHT):
    """Draws a simple draw animation on the screen."""
    animation_font = pygame.font.Font(None, int(HEIGHT * 0.1))
    draw_text = animation_font.render("DRAW!", True, pygame.Color(255, 255, 255))
    screen.blit(draw_text, (
        WIDTH // 2 - draw_text.get_width() // 2,
        HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Display for 2 seconds
