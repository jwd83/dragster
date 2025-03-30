import pygame
from pygame.locals import *
import math

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TRACK_LENGTH_PX = 1000
TRACK_HEIGHT_PX = 50
TRACK_COLOR = (255, 255, 255)
CAR_SIZE = 10
CAR_COLOR = (255, 0, 0)
BG_COLOR = (0, 0, 0)

# Car constants
GEAR_RATIOS = [4.3, 3.0, 2.2, 1.0, 0.8]
FINAL_DRIVE = 4.3
TIRE_DIAMETER = 22.7  # inches
TIRE_RADIUS = (TIRE_DIAMETER / 2) / 12  # convert to feet
CAR_WEIGHT = 2000  # lbs
MASS = CAR_WEIGHT / 32.174  # convert to slugs
MAX_RPM = 7400
MIN_RPM = 2000
QUARTER_MILE_FEET = 1320  # 1/4 mile in feet


def calculate_rpm(speed_fps, gear):
    if gear < 1 or gear > 5 or speed_fps == 0:
        return 0
    gear_ratio = GEAR_RATIOS[gear - 1]
    circumference = 2 * math.pi * TIRE_RADIUS
    wheel_rpm = (speed_fps * 60) / circumference
    return wheel_rpm * gear_ratio * FINAL_DRIVE


def calculate_torque(rpm):
    if rpm < MIN_RPM:
        return 108.0
    elif rpm > MAX_RPM:
        return (150 * 5252) / MAX_RPM  # ~106.46 ft-lb
    else:
        x = (rpm - MIN_RPM) / (MAX_RPM - MIN_RPM)
        return 108.0 - x * (108.0 - 106.46)


def calculate_force(torque, gear):
    if gear < 1 or gear > 5:
        return 0.0
    gear_ratio = GEAR_RATIOS[gear - 1]
    return (torque * gear_ratio * FINAL_DRIVE) / TIRE_RADIUS


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Drag Racing Simulator")
    clock = pygame.time.Clock()

    track_x = (SCREEN_WIDTH - TRACK_LENGTH_PX) // 2
    track_y = (SCREEN_HEIGHT - TRACK_HEIGHT_PX) // 2

    position_ft = 0.0
    speed_fps = 0.0
    current_gear = 1
    throttle = False

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    throttle = True
                elif event.key == K_LEFT and current_gear > 1:
                    current_gear -= 1
                elif event.key == K_RIGHT and current_gear < 5:
                    current_gear += 1
            elif event.type == KEYUP and event.key == K_UP:
                throttle = False

        if throttle:
            rpm = calculate_rpm(speed_fps, current_gear)
            rpm = max(0, min(rpm, MAX_RPM))
            torque = calculate_torque(rpm)
            force = calculate_force(torque, current_gear)
            speed_fps += (force / MASS) * dt

        position_ft += speed_fps * dt
        if position_ft >= QUARTER_MILE_FEET:
            print("Race Over!")
            running = False

        screen.fill(BG_COLOR)
        pygame.draw.rect(
            screen, TRACK_COLOR, (track_x, track_y, TRACK_LENGTH_PX, TRACK_HEIGHT_PX)
        )

        car_x = track_x + (position_ft / QUARTER_MILE_FEET) * TRACK_LENGTH_PX
        car_y = track_y + (TRACK_HEIGHT_PX - CAR_SIZE) // 2
        pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, CAR_SIZE, CAR_SIZE))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
