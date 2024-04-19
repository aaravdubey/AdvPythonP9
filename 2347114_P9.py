import pygame
import random

pygame.init()

WIN_WIDTH, WIN_HEIGHT = 800, 600
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Bombing Jet Game")

bg_image = pygame.image.load("background.jpg").convert()
jet_image = pygame.image.load("jet.png").convert_alpha()
bomb_image = pygame.image.load("bomb.png").convert_alpha()
explosion_image = pygame.image.load("explosion.png").convert_alpha()
building_image = pygame.image.load("house.png").convert_alpha()

bg_image = pygame.transform.scale(bg_image, (800, 600))
jet_image = pygame.transform.scale(jet_image, (300, 100))
bomb_image = pygame.transform.scale(bomb_image, (60, 60))
building_image = pygame.transform.scale(building_image, (300, 270))
explosion_image = pygame.transform.scale(explosion_image, (340, 200))

jet_pos_x = WIN_WIDTH // 2 - 50
jet_pos_y = 50
jet_speed = 18
bomb_pos_x = 0
bomb_pos_y = 0
bomb_speed = 10
bomb_dropped = False
explosion_pos_x = 0
explosion_pos_y = 0
explosion_timer = 0
score = 0
buildings = []

def generate_buildings():
    global buildings
    buildings = []
    for _ in range(random.randint(2, 3)):
        building_x = random.randint(50, WIN_WIDTH - 250)
        building_y = WIN_HEIGHT - 250
        buildings.append((building_x, building_y))


generate_buildings()

running = True

while running:
    window.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bomb_dropped:
                bomb_pos_x = jet_pos_x + 50
                bomb_pos_y = jet_pos_y + 100
                bomb_dropped = True

    jet_pos_x += jet_speed

    if jet_pos_x > WIN_WIDTH:
        jet_pos_x = -jet_image.get_width()

    if bomb_dropped:
        bomb_pos_y += bomb_speed
        if bomb_pos_y > WIN_HEIGHT:
            bomb_dropped = False

    for building_x, building_y in buildings:
        if 200 < bomb_pos_y < 400:
            if building_x < bomb_pos_x < building_x + 200 and building_y < bomb_pos_y < building_y + 200:
                explosion_pos_x = bomb_pos_x
                explosion_pos_y = bomb_pos_y
                explosion_timer = 30
                bomb_dropped = False
                score += 1
                generate_buildings()

    window.blit(jet_image, (jet_pos_x, jet_pos_y))

    if bomb_dropped:
        window.blit(bomb_image, (bomb_pos_x, bomb_pos_y))

    if explosion_timer > 0:
        window.blit(explosion_image, (explosion_pos_x, explosion_pos_y))
        explosion_timer -= 1

    for building_x, building_y in buildings:
        window.blit(building_image, (building_x, building_y))

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (700, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(30)

pygame.quit()
