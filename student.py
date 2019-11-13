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
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        

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
                "q": ("Quit", self.quit)
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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 250):
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
            if self.read_distance() < 250 and not found_something:
                found_something = True
                count += 1
            elif self.read_distance() > 250 and found_something:
                found_something = False
                print("I have a clear view. Resetting my counter")
        self.stop()
        print("I found this many things: %d" % count)
        return count

    def quick_check(self):
        # three quick checks
        for ang in range(self.MIDPOINT-150. self.MIDPOINT+151, 150):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False
        return True


    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        while True:
            self.servo(self.MIDPOINT)
            while self.quick_check():
                self.fwd()
                time.sleep(.01)
            self.stop()    
            corner_count += 1
            if corner_count > 3:
                self.turn_by_deg(180)            
            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
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