#!/usr/bin python3
from collections import OrderedDict
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
        self.RIGHT_DEFAULT = 83.5
        self.SAFE_DISTANCE = 300
        self.CLOSE_DISTANCE = 35
        self.MIDPOINT = 1400  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
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
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
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
        if not self.safe_to_dance():
            return False #shut the dance down
        self.salsa_shuffle()
        self.headrager_shuffle()
        self.poplock_shuffle()
        self.swerving_shuffle()
        self.coolwalk_shuffle()

    
    def salsa_shuffle(self):
        """first dance of 5"""
        for x in range(8):
            self.back()
            time.sleep(.5)
            self.turn_by_deg(180)
            self.turn_by_deg(180)
            time.sleep(.5)
            self.fwd(left=100, right=100)
            time.sleep(1)
            self.stop()
    
    def headrager_shuffle(self):
        """robot moves his head back and fourth like he is rageing"""
        for x in range(8):
            self.servo(1000)
            self.turn_by_deg(180)
            self.servo(2000)
            self.turn_by_deg(180)
            self.servo(1000)
            self.turn_by_deg(180)
            self.turn_by_deg(180)
            self.servo(2000)

    def poplock_shuffle(self):
        """robot moves around like he is poping and locking it"""
        for x in range(8):
            self.fwd()
            time.sleep(.2) 
            self.right()
            time.sleep(.2)
            self.fwd()
            time.sleep(.2)
            self.left()
            time.sleep(.2)
            self.back()
            time.sleep(.2)
            self.stop()
            time.sleep(.2)
    
    def swerving_shuffle(self):
        """new dance makes the robot swerve around"""
        for x in range(8):
            self.right(primary=70, counter=30)
            time.sleep(1)
            self.left(primary=70, counter=30)
            time.sleep(1)
            self.servo(1000)
            self.servo(2000)
            time.sleep(.5)
        self.stop()
            
            
    def coolwalk_shuffle(self):
        """this dance makes the robot walk like his cool"""
        for x in range(8): 
            self.fwd()   
            self.right(primary=70, counter=30)
            time.sleep(.5)
            self.fwd()
            self.left(primary=70, counter=30)
            time.sleep(.5)
            self.back()
            self.stop()
        




    


        
            # call other dance moves

    def safe_to_dance(self):
        """ Does a 360 distance check and returns true if safe """
        #check for all fail/early-termanation conditions 
        for _ in range(4):
            if self.read_distance() < 300:
                print("not safe to dance!") 
                return False
            else:
                self.turn_by_deg(90)
        #after all check have been done. We deduce its safe 
        print("safe to dance, brah!")
        return True 

    def shake(self):
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left

    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()
        # sort the scan data for easier analysis
        self.scan_data = OrderedDict(sorted(self.scan_data.items()))

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        # print the scan of the area in front of the robot 
        self.scan()
        # Figure out how many obstacles there were
        see_an_object = False
        count = 0 

 
        for angle in self.scan_data:
            dist = self.scan_data[angle]
            if dist < self.SAFE_DISTANCE and not see_an_object:
                see_an_object = Truecount += 1
                print("~~~ I SEE SOMTHING!!! ~~~")
            elif dist > self.SAFE_DISTANCE and see_an_object:
                see_an_object = False 
                print("I guess the object ended")

                
            print("ANGLE:  %d  |  DIST: %d" % (angle, dist))
        print("\nI saw %d objects" % count)

          

        
            



    def quick_check(self):
        """ Moves servo to three angles and performs a distance check """
        #loop three times and move servo 
        for ang in range(self.MIDPOINT - 100, self.MIDPOINT+101, 100):
            self.servo(ang)
            time.sleep(.05)
            if self.read_distance() < self.SAFE_DISTANCE:
                return False
        #if the three part check dident freak out
        return True


    def turn_until_clear(self):
        """ Rotate right until no obstcale is seen """
        print("-----turning until clear----")
        # make sure were looking straight
        self.servo(self.MIDPOINT)
        # so long as we see somthing close, keep turning left
        while self.read_distance() < self.SAFE_DISTANCE:
            self.left(primary=40, counter=-40)
            time.sleep(.05)
        # stop motion before we end the motion
        self.stop




    def nav(self):
        """ Auto-pilot program """
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        

        while True:
            if not self.quick_check():
                self.stop()  
                self.turn_until_clear()
            else:
                self.fwd()
        
        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


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
