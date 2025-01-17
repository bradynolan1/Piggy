from teacher import PiggyParent
import sys
import time


class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.starting_position = 0
        self.start_time = 0
        self.LEFT_DEFAULT = 90
        self.RIGHT_DEFAULT = 90
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        self.SAFE_Distance = 250

    def getout(self):
        starting_postion = 0
        starting_position = self.getout
        # This commands robot to move away from corner and favor starting position
        self.turn_by_deg(180)
        self.deg_fwd(720)
        self.turn_to_deg(self.get_heading)
        


    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit),
                "h": ("Return to start", self.ret_to_st),
                "s": ("Slither", self.slither)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self): 
        """A higher-ordered algorithm to make your robot dance"""
        # check to see it's safe
        if not self.safe_to_dance():
            print("Not cool. Not going to dance")
            return # return closes down the method
        else:
            print("It's safe to dance!")
        for x in range(3):
            self.cupidshuffle()
        for x in range(3):
            self.jaywalk()
        for x in range(2):
            self.millyrock()
        for x in range(1):
            self.check360()
  
    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 150):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()


    
    def obstacle_count(self):
        print("I can't count how many obstacles are around me. Please give my programmer a zero.")
        """Does a 360 scan and returns the number of obstacles it sees"""
        found_something = False # trigger
        trigger_distance = 350
        count = 0
        starting_position = self.get_heading()
        self.right(primary=60, counter=-60)
        time.sleep(3)
        while abs(self.get_heading() - starting_position) <= 1:
            if self.read_distance() < 350 and not found_something:
                found_something = True
                count += 1
            elif self.read_distance() > 350 and found_something:
                found_something = False
                print("I have a clear view. Resetting my counter")
        self.stop()
        print("I found this many things: %d" % count)
        return count

    def quick_check(self):
        # three quick checks
        for ang in range(self.MIDPOINT-250, self.MIDPOINT+251, 250):
            self.servo(ang)
            if self.read_distance() < 200:
                return False
        return True

    

    def ret_to_st(self):
        starting_position = self.get_heading()
        while True:
            time.sleep(.1)
            new_ang = self.get_heading()
            if abs(starting_position-new_ang) > 20:
                self.turn_to_deg(starting_position)
                self.stop()
                print("I made it back!")

            



    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        self.corner_count = 0
        self.starting_position = self.get_heading()
        while True:
            self.servo(self.MIDPOINT)
            while self.quick_check():
                self.corner_count = 0
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.corner_count += 1
            if self.corner_count >= 4:
                current_heading = self.get_heading()
                # check if there's a path toward the exit
                self.turn_to_deg(self.starting_position)
                # but if that's not clear, face the opposite as I was when I started this mess
                if not self.quick_check():
                    self.turn_to_deg(current_heading + 180)
            else:        
                #traversal
                left_total = 0
                left_count = 0
                right_total = 0
                right_count = 0
                self.scan()
                for ang, dist in self.scan_data.items():
                    if ang < self.MIDPOINT: 
                        right_total += dist
                        right_count += 1
                    else:
                        left_total += dist
                        left_count += 1
                left_avg = left_total / left_count
                right_avg = right_total / right_count
                if left_avg > right_avg:
                    self.turn_by_deg(-45)
                else:
                    self.turn_by_deg(45)



    def slither(self):
        pass
        """ practice a smooth veer """
        #
        starting_direction = self.get_heading()
        # start driving forward
        self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd()
        #throttle down the left motor
        for power in range(self.LEFT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        #throttle up the left 
        for power in range(50, self.LEFT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.1)
        # throttle down the right
        for power in range(self.RIGHT_DEFAULT, 50, -10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        
        # throttle up the right 
        for power in range(50, self.RIGHT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.1) 
        
        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT
        
        self.turn_to_deg(self.get_heading)
        while self.get_heading() !=starting_direction:

            if self.get_heading() < starting_direction:
                print("I'm too far left!")
                right_speed -= 5

            elif self.get_heading() > starting_direction:
                print("I'm too far right!")
                left_speed -= 5
                
            self.set_motor_power(self.MOTOR_LEFT, left_speed)
            self.set_motor_power(self.MOTOR_RIGHT, right_speed)


    def path_towards_exit(self):
        self.exit_heading = self.get_heading() 
        self.turn_to_deg(self.exit_heading)
        if self.quick_check():
            return True
        else:
            self.turn_to_deg(self.get_heading)
        return False

    
    def checkdirection(self):
        self.servo(1000)
        time.sleep(.1)
        r = self.read_distance()
        self.servo(2000)
        time.sleep(.1)
        l = self.read_distance()
        if l > r:
            self.turn_by_deg(-90)
        if l < r:
            self.turn_by_deg(90)





    def cupidshuffle(self):
        """Does a quick look and moves forward. Then it turns 90 degrees to the right and does the same thing. Lastly, it turns 180 degrees and does the same thing again and then ends at its starting point."""
        for x in range(1):
            self.turn_by_deg(-90)
            time.sleep(.1)
            self.fwd(left=50, right=50)
            time.sleep(.1)
            self.stop()
        for x in range(1):
            self.turn_by_deg(-180)
            time.sleep(.1)
            self.fwd(left=50, right=50)
            time.sleep(.1)
            self.stop()   
        for x in range(1):    
            self.turn_by_deg(90)
            time.sleep(.1)
            self.servo(1000)
            time.sleep(.1)
            self.servo(2000)
            self.stop()


    def jaywalk(self):
        """Turns 90 degrees to the right and does a jay walk which repeats 4 times."""
        for x in range(4):
            self.turn_by_deg(90)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.stop()

    def millyrock(self):
        """Moves back for a second then turns left 30 degrees and then moves forward for a half of a second. Then, it moves back again and turns right 60 degrees and then moves forward for a half a seond again.  This repeats once. """
        for x in range(2):
            self.back()
            time.sleep(1)
            self.turn_by_deg(-30)
            time.sleep(1)
            self.fwd()
            time.sleep(.5)
            self.back()
            time.sleep(1)
            self.turn_by_deg(60)
            time.sleep(1)
            self.fwd()
            time.sleep(.5)
            self.back()
            time.sleep(1)
            self.stop()

    def check360(self):
        """Turns right 180 degrees then does a check.  This repeats to make it do an entire 360"""
        for x in range(2):
            self.turn_by_deg(180)
            self.servo(1000)
            time.sleep(.1)
            self.stop()

    def safe_to_dance(self):
        for x in range(4):
            for ang in range (1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True
###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  