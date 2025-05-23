# todo
#
# draw sprite instead of red box
# draw a better looking track
# add engine sfx

import pygame
from pygame.locals import *
import math
import time
# import winsound

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TRACK_LENGTH_PX = 1000
TRACK_HEIGHT_PX = 50
TRACK_COLOR = (255, 255, 255)
CAR_SIZE = 10
CAR_COLOR = (255, 0, 0)
BG_COLOR = (0, 180, 0)

# Car constants
GEAR_RATIOS = [3.587, 2.022, 1.384, 1.0, 0.861]
FINAL_DRIVE = 4.3
TIRE_DIAMETER = 22.7  # inches
TIRE_RADIUS = (TIRE_DIAMETER / 2) / 12  # convert to feet
CAR_WEIGHT = 2000  # lbs
MASS = CAR_WEIGHT / 32.174  # convert to slugs
MAX_RPM = 7400
MIN_RPM = 2000
QUARTER_MILE_FEET = 1320  # 1/4 mile in feet
TIME_START = time.time()


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
        return 0
        # return (150 * 5252) / MAX_RPM  # ~106.46 ft-lb
    else:
        x = (rpm - MIN_RPM) / (MAX_RPM - MIN_RPM)
        return 108.0 - x * (108.0 - 106.46)


def calculate_force(torque, gear):
    if gear < 1 or gear > 5:
        return 0.0
    gear_ratio = GEAR_RATIOS[gear - 1]
    return (torque * gear_ratio * FINAL_DRIVE) / TIRE_RADIUS


def main():
    global TIME_START

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Drag Racing Simulator")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    car_image = pygame.image.load("car.png").convert_alpha()
    car_width = car_image.get_width()
    track_image = pygame.image.load("track.png").convert_alpha()

    sound_enabled = False

    track_x = (SCREEN_WIDTH - TRACK_LENGTH_PX) // 2
    track_y = (SCREEN_HEIGHT - TRACK_HEIGHT_PX) // 2

    # Initialize state
    STATE_STAGING = 1
    STATE_RACING = 2
    STATE_RESULTS = 3
    state = STATE_STAGING
    state_sub_staging = 0

    # Initialize game variables
    reaction_time: float = 0.0
    quarter_mile_time: float = 0.0
    quarter_mile_speed: float = 0.0

    position_ft = 0.0
    speed_fps = 0.0
    position_ft = 0.0
    current_gear = 0
    throttle = False
    running = True
    rpm = 0
    speed_mph = 0.0
    torque = 0
    power = 0
    force = 0
    car_y = 250
    car_x = track_x - car_width

    while running:
        dt = clock.tick(60) / 1000.0

        # draw the track
        screen.blit(track_image)

        # screen.fill(BG_COLOR)
        # pygame.draw.rect(
        #     screen,
        #     TRACK_COLOR,
        #     (track_x, track_y, TRACK_LENGTH_PX, TRACK_HEIGHT_PX),
        # )

        held = pygame.key.get_pressed()
        if held[K_ESCAPE]:
            running = False
        throttle = held[K_UP]
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:

                if event.key == K_s:
                    sound_enabled = not sound_enabled

                if state == STATE_RESULTS:
                    if event.key == K_RETURN:
                        state = STATE_STAGING

                elif state == STATE_STAGING:

                    if event.key == K_RIGHT:
                        state = STATE_RACING
                        TIME_START = time.time()

                elif state == STATE_RACING:

                    if event.type == KEYDOWN:
                        if event.key == K_UP:
                            throttle = True
                            if reaction_time == 0.0:
                                reaction_time = time.time() - TIME_START
                        elif event.key == K_LEFT and current_gear > 1:
                            current_gear -= 1
                        elif event.key == K_RIGHT and current_gear < 5:
                            current_gear += 1
                    elif event.type == KEYUP and event.key == K_UP:
                        throttle = False

        # end of event handling

        # update and draw the scene based on state

        if state == STATE_RESULTS:
            current_gear = 1
            state_sub_staging = 0
            throttle = False
            text_color = (0, 0, 0)
            rpm = 0
            results = [
                f"Reaction Time: {reaction_time:.3f} seconds",
                f"Quarter Mile Time: {quarter_mile_time:.3f} seconds",
                f"Quarter Mile Speed: {quarter_mile_speed:.3f} mph",
                f"Travel Time: {quarter_mile_time - reaction_time:.3f} seconds",
                "Press [enter] to restart",
            ]
            text_y = SCREEN_HEIGHT // 2 - 50
            text_x = 800
            for text in results:
                text_surface = font.render(text, True, text_color)
                screen.blit(text_surface, (text_x, text_y))
                text_y += 30

        elif state == STATE_STAGING:

            if state_sub_staging == 0:
                state_sub_staging = 1

                # reset variables
                reaction_time: float = 0.0
                quarter_mile_time: float = 0.0
                quarter_mile_speed: float = 0.0

                position_ft = 0.0
                speed_fps = 0.0
                position_ft = 0.0
                current_gear = 1
                throttle = False
                running = True
                rpm = 0
                speed_mph = 0.0

            messages = [
                "Press [->] to start and upshift",
                "Press [UP] to throttle",
                "Press [<-] to downshift",
            ]
            text_color = (0, 0, 0)
            text_x = 800
            text_y = SCREEN_HEIGHT // 2 - 50
            for text in messages:
                text_surface = font.render(text, True, text_color)
                screen.blit(text_surface, (text_x, text_y))
                text_y += 30

        elif state == STATE_RACING:

            # Physics calculations
            rpm = calculate_rpm(speed_fps, current_gear)
            # rpm = max(0, min(rpm, MAX_RPM))

            if throttle:
                torque = calculate_torque(rpm)
                power = torque * max(2000, rpm) / 5252
                force = calculate_force(power, current_gear)
                # force = calculate_force(torque, current_gear)
                speed_fps += (force / MASS) * dt

            position_ft += speed_fps * dt
            if position_ft >= QUARTER_MILE_FEET:
                state = STATE_RESULTS
                quarter_mile_time = time.time() - TIME_START
                quarter_mile_speed = speed_fps * 0.681818  # fps to mph

                print(f"Race Over! Time: {time.time() - TIME_START:.3f} seconds")
                # running = False

            # Convert speed to MPH
            speed_mph = speed_fps * 0.681818  # fps to mph

            # Draw car
            car_x = (
                track_x
                + (position_ft / QUARTER_MILE_FEET) * TRACK_LENGTH_PX
                - car_width
            )
        screen.blit(car_image, (car_x, car_y))
        # pygame.draw.rect(screen, CAR_COLOR, (car_x, car_y, CAR_SIZE, CAR_SIZE))

        # draw the game
        # Draw text readouts
        text_y = 360
        text_x = 420
        readouts = [
            f"RPM: {int(rpm)}",
            f"Speed: {speed_mph:.1f} mph",
            f"Gear: {current_gear}",
            f"Throttle: {'ON' if throttle else 'OFF'}",
            f"Torque: {torque:.2f} ft-lb",
            f"Power: {power:.2f} hp",
            f"Force: {force:.2f} lbs",
        ]

        for text in readouts:
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (text_x, text_y))
            text_y += 30

        # draw rpm and speed gauges
        gauge_x = 200
        gauge_y = 360
        gauge_width = 200
        display_rpm = max(rpm, 1000)

        if sound_enabled:
            pass
            # winsound.Beep(int(display_rpm), 1)
        pygame.draw.rect(screen, (255, 255, 0), (gauge_x, gauge_y, gauge_width, 20))
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (gauge_x, gauge_y, int(rpm / MAX_RPM * gauge_width), 20),
        )

        gauge_y += 30

        pygame.draw.rect(screen, (255, 255, 0), (gauge_x, gauge_y, gauge_width, 20))
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (gauge_x, gauge_y, int(speed_mph / 200 * gauge_width), 20),
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
