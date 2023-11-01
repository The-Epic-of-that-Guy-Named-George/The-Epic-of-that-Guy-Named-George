import pygame
import easygui
import animations

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

class Character(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(character_image_name).convert_alpha()

        self.rect = self.image.get_rect().move(player_pos.x, player_pos.y)

        self.mask = pygame.mask.from_surface(self.image)

        self.draw()

    def draw(self):
        screen.blit(self.image, (player_pos.x, player_pos.y))

    # def update_image(self, new_image):
        # pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load(character_image_name)
        # self.rect = self.image.get_rect()
    # def draw(self, player_pos):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = pygame.image.load(character_image_name)
    #     self.rect = self.image.get_rect()
    #     screen.blit(self.image, (player_pos.x, player_pos.y))
class Ground(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Objects/ground.png")
        self.image.set_colorkey((255, 255, 255))

        self.rect = self.image.get_rect().move(0,670)

        self.mask = pygame.mask.from_surface(self.image)

        screen.blit(self.image, (0,670))
    # def draw(self, x, y):
    #     pygame.sprite.Sprite.__init__(self)
    #     self.image = pygame.image.load("Objects/ground.png")
    #     self.rect = self.image.get_rect()
        

while running:
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
        # elif event.type == pygame.KEYDOWN:
        pygame_events = pygame.key.get_pressed()
        if pygame_events[pygame.K_UP]:
        # if event.key == pygame.K_UP:
            player_pos.y -= 200
            state = "jumping1"
            animation_number = 2
        # if event.key == pygame.K_DOWN:
        elif pygame_events[pygame.K_DOWN]:
            state = "attack"
            animation_number = 1
        # if event.key == pygame.K_LEFT:
        elif pygame_events[pygame.K_LEFT]:
            state = "running"
            animation_number = 1
            # player_pos.x -= 1
            all_pos += 30
        # if event.key == pygame.K_RIGHT:
        elif pygame_events[pygame.K_RIGHT]:
            state = "running"
            animation_number = 1
            pygame_events = 0
            # player_pos.x += 1
            all_pos -= 30

    pygame.display.flip()

    dt = clock.tick(60) / 1000

    screen.fill((0, 100, 255))

    character = Character((0,0,0),20,20)

    # Decide the state of the character.
    if not state == "jumping1" and not state == "jumping2" and not state == "jumping3":
        character_image_name, animation_number = animations.load_images(name, state, animation_number)
        # screen.fill((255, 255, 255))
        # Character.draw(Character, player_pos)
        # screen.blit(Character.image, (player_pos.x, player_pos.y))
    elif state == "jumping2":
        # screen.fill((255, 255, 255))
        # Character.draw(Character, player_pos)
        # screen.blit(Character.image, (player_pos.x, player_pos.y))
        character_image_name = "Animations/" + name + "_jumping_2.png"
        state = "jumping3"
    elif state == "jumping3":
        # screen.fill((255, 255, 255))
        # Character.draw(Character, player_pos)
        # screen.blit(Character.image, (player_pos.x, player_pos.y))
        character_image_name = "Animations/" + name + "_jumping_2.png"
        state = "standing"
        animation_number = 0
    else:
        character_image_name = "Animations/" + name + "_jumping_1.png"
        state = "jumping2"
    # Character.draw(Character, player_pos)

    # screen.blit(character, (player_pos.x, player_pos.y))

    # screen.blit(Character.image, (player_pos.x, player_pos.y))

    # Draw the ground
    ground = Ground((0,0,0),0,0)
    scenery = pygame.sprite.Group()
    scenery.add(ground)
    object_list, object_count = animations.generate_landscape(screen, "Objects/Grass.png", 100, 3, all_pos, object_list, object_count, create)
    create = False # Really, you must only create once. It can mess things up.

    # Draw Health
    animations.draw_health(george_health, screen)
    george_health -= 0.1
    
    # Collision detection
    character_collided_with_ground = pygame.sprite.collide_mask(ground, character)
    # character_collided_with_ground = pygame.sprite.spritecollide(character, scenery, False)

    # print(character.rect, ground.rect)
    # print(character_collided_with_ground)
    # if not any(character_collided_with_ground):
    if character_collided_with_ground == None:
        player_pos.y += gravity_strength
        # print("falling")
    else:
        player_pos.y -= 1
        # print("collided")

    # if all_pos < -1280:
    #     all_pos = 0
    # elif all_pos > 0:
    #     all_pos = -1280


pygame.quit()