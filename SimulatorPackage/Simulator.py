import sys
import pygame
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from SimulatorPackage.Vehicle import Vehicle
from SimulatorPackage.Light import Light

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Braitenberg vehicle simulation")
for e in pygame.event.get():
    pygame.key.set_repeat(50, 20)
clock = pygame.time.Clock()

white = 240, 240, 240
background = pygame.Surface(screen.get_size())
background = background.convert(background)
background.fill(white)

iterations = 300
myfont = pygame.font.SysFont('monospace', 12)
v1 = Vehicle(screen, [100, 100], 180)
light = Light([400, 400])
all_sprites = pygame.sprite.RenderPlain(v1, light)


def show_sensors_motors(vehicle):
    bearing = vehicle.bearing[-1]
    radius = vehicle.R + 5

    direction_x = (vehicle.pos[-1][0] - math.cos(bearing) * radius) + math.sin(bearing) * radius / 2
    direction_y = (vehicle.pos[-1][1] + math.sin(bearing) * radius) + math.cos(bearing) * radius / 2
    left_wheel = myfont.render(format(v1.wheel_l, '.1f'), 1, (0, 0, 0))
    screen.blit(left_wheel, [int(direction_x), int(direction_y)])

    direction_x = (vehicle.pos[-1][0] + math.cos(bearing) * radius) + math.sin(bearing) * radius / 2
    direction_y = (vehicle.pos[-1][1] - math.sin(bearing) * radius) + math.cos(bearing) * radius / 2
    right_wheel = myfont.render(format(v1.wheel_r, '.1f'), 1, (0, 0, 0))
    screen.blit(right_wheel, [int(direction_x), int(direction_y)])

    direction_x = (vehicle.pos[-1][0] - math.cos(bearing) * radius) - math.sin(bearing) * radius
    direction_y = (vehicle.pos[-1][1] + math.sin(bearing) * radius) - math.cos(bearing) * radius
    left_sensor = myfont.render(format(v1.sensor_left[-1], '.2f'), 1, (100, 100, 0))
    screen.blit(left_sensor, [int(direction_x), int(direction_y)])

    direction_x = (vehicle.pos[-1][0] + math.cos(bearing) * radius) - math.sin(bearing) * radius
    direction_y = (vehicle.pos[-1][1] - math.sin(bearing) * radius) - math.cos(bearing) * radius
    right_sensor = myfont.render(format(v1.sensor_right[-1], '.2f'), 1, (100, 100, 0))
    screen.blit(right_sensor, [int(direction_x), int(direction_y)])


def run():

    for t in range(1, iterations):
        clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                all_sprites.add(Vehicle(screen))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                v1._leftwheel()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                v1._rightwheel()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                v1._bothwheels()

        all_sprites.update(t, light.pos)
        screen.blit(background, (0, 0))

        all_sprites.draw(screen)

        show_sensors_motors(v1)

        pygame.display.flip()
        pygame.display.set_caption('Braitenberg vehicle simulation - ' + str(format(clock.get_fps(), '.0f')) + 'fps')

    pygame.display.quit()
    print('Finished:')

    i = range(1, iterations)

    plt.plot(i, v1.sensor_left, 'r', i, v1.sensor_right, 'y', i, v1.motor_left, 'g', i, v1.motor_right, 'b')
    red_line = mlines.Line2D([], [], color='red', label='left sensor')
    yellow_line = mlines.Line2D([], [], color='yellow', label='right sensor')
    green_line = mlines.Line2D([], [], color='green', label='left motor')
    blue_line = mlines.Line2D([], [], color='blue', label='right motor')
    plt.legend(handles=[red_line, yellow_line, green_line, blue_line])
    plt.show()