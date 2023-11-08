import pygame
import easygui
import animations
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

animation_number = 0
state = "standing"
name = "George"
character_image_name = "Animations/" + name + "_" + state + ".png"
gravity_strength = 3
reset_animation = 0
all_pos = -1280
object_list = {}
create = True
object_count = 0
george_health = 100
enemy = {}
enemy_group = pygame.sprite.Group()
moved = 0

class Character(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(character_image_name).convert_alpha()

        self.rect = self.image.get_rect().move(player_pos.x, player_pos.y)

        self.mask = pygame.mask.from_surface(self.image)

        self.draw()

    def draw(self):
        screen.blit(self.image, (player_pos.x, player_pos.y))

class Ground(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Objects/ground.png")
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect().move(0,670)

        self.mask = pygame.mask.from_surface(self.image)

        screen.blit(self.image, (0,670))     

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Enemies/scribblebeast.png")
        self.image.set_colorkey((255, 255, 255))

        self.x = x
        self.y = y

        self.rect = self.image.get_rect().move(self.x,self.y)

        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, x, y):
        screen.blit(self.image, (x,y))     


while running:
    moved = 0
    first_all_pos = all_pos
    pygame.display.set_caption('The Epic of that Guy Named George')
    reset_animation += 1
    if reset_animation >= dt * 200:
        reset_animation = 0
        pygame_events = 0
        animation_number = 0
        state = "standing"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == None:
            animation_number = 0
            state = "standing"
        pygame_events = pygame.key.get_pressed()
        if pygame_events[pygame.K_UP]:
            player_pos.y -= 200
            state = "jumping1"
            animation_number = 2
        elif pygame_events[pygame.K_DOWN]:
            state = "attack"
            animation_number = 1
        elif pygame_events[pygame.K_LEFT]:
            state = "running"
            animation_number = 1
            all_pos += 30
        elif pygame_events[pygame.K_RIGHT]:
            state = "running"
            animation_number = 1
            pygame_events = 0
            all_pos -= 30

    pygame.display.flip()

    dt = clock.tick(60) / 1000

    screen.fill((0, 100, 255))

    character = Character((0,0,0),20,20)

    # Decide the state of the character.
    if not state == "jumping1" and not state == "jumping2" and not state == "jumping3":
        character_image_name, animation_number = animations.load_images(name, state, animation_number)
    elif state == "jumping2":
        character_image_name = "Animations/" + name + "_jumping_2.png"
        state = "jumping3"
    elif state == "jumping3":
        character_image_name = "Animations/" + name + "_jumping_2.png"
        state = "standing"
        animation_number = 0
    else:
        character_image_name = "Animations/" + name + "_jumping_1.png"
        state = "jumping2"

    # Draw the ground
    ground = Ground((0,0,0),0,0)
    scenery = pygame.sprite.Group()
    scenery.add(ground)
    object_list, object_count = animations.generate_landscape(screen, "Objects/Grass.png", 100, 3, all_pos, object_list, object_count, create)

    # Draw Health
    animations.draw_health(george_health, screen)
    
    # Create enemies
    enemy, enemy_group = animations.generate_enemies(Enemy, enemy, enemy_group, 5, [1000,3000], all_pos, create)
    # print("enemy")
    # print(enemy)
    # print()
    create = False # Really, you must only create once. It can mess things up.

    # Collision detection
    character_collided_with_ground = pygame.sprite.collide_mask(ground, character)
    if character_collided_with_ground == None:
        player_pos.y += gravity_strength
    else:
        player_pos.y -= 1
    for i in range(0, len(enemy)):
        collided_with_enemies = pygame.sprite.collide_mask(character, enemy[i])
        # print(str(enemy[i].rect))
        # pygame.draw.rect(screen, (0,0,0), enemy[i].rect)
        if not collided_with_enemies == None:
            george_health -= 0.5#random.randint(1,5)
            # print(str(collided_with_enemies))
        else:
            if george_health < 100:
                george_health += 0.01
    moved = -(first_all_pos - all_pos)

pygame.quit()