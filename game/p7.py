import time
import pygame
import random
# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700
GRID_SIZE = 4
CELL_SIZE = 150
MOLE_SIZE = 100
GRID_SPACING = 10
BACKGROUND_COLOR = (0, 128, 0)
HOLE_COLOR = (139, 69, 19)
FPS = 30
MOLE_TIME = 1
GAME_TIME = 20

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack-a-Mole")

pygame.mixer.init()

# Load images
PLAYER_MOLE_IMAGE_PATH = 'mole1.png'
AI_MOLE_IMAGE_PATH = 'mole2.png'
HAMMER_IMAGE_PATH = 'hammer.png'
player_mole_image = pygame.image.load(PLAYER_MOLE_IMAGE_PATH)
player_mole_image = pygame.transform.scale(player_mole_image, (MOLE_SIZE, MOLE_SIZE))
ai_mole_image = pygame.image.load(AI_MOLE_IMAGE_PATH)
ai_mole_image = pygame.transform.scale(ai_mole_image, (MOLE_SIZE, MOLE_SIZE))
hammer_image = pygame.image.load(HAMMER_IMAGE_PATH)
hammer_image = pygame.transform.scale(hammer_image, (50, 50))
GOLDEN_MOLE_IMAGE_PATH = 'golden_mole.png'  # Replace with the actual image path
golden_mole_image = pygame.image.load(GOLDEN_MOLE_IMAGE_PATH)
golden_mole_image = pygame.transform.scale(golden_mole_image, (MOLE_SIZE, MOLE_SIZE))

# Load sound effects
hit_sound = pygame.mixer.Sound('sound-1-167181.mp3')  # Replace with your sound file
ai_hit_sound = pygame.mixer.Sound('sound-1-167181.mp3')  # Replace with your sound file

# Font
font = pygame.font.SysFont('arial', 36)
hit_sound.set_volume(1.0)  # Maximum volume for hit sound
ai_hit_sound.set_volume(1.0)  # Maximum volume for AI hit sound

# Load background music
pygame.mixer.music.load('background-game-145867.mp3')  # Replace with your music file path
pygame.mixer.music.set_volume(0.2)  # Set lower volume for background music
pygame.mixer.music.play(-1, 0.0)  # Play music in a loop (-1 means looping)

# Functions
def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + GRID_SPACING)
            y = row * (CELL_SIZE + GRID_SPACING)
            pygame.draw.rect(screen, HOLE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

def draw_mole(mole_position, mole_type):
    row, col = mole_position
    x = col * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    y = row * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    if mole_type == "player":
        screen.blit(player_mole_image, (x, y))
    elif mole_type == "ai":
        screen.blit(ai_mole_image, (x, y))
    elif mole_type == "golden":
        screen.blit(golden_mole_image, (x, y))

def get_cell_from_mouse_pos(pos):
    x, y = pos
    col = x // (CELL_SIZE + GRID_SPACING)
    row = y // (CELL_SIZE + GRID_SPACING)
    return row, col

def ai_decide_hit(mole_position, ai_last_hit_time, ai_reaction_time, mole_visible):
    current_time = time.time()
    if mole_visible and (current_time - ai_last_hit_time >= ai_reaction_time):
        return True
    return False

def draw_hit_effect(mole_position):
    row, col = mole_position
    x = col * (CELL_SIZE + GRID_SPACING)
    y = row * (CELL_SIZE + GRID_SPACING)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))  # Red flash for hit
    
def play_game():
    clock = pygame.time.Clock()
    player_score = 0
    ai_score = 0
    last_mole_time = 0
    mole_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    mole_visible = False
    start_time = time.time()

    pygame.mouse.set_visible(False)

    ai_last_hit_time = 0
    ai_reaction_time = random.uniform(0.5, 1.5)

    player_moles_appeared = 0
    ai_moles_appeared = 0
    max_moles = 20

    # Golden mole position and appearance
    golden_mole_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    golden_mole_appeared = False  # Ensure it appears only once

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid()

        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = GAME_TIME - elapsed_time

        if remaining_time <= 0:
            running = False

        if player_moles_appeared + ai_moles_appeared >= max_moles:
            mole_visible = False

        if current_time - last_mole_time > MOLE_TIME and player_moles_appeared + ai_moles_appeared < max_moles:
            mole_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

            # Check if it's the 10th second for golden mole appearance
            if 9.5 <= elapsed_time <= 10.5 and not golden_mole_appeared:
                mole_type = "golden"
                golden_mole_position = mole_position
                golden_mole_appeared = True
                mole_visible = True
                last_mole_time = current_time
            else:
                if player_moles_appeared == ai_moles_appeared:
                    mole_type = random.choice(["player", "ai"])
                elif player_moles_appeared > ai_moles_appeared:
                    mole_type = "ai"
                else:
                    mole_type = "player"

                # Update mole counts
                if mole_type == "player":
                    player_moles_appeared += 1
                elif mole_type == "ai":
                    ai_moles_appeared += 1

                last_mole_time = current_time
                mole_visible = True
                ai_last_hit_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mole_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_cell = get_cell_from_mouse_pos(mouse_pos)
                    if clicked_cell == mole_position:
                        if mole_type == "player":
                            player_score += 1
                            hit_sound.play()  # Play sound for player hit
                        elif mole_type == "ai":
                            player_score -= 1
                            ai_hit_sound.play()  # Play sound for AI hit
                        elif mole_type == "golden":  # Golden mole bonus points
                            player_score += 3
                            hit_sound.play()  # Play sound for golden mole hit
                        mole_visible = False
                    draw_hit_effect(mole_position)
                    pygame.display.flip()  # Update display to show the hit effect
                    pygame.time.wait(100)  # Show the effect briefly (100ms)
                    mole_visible = False

        # AI decision to hit
        if mole_visible and mole_type == "ai":
            ai_reaction_time = random.uniform(0.5, 1.5)
            if ai_decide_hit(mole_position, ai_last_hit_time, ai_reaction_time, mole_visible):
                if mole_type == "ai":
                    ai_score += 1
                elif mole_type == "golden":  # AI golden mole hit
                    ai_score += 3
                ai_last_hit_time = time.time()
                mole_visible = False
                ai_hit_sound.play()  # Play sound for AI hit
                draw_hit_effect(mole_position)
                pygame.display.flip()  # Update display to show the hit effect
                pygame.time.wait(100)  # Show the effect briefly (100ms)

        # Draw the moles
        if mole_visible:
            if mole_type == "golden":
                draw_mole(golden_mole_position, "golden")  # Draw golden mole
            else:
                draw_mole(mole_position, mole_type)

        # Display remaining time
        time_text = font.render(f"Time: {int(remaining_time)}s", True, (0, 0, 0))
        screen.blit(time_text, (400, SCREEN_HEIGHT - 50))

        # Display scores
        score_text = font.render(f"My Score: {player_score}", True, (0, 0, 0))
        ai_score_text = font.render(f"AI Score: {ai_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, SCREEN_HEIGHT - 50))
        screen.blit(ai_score_text, (200, SCREEN_HEIGHT - 50))

        # Draw the hammer cursor
        mouse_pos = pygame.mouse.get_pos()
        hammer_rect = hammer_image.get_rect(center=mouse_pos)
        screen.blit(hammer_image, hammer_rect.topleft)

        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    screen.fill(BACKGROUND_COLOR)
    game_over_text = font.render("Game Over!", True, (0, 0, 0))
    final_score_text = font.render(f"Final Score: {player_score} (Player) vs {ai_score} (AI)", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Determine and display the winner
    if player_score > ai_score:
        winner_text = font.render("You win!", True, (0, 0, 0))
    elif player_score < ai_score:
        winner_text = font.render("AI wins!", True, (0, 0, 0))
    else:
        winner_text = font.render("It's a tie!", True, (0, 0, 0))

    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.time.wait(3000)

    # Ask if the player wants to play again
    return_to_home = False
    while not return_to_home:
        screen.fill(BACKGROUND_COLOR)
        play_again_text = font.render("Press R to Play Again or ESC to Exit", True, (255, 255, 255))
        screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Play again
                    return_to_home = True
                    play_game()  # Restart the game
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    pygame.quit()
                    return

def show_home_page():
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Whack-a-Mole", True, (255, 255, 255))
        start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
        exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Ensure proper program exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start the game
                    play_game()
                elif event.key == pygame.K_ESCAPE:  # Exit the game
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    show_home_page()