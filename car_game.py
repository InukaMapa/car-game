import pygame
from pygame.locals import *
import random

pygame.init()


# 1. Create the window FIRST
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Game")

# colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# game settings
speed = 2

# markers size 
marker_width = 10
marker_height = 50

# road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# cordinates of Lanes
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# for animating movement of the lane makers 
lane_marker_move_y = 0


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()

        # Load image
        self.image = pygame.image.load(image_path).convert_alpha()

        # Scale image
        image_scale = 55 / self.image.get_rect().width
        new_width = int(self.image.get_rect().width * image_scale)
        new_height = int(self.image.get_rect().height * image_scale)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))


class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        super().__init__('images/Audi.png', x, y)


# player's starting coordinates
player_x = 250
player_y = 400

# create player
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

#load the ther vehicle images
image_filenames = ['pickup_truck.png' , 'semi_trailer.png' , 'taxi.png' , 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)

#sprite group for vehicles
vehicle_group =pygame.sprite.Group()

# game loop
clock = pygame.time.Clock()
fps = 120
running = True
lane_marker_move_y = 0

while running:
    clock.tick(fps)

    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.centerx > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.centerx < right_lane:
                player.rect.x += 100

    # draw background (grass)
    screen.fill(green)

    # draw road
    pygame.draw.rect(screen, gray, road)

    # draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # draw the player's car
    player_group.draw(screen)

    #add up two vehcle 
    if len(vehicle_group) < 2:

        #ensure there's enough gap between vehicle 
        add_vehicle = True 
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:

            # Select a random lane
            lane = random.choice(lanes) 

            #select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle("images/Mini_truck.png", lane, height / -2)
            vehicle_group.add(vehicle)

    # make the vehicle move 
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        #remove the vehicle once it goes off screen 
        if vehicle.rect.top >= height:
            vehicle.kill()

            # add to score
            score += 1

            #speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1

        #draw the vehicles
        vehicle_group.draw(screen)


    # update display
    pygame.display.update()

pygame.quit()22.19
