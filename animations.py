import pygame
import random

def load_images(name, state, number):
    if number == 0:
        image = "Animations/" + name + "_" + state + ".png"
        number = 0
    else:
        image = "Animations/" + name + "_" + state + "_" + str(number) + ".png"
        if number == 2:
            number = 1
        else:
            number = 2
    return image, number

# Frequency is the maximum chance an object has of appearing. It must be over 2 if you want any objects to appear.
def generate_landscape(screen, landscape_type, maxobs, frequency, all_pos, object_list, object_count, create):
    image = pygame.image.load(landscape_type).convert_alpha()
    image.set_colorkey((255, 255, 255))
    maxobs += len(object_list) + 1

    # Draw images
    if create:
        for i in range(len(object_list) + 1, maxobs):
            appearance = random.randint(0, frequency)
            if appearance > 1:
                object_list[object_count] = 1280 + random.randint(0, 6000)
                screen.blit(image, (object_list[object_count],570))
                # Give the object a number and an x coordinate.
                object_count += 1

    # Update images
    for i in range(0, object_count):
        screen.blit(image, (object_list[i] + all_pos, 570))
    return object_list, object_count

def draw_health(health, screen):
    pygame.draw.rect(screen, (200,200,200), (48, 48, 204, 44))
    pygame.draw.rect(screen, (255,0,0), (50, 50, health * 2, 40))

# Distance is a list with a minimum value and a maximum value.
def generate_enemies(Enemy, enemy, enemy_group, enemy_count, distance, all_pos,create):
    if create:
        for i in range(0, enemy_count):
            distance_int = random.randint(distance[0], distance[1])
            enemy[i] = Enemy((0,0,0),0,0,distance_int+1280,568)
            enemy_group.add(enemy[i])
    for i in range(0, len(enemy)):
        enemy[i].x += all_pos
        enemy[i].draw()
        enemy[i].x -= all_pos
    return enemy, enemy_group