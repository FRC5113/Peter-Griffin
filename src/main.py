# region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain = Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
B_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
FL_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
FR_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)

# Wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = (
        brain.battery.voltage(MV)
        + brain.battery.current(CurrentUnits.AMP) * 100
        + brain.timer.system_high_res()
    )
    urandom.seed(int(random))


# Set random seed
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)


# Add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# Clear the console to make sure we don't have the REPL in the console
print("\033[2J")


# endregion VEXcode Generated Robot Configuration

# Motor velocity variables
motorFR = 0
motorFL = 0


# Helper function to calculate sine with degrees
def sinDegrees(degrees):
    return math.sin(math.radians(degrees))


# KiwiDrive function to move the robot in a particular direction
def KiwiDrive(angle):
    x = angle + 180
    B_motor.set_velocity(sinDegrees(x + 120) * 100, PERCENT)
    FR_motor.set_velocity(sinDegrees(x) * 100, PERCENT)
    FL_motor.set_velocity(sinDegrees(x - 120) * 100, PERCENT)

    # Spin motors forward with calculated velocities
    FR_motor.spin(FORWARD)
    B_motor.spin(FORWARD)
    FL_motor.spin(FORWARD)


# Bump function to avoid obstacles
def Bump(angle):
    KiwiDrive(angle + 180)  # Run the robot away from the obstacle


# Main loop
while True:
    if controller_1.buttonLeft.pressing():
        Bump(0)
    elif controller_1.buttonRight.pressing():
        Bump(120)
    elif controller_1.buttonUp.pressing():
        Bump(240)
    elif controller_1.buttonDown.pressing():
        Bump(359)
    else:
        if controller_1.axis4.position() != 0:  # Spin the robot
            FR_motor.set_velocity(controller_1.axis4.position(), PERCENT)
            FL_motor.set_velocity(controller_1.axis4.position(), PERCENT)
            B_motor.set_velocity(controller_1.axis4.position(), PERCENT)

            FR_motor.spin(FORWARD)
            FL_motor.spin(FORWARD)
            B_motor.spin(FORWARD)
        else:
            if controller_1.axis1.position() != 0 or controller_1.axis2.position() != 0:
                # Calculate direction based on joystick position
                angle = math.degrees(
                    math.atan2(controller_1.axis1.position(), controller_1.axis2.position())
                )
                KiwiDrive(angle)
            else:
                # Stop all motors when no input
                FR_motor.stop()
                FL_motor.stop()
                B_motor.stop()
