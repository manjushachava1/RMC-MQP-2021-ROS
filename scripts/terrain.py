#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from nav_msgs.msg import GridCells
from geometry_msgs.msg import Point

# randomly shuffle a sequence
from random import seed
from random import shuffle
from random import choice


def terrain():
    pub_obs = rospy.Publisher('obstacle', GridCells, queue_size=10)
    pub_clr = rospy.Publisher('clear_space', GridCells, queue_size=10)
    pub_path = rospy.Publisher('path', GridCells, queue_size=10)
    rospy.init_node('terrain', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    path_len = 1
    obstacles = point_gen(5, 5, 70, path_len)
    clear_space = point_gen(5, 5, 40, path_len)
    path_points = path_gen(path_len)

    time_up = rospy.get_time() + 2
    while not rospy.is_shutdown():
        if rospy.get_time() > time_up:
            if path_len < 20:
                path_len += 1
            obstacles = point_gen(5, 5, 100, path_len)
            clear_space = point_gen(5, 5, 50, path_len)
            path_points = path_gen(path_len)
            time_up = rospy.get_time() + 1
        # setup obstacles
        obs = GridCells()
        obs.cell_width = 1
        obs.cell_height = 1
        obs.header.frame_id = 'map'
        obs.cells = obstacles
        rospy.loginfo(str(obs))
        # setup clear space
        clr = GridCells()
        clr.cell_width = 1
        clr.cell_height = 1
        clr.header.frame_id = 'map'
        clr.cells = clear_space
        # setup fake path
        path = GridCells()
        path.cell_width = 1
        path.cell_height = 1
        path.header.frame_id = 'map'
        path.cells = path_points
        # publish all
        pub_obs.publish(obs)
        pub_clr.publish(clr)
        pub_path.publish(path)
        rate.sleep()


# generates some random points, can switch out for actual info
def point_gen(x_max, y_max, n, see):
    points = []
    # seed random number generator
    seed(see)
    # prepare a sequence
    x_range = [i for i in range(x_max*2)]
    y_range = [j for j in range(y_max*2)]
    for k in range(n):
        x = choice(x_range) - x_max + .5
        y = choice(y_range) - y_max + .5
        points.append(Point(x, y, 0))
        shuffle(x_range)
        shuffle(y_range)
    return points


# generates fake path, switch out for A* later
def path_gen(length):
    points = []
    start = [5, 4]
    for i in range(length):
        points.append(Point(start[0] - .5, start[1] - .5, 0))
        if i % 6 == 0:
            start = [start[0] - 1, start[1]]
        elif i % 5 == 0:
            start = [start[0], start[1] - 1]
        elif i % 4 == 0:
            start = [start[0] - 1, start[1]]
        elif i % 3 == 0:
            start = [start[0], start[1] - 1]
        elif i % 2 == 0:
            start = [start[0] - 1, start[1]]
    return points






if __name__ == '__main__':
    try:
        terrain()
    except rospy.ROSInterruptException:
        pass