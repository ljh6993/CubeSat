#!/usr/bin/env python


import rospy
from std_msgs.msg import UInt8
from geometry_msgs.msg import Vector3
import ephem
import datetime
from math import degrees as deg


def callback0(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data)


def listener():
    rospy.init_node('mainmoon', anonymous=True)

    rospy.Subscriber('GPSlocation', Vector3, callback0)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def talker():
    rospy.init_node('moonros', anonymous=True)  # node name talker
    pub = rospy.Publisher('motor_1', UInt8, queue_size=10)
    pub1 = rospy.Publisher('motor_2', UInt8, queue_size=10)

    rate = rospy.Rate(10)  # 10hz send
    while not rospy.is_shutdown():  # test if shutdown

        now = datetime.datetime.utcnow()
        home = ephem.Observer()
        home.date = now
        home.lat, home.lon = '42.593948', '-81.174415'
        moon = ephem.Moon()
        moon.compute(home)
        moon_azimuth = round(deg(float(moon.az)), 1)
        moon_altitude = round(deg(float(moon.alt)), 1)
        print("%s" % (now))
        print("%s %s" % (moon_altitude, moon_azimuth))

        motor_1 = moon_altitude * 160  # for gearbox
        motor_2 = moon_azimuth
        pub.publish(motor_1)
        pub1.publish(motor_2)

    rate.sleep()


if __name__ == '__main__':

    listener()
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
