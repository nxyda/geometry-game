import pygame
import random

pygame.init()

player_image_1 = pygame.image.load("square_1.png")
player_image_2 = pygame.image.load("square_2.png")
player_rect = player_image_1.get_rect()

obstacle_1 = pygame.image.load("obstacle_1.png")

obstacle_top = pygame.image.load("obstacle_top.png")

background_image = pygame.image.load("background.png")

screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Platformer")

background_color = (32, 26, 35)
cube_color = (141, 170, 157)
triangle_color = (251, 245, 243)
ground_color = (46, 37, 50)
text_color = (255, 255, 255)

clock = pygame.time.Clock()

obstacles = []
obstacles_top = []
score = 0
start_time = pygame.time.get_ticks()
game_over = False
counting_score = True
obstacle_timer = 0
obstacle_2_timer = 0

font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

square = {
    'height': 32,
    'jumping': True,
    'width': 32,
    'x': 100,
    'x_velocity': 0,
    'y': screen_height - 32 - 50,
    'y_velocity': 0,
    'image': player_image_1
}



obstacle_delays = [800, 1000, 1200, 1400]
obstacle_delays_1 = [800, 1000, 1200]
obstacle_delays_2 = [800, 1000]
obstacle_delays_3 = [800]

obstacle_top_delays = [800,1000, 1200,1400]
obstacle_top_delays_1 = [800,1000, 1200]
obstacle_top_delays_2 = [800, 1000]
obstacle_top_delays_3 = [800]

def generate_obstacle():
    global obstacles, score
    ob_x_coord = screen_width 
    height = 50
    obstacles.append((ob_x_coord, height))

    if score < 150:
        obstacle_delays_list = obstacle_delays
    elif score < 300:
        obstacle_delays_list = obstacle_delays_1
    elif score < 450:
        obstacle_delays_list = obstacle_delays_2
    else:
        obstacle_delays_list = obstacle_delays_3

    random_delay = random.choice(obstacle_delays_list)
    return random_delay

def move_obstacles():
    global obstacles, score
    new_obstacles = []
    for (ob_x_coord, height) in obstacles:
        ob_x_coord -= 5 + (score // 100) * 0.15
        if ob_x_coord + 20 > 0:
            new_obstacles.append((ob_x_coord, height))
    obstacles = new_obstacles

def generate_obstacles_top():
  global obstacles_top, score
  ob_x_coord = screen_width
  height_top = 125
  obstacles_top.append((ob_x_coord, height_top))
  
  if score < 150:
    obstacle_delays_list = obstacle_top_delays
  elif score < 300:
    obstacle_delays_list = obstacle_top_delays_1
  elif score < 450:
    obstacle_delays_list = obstacle_top_delays_2
  else:
    obstacle_delays_list = obstacle_top_delays_3

  random_delay = random.choice(obstacle_delays_list)
  return random_delay

def move_obstacles_top():
  global obstacles_top, score
  new_obstacles_top = []
  for (ob_x_coord, height_top) in obstacles_top:
    ob_x_coord -= 5 + (score // 100) * 0.15
    if ob_x_coord + 20 > 0:
      new_obstacles_top.append((ob_x_coord, height_top))
  obstacles_top = new_obstacles_top
  
def check_collision():
    global square, obstacles, obstacles_top, game_over
    square_rect = pygame.Rect(square['x'], square['y'], square['width'], square['height'])

    for (ob_x_coord, height) in obstacles:
        ob_rect = pygame.Rect(ob_x_coord, screen_height - height, 20, height)

        if square_rect.colliderect(ob_rect):
            game_over = True

    for (ob_x_coord, height_top) in obstacles_top:
        obstacle_top_image = pygame.image.load("obstacle_top.png")
        obstacle_top_rect = obstacle_top_image.get_rect()
        obstacle_top_rect.topleft = (ob_x_coord, screen_height - height_top)

        if square_rect.colliderect(obstacle_top_rect):
            game_over = True


def new_game():
    global obstacles, score, start_time, game_over, counting_score
    obstacles = []
    score = 0
    start_time = pygame.time.get_ticks()
    game_over = False
    counting_score = True

def calculate_score():
    global score, start_time, counting_score
    if counting_score:
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - start_time) // 100
        score = elapsed_seconds

def draw_player():
    global square, player_image_1, player_image_2

    if square['jumping'] or square['y'] < screen_height - 100:
        screen.blit(player_image_2, (square['x'], square['y']))
    else:
        screen.blit(player_image_1, (square['x'], square['y']))

def draw_obstacles():
  for (ob_x_coord, height) in obstacles:
    obstacle_image = pygame.image.load("obstacle_1.png")
    obstacle_rect = obstacle_image.get_rect()
    obstacle_rect.topleft = (ob_x_coord, screen_height - height)
    screen.blit(obstacle_image, obstacle_rect)

def draw_obstacles_top():
  for (ob_x_coord, height_top) in obstacles_top:
    obstacle_image = pygame.image.load("obstacle_top.png")
    obstacle_rect = obstacle_image.get_rect()
    obstacle_rect.topleft = (ob_x_coord, screen_height - height_top)
    screen.blit(obstacle_image, obstacle_rect)

new_game()

running = True
obstacle_delay = 0 
obstacle_top_delay = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and not square['jumping']:
        square['y_velocity'] -= 22
        square['jumping'] = True

    square['y_velocity'] += 1
    square['x'] += square['x_velocity']
    square['y'] += square['y_velocity']
    square['y_velocity'] *= 0.9

    if square['y'] > screen_height - 16 - square['height']:
        square['jumping'] = False
        square['y'] = screen_height - 16 - square['height']
        square['y_velocity'] = 0

    current_time = pygame.time.get_ticks()
    current_time_2 = pygame.time.get_ticks()
  
    if current_time - obstacle_timer > obstacle_delay:
      test = random.randint(1,2)
      if test == 1:
        obstacle_delay = generate_obstacle() 
      elif test == 2:
        obstacle_top_delay = generate_obstacles_top()
      obstacle_timer = current_time


    move_obstacles()

    move_obstacles_top()
  

    calculate_score()


    check_collision()


    screen.fill(background_color)


    pygame.draw.line(screen, ground_color, (0, screen_height - 15), (screen_width, screen_height - 15), 30)


    draw_obstacles()

    draw_obstacles_top()

  

    draw_player()


    score_text = font.render(f"Score: {score}", True, text_color)
    screen.blit(score_text, (screen_width - 150, 20))

    if game_over:
        screen.fill((0, 0, 0))
        counting_score = False
        game_over_text = game_over_font.render("GAME OVER", True, text_color)
        text = ["Game over. Press Enter to play again", "Esc to return to menu."]
        text_renders = [font.render(line, True, "white") for line in text]
        text_y = 300
        for text_render in text_renders:
            text_width = text_render.get_width()
            screen.blit(text_render, (400 - text_width // 2, text_y))
            text_y += text_render.get_height()
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2 - 50))
        screen.blit(score_text, (screen_width // 2 - 70, screen_height // 2 + 20))
        if keys[pygame.K_RETURN]:
            new_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
