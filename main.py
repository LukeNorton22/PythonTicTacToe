import pygame
import time
import sys
from game_logic import create_board, check_win, is_draw, ai_smart_move, place_mark, end_game_logic
from game_additions import win_animation, draw_screen_animation, init_sounds, play_sound, stop_sound

######################## PYGAME UI LOGIC ##########################

# Initialize Pygame
pygame.init()

# Set up the display
info = pygame.display.Info()  # Get the screen resolution
WIDTH, HEIGHT = info.current_w, info.current_h  # Set to the full screen resolution

# Create a full-screen window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Tic Tac Toe")

# Define colors (Dark Mode Theme)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HOVER_COLOR = (100, 100, 100)
SOFT_YELLOW = pygame.Color(255, 213, 79)  # Soft Yellow color
DARKER_GRAY = pygame.Color(30, 30, 30)
PYTHON_BLUE = pygame.Color(52, 101, 164)  # Python Blue
BORDER_COLOR = pygame.Color(255, 213, 79)  # Python Yellow for border

# Load the Quicksand font
# Adjust font sizes based on screen height for better scaling
quicksand_font_size = int(HEIGHT * 0.15)  # 15% of screen height
quicksand_font = pygame.font.Font('Quicksand-Regular.ttf', quicksand_font_size)  # Adjust as needed

font_size = int(HEIGHT * 0.06)  # 6% of screen height
font = pygame.font.Font(None, font_size)

title_font_size = int(HEIGHT * 0.1)  # 10% of screen height
title_font = pygame.font.Font(None, title_font_size)

exit_font_size = int(HEIGHT * 0.05)  # 5% of screen height
exit_font = pygame.font.Font(None, exit_font_size)

# Padding for buttons
padding_x = WIDTH * 0.06  # 6% of screen width
padding_y = HEIGHT * 0.04  # 4% of screen height

# Button state to track expansion and pulsating
button_states = {
    "single_player_hover": False,
    "two_player_hover": False,
    "single_player_clicked": False,
    "two_player_clicked": False,
    "pulsate_timer": 0
}

# Create the initial board
game_board = create_board()


def reset_board():
    global game_board
    game_board = create_board()


def draw_board():
    screen.fill(DARKER_GRAY)
    # Adjust the positions based on WIDTH and HEIGHT
    pygame.draw.line(screen, SOFT_YELLOW, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), 5)
    pygame.draw.line(screen, SOFT_YELLOW, (2 * WIDTH / 3, 0), (2 * WIDTH / 3, HEIGHT), 5)
    pygame.draw.line(screen, SOFT_YELLOW, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), 5)
    pygame.draw.line(screen, SOFT_YELLOW, (0, 2 * HEIGHT / 3), (WIDTH, 2 * HEIGHT / 3), 5)


def draw_marks(board):
    for row in range(3):
        for col in range(3):
            x_pos = col * WIDTH / 3 + WIDTH / 6  # Center of the cell horizontally
            y_pos = row * HEIGHT / 3 + HEIGHT / 6  # Center of the cell vertically

            if board[row][col] == 'X':
                # Render X using the Quicksand font
                text = quicksand_font.render('X', True, PYTHON_BLUE)  # Render the "X" in blue
                screen.blit(text, text.get_rect(center=(x_pos, y_pos)))

            elif board[row][col] == 'O':
                # Render O using the Quicksand font
                text = quicksand_font.render('O', True, PYTHON_BLUE)  # Render the "O" in blue
                screen.blit(text, text.get_rect(center=(x_pos, y_pos)))


def get_mouse_position():
    x, y = pygame.mouse.get_pos()
    row = int(y // (HEIGHT / 3))
    col = int(x // (WIDTH / 3))
    position = row * 3 + col + 1
    return row, col, position


# Check if the mouse is hovering over a button
def is_hovering(mouse_pos, button_rect):
    return button_rect.collidepoint(mouse_pos)


def draw_buttons():
    # Define button rectangles with padding for text
    single_player_text = font.render("1 Player", True, SOFT_YELLOW)
    two_player_text = font.render("2 Player", True, SOFT_YELLOW)

    # Calculate button positions relative to screen size
    single_player_button = pygame.Rect(
        (WIDTH - single_player_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.3,
        single_player_text.get_width() + 2 * padding_x,
        single_player_text.get_height() + 2 * padding_y
    )
    two_player_button = pygame.Rect(
        (WIDTH - two_player_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.45,
        two_player_text.get_width() + 2 * padding_x,
        two_player_text.get_height() + 2 * padding_y
    )

    # Expand effect on hover
    expand_size = 10 if button_states['single_player_hover'] else 0
    expand_size_2 = 10 if button_states['two_player_hover'] else 0

    # Apply pulsating effect when clicked
    if button_states['single_player_clicked']:
        pulsate_offset = 5 if button_states['pulsate_timer'] % 10 < 5 else -5
        button_states['pulsate_timer'] += 1
        single_player_button.inflate_ip(pulsate_offset, pulsate_offset)

    if button_states['two_player_clicked']:
        pulsate_offset_2 = 5 if button_states['pulsate_timer'] % 10 < 5 else -5
        button_states['pulsate_timer'] += 1
        two_player_button.inflate_ip(pulsate_offset_2, pulsate_offset_2)

    # Draw buttons with hover effect and borders
    pygame.draw.rect(screen, BORDER_COLOR, single_player_button.inflate(expand_size, expand_size), 5)  # Border only
    pygame.draw.rect(screen, BORDER_COLOR, two_player_button.inflate(expand_size_2, expand_size_2), 5)  # Border only

    # Render and blit text onto buttons
    screen.blit(single_player_text,
                (single_player_button.centerx - single_player_text.get_width() / 2,
                 single_player_button.centery - single_player_text.get_height() / 2))
    screen.blit(two_player_text,
                (two_player_button.centerx - two_player_text.get_width() / 2,
                 two_player_button.centery - two_player_text.get_height() / 2))

    return single_player_button, two_player_button


def draw_end_buttons():
    play_again_text = font.render("Play Again", True, SOFT_YELLOW)
    exit_text = exit_font.render("Exit", True, SOFT_YELLOW)

    play_again_button = pygame.Rect(
        (WIDTH - play_again_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.5,
        play_again_text.get_width() + 2 * padding_x,
        play_again_text.get_height() + 2 * padding_y
    )
    exit_button = pygame.Rect(
        (WIDTH - exit_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.65,
        exit_text.get_width() + 2 * padding_x,
        exit_text.get_height() + 2 * padding_y
    )

    mouse_pos = pygame.mouse.get_pos()

    # Draw buttons with hover effect
    for button, text, hover_state in [(play_again_button, play_again_text, 'play_again_hover'),
                                      (exit_button, exit_text, 'exit_hover')]:
        if is_hovering(mouse_pos, button):
            pygame.draw.rect(screen, WHITE, button, 5)  # White border on hover
            button_states[hover_state] = True
        else:
            pygame.draw.rect(screen, SOFT_YELLOW, button, 5)
            button_states[hover_state] = False
        screen.blit(text, (button.centerx - text.get_width() / 2, button.centery - text.get_height() / 2))

    return play_again_button, exit_button


# Player vs AI Mode
def single_player_mode(player_mark, ai_mark):
    win_sound, click_sound, draw_sound, soundtrack = init_sounds()  # Initialize sounds

    play_sound(soundtrack, loop=True, volume=0.3)  # Start background soundtrack at lower volume

    reset_board()  # Ensure the board is reset for a new game
    player = 'Player'
    game_over = False

    while not game_over:
        draw_board()
        draw_marks(game_board)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player == 'Player':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col, position = get_mouse_position()
                    if place_mark(game_board, player_mark, position):
                        play_sound(click_sound)  # Play click sound on valid move
                        if check_win(game_board, player_mark):
                            stop_sound(soundtrack)  # Stop the background music
                            play_sound(win_sound)  # Play win sound
                            # Display WINNER screen with confetti
                            win_animation(screen, "WINNER", "PLAYER 1", WIDTH, HEIGHT, confetti_stop=False)
                            pygame.time.delay(3000)  # Delay for 3 seconds before showing GAME OVER
                            game_over = True
                        elif is_draw(game_board):
                            stop_sound(soundtrack)  # Stop the background music
                            play_sound(draw_sound)  # Play draw sound
                            draw_screen_animation(screen, WIDTH, HEIGHT)  # Play draw animation
                            game_over = True
                        player = 'AI'
            else:
                time.sleep(1)  # AI "thinks"
                ai_choice = ai_smart_move(game_board, player_mark, ai_mark)
                place_mark(game_board, ai_mark, ai_choice)
                play_sound(click_sound)  # Play click sound for AI move
                if check_win(game_board, ai_mark):
                    stop_sound(soundtrack)  # Stop the background music
                    play_sound(win_sound)  # Play win sound
                    # Display WINNER screen with confetti
                    win_animation(screen, "WINNER", "Matt!", WIDTH, HEIGHT, confetti_stop=False)
                    pygame.time.delay(3000)  # Delay for 3 seconds before showing GAME OVER
                    game_over = True
                elif is_draw(game_board):
                    stop_sound(soundtrack)  # Stop the background music
                    play_sound(draw_sound)  # Play draw sound
                    draw_screen_animation(screen, WIDTH, HEIGHT)  # Play draw animation
                    game_over = True
                player = 'Player'

    if game_over:
        end_game_logic()
    # Transition to "GAME OVER" screen
    show_game_over_screen()


# Two-player mode
def two_player_mode(player_1, player_2):
    win_sound, click_sound, draw_sound, soundtrack = init_sounds()  # Initialize sounds

    play_sound(soundtrack, loop=True, volume=0.3)  # Start background soundtrack at lower volume

    reset_board()  # Ensure the board is reset for a new game
    current_player = 'Player 1'
    current_mark = player_1
    game_over = False

    while not game_over:
        draw_board()
        draw_marks(game_board)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col, position = get_mouse_position()
                if place_mark(game_board, current_mark, position):
                    play_sound(click_sound)  # Play click sound on valid move
                    if check_win(game_board, current_mark):
                        stop_sound(soundtrack)  # Stop the background music
                        play_sound(win_sound)  # Play win sound
                        # Display WINNER screen with confetti
                        win_animation(screen, "WINNER", current_player, WIDTH, HEIGHT, confetti_stop=False)
                        pygame.time.delay(3000)  # Delay for 3 seconds before showing GAME OVER
                        game_over = True
                    elif is_draw(game_board):
                        stop_sound(soundtrack)  # Stop the background music
                        play_sound(draw_sound)  # Play draw sound
                        draw_screen_animation(screen, WIDTH, HEIGHT)  # Play draw animation
                        game_over = True

                    # Switch turns
                    if current_player == 'Player 1':
                        current_player = 'Player 2'
                        current_mark = player_2
                    else:
                        current_player = 'Player 1'
                        current_mark = player_1

    # Transition to "GAME OVER" screen
    show_game_over_screen()

def draw_exit_and_play_again_buttons():
    exit_text = exit_font.render("Exit", True, SOFT_YELLOW)
    play_again_text = exit_font.render("Play Again", True, SOFT_YELLOW)

    exit_button = pygame.Rect(
        (WIDTH - exit_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.7,
        exit_text.get_width() + 2 * padding_x,
        exit_text.get_height() + 2 * padding_y
    )
    play_again_button = pygame.Rect(
        (WIDTH - play_again_text.get_width()) / 2 - padding_x,
        HEIGHT * 0.55,
        play_again_text.get_width() + 2 * padding_x,
        play_again_text.get_height() + 2 * padding_y
    )

    mouse_pos = pygame.mouse.get_pos()

    # Check hover for both buttons
    exit_hover = is_hovering(mouse_pos, exit_button)
    play_again_hover = is_hovering(mouse_pos, play_again_button)

    # Expand buttons when hovered
    if exit_hover:
        exit_button.inflate_ip(10, 10)
    if play_again_hover:
        play_again_button.inflate_ip(10, 10)

    # Draw Exit button
    exit_color = SOFT_YELLOW if exit_hover else BORDER_COLOR
    pygame.draw.rect(screen, exit_color, exit_button, 5)  # Border only
    screen.blit(exit_text,
                (exit_button.centerx - exit_text.get_width() / 2,
                 exit_button.centery - exit_text.get_height() / 2))

    # Draw Play Again button
    play_again_color = SOFT_YELLOW if play_again_hover else BORDER_COLOR
    pygame.draw.rect(screen, play_again_color, play_again_button, 5)  # Border only
    screen.blit(play_again_text,
                (play_again_button.centerx - play_again_text.get_width() / 2,
                 play_again_button.centery - play_again_text.get_height() / 2))

    return exit_button, play_again_button

def show_game_over_screen():
    while True:
        screen.fill(DARKER_GRAY)
        # Display "GAME OVER" text
        game_over_text = title_font.render("GAME OVER", True, SOFT_YELLOW)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT * 0.3))

        # Draw the Exit and Play Again buttons with hover effect
        exit_button, play_again_button = draw_exit_and_play_again_buttons()

        # Check hover effect and expand the buttons
        mouse_pos = pygame.mouse.get_pos()

        # Expand buttons when hovering
        if is_hovering(mouse_pos, exit_button):
            exit_button.inflate_ip(10, 10)
        if is_hovering(mouse_pos, play_again_button):
            play_again_button.inflate_ip(10, 10)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovering(mouse_pos, exit_button):
                    pygame.quit()
                    sys.exit()
                if is_hovering(mouse_pos, play_again_button):
                    reset_board()
                    main()  # Restart the game

###################################################################

# Game mode selection
def main():
    # Reset button states to avoid spazzing out when returning to the menu
    button_states['single_player_hover'] = False
    button_states['two_player_hover'] = False
    button_states['single_player_clicked'] = False
    button_states['two_player_clicked'] = False
    button_states['pulsate_timer'] = 2

    running = True

    while running:
        screen.fill(DARKER_GRAY)

        # Add title
        title_text = title_font.render("Tic Tac Toe", True, SOFT_YELLOW)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT * 0.1))

        # Add subtitle
        subtitle_font = pygame.font.Font(None, int(HEIGHT * 0.05))  # Create a smaller font for the subtitle
        subtitle_text = subtitle_font.render("Try your luck in single player versus Matt!", True, SOFT_YELLOW)
        subsubtitle_text = subtitle_font.render("100 bucks says Matt will never let you win.", True, SOFT_YELLOW)
        screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT * 0.2))
        screen.blit(subsubtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, HEIGHT * 0.25))

        # Define button rectangles with padding
        single_player_button, two_player_button = draw_buttons()

        # Handle mouse hover and click events
        mouse_pos = pygame.mouse.get_pos()

        button_states['single_player_hover'] = is_hovering(mouse_pos, single_player_button)
        button_states['two_player_hover'] = is_hovering(mouse_pos, two_player_button)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovering(mouse_pos, single_player_button):
                    button_states['single_player_clicked'] = True
                    button_states['pulsate_timer'] = 0
                    single_player_mode('X', 'O')  # Start single-player mode
                    button_states['single_player_clicked'] = False
                elif is_hovering(mouse_pos, two_player_button):
                    button_states['two_player_clicked'] = True
                    button_states['pulsate_timer'] = 0
                    two_player_mode('X', 'O')  # Start two-player mode
                    button_states['two_player_clicked'] = False

    pygame.quit()


if __name__ == '__main__':
    main()
