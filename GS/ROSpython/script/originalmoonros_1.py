class driver:
    def __init__(self):
        # init ros
        rospy.init_node('moonros', anonymous=True)
        rospy.Subscriber('GPSlocation', Vector3, self.callback0)
        self.ser = serial.Serial('/dev/ttyACM1', 9600)
        self.get_arduino_message()

    # get cmd_vel message, and get linear velocity and angular velocity
    def callback0(self, data):
        rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)

    # translate and send to arduino
    def send_cmd_to_arduino(self, x, angular):
        now = datetime.datetime.utcnow()
        home = ephem.Observer()
        home.date = now
        home.lat, home.lon = '42.593948', '-81.174415'
        moon = ephem.Moon()
        moon.compute(home)
        moon_azimuth = round(deg(float(moon.az)), 0)
        moon_altitude = round(deg(float(moon.alt)), 0)

        motor_1 = moon_altitude  # for gearbox
        motor_2 = moon_azimuth
        hello_str = "azal%s  %s" % (moon_azimuth, moon_altitude)
        rospy.loginfo(hello_str)
        # send by serial

    # receive serial text from arduino and publish it to '/arduino' message
    def get_arduino_message(self):
        #pub = rospy.Publisher('arduino', String, queue_size=10)
        pub = rospy.Publisher('motor_1', Int16, queue_size=10)
        pub1 = rospy.Publisher('motor_2', Int16, queue_size=10)
        r = rospy.Rate(0.5)
        while not rospy.is_shutdown():

            pub.publish(send_cmd_to_arduino.motor_1)
            pub1.publish(motor_2)
            r.sleep()

if __name__ == '__main__':
    try:
        d = driver()
    except rospy.ROSInterruptException:
        pass