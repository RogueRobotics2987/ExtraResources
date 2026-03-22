import numpy as np
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
import math

class ShootOnMove():
    def __init__(self):
        self.robot_pos = None
        self.target_pos = None
        self.robot_vel = None

        self.dist_interp = interp1d([0, 0.5, 1, 1.5, 5], [.1, .15, .2, .25, .33]) # dist, time. Placeholder values

        self.time_array = []
        self.virtual_goal_dist_array = []


    # testing logic from https://github.com/rr1706/2022-Main/blob/main/src/main/java/frc/robot/commands/TurretedShooter/SmartShooter.java
    def Calculate(self, robot_pos, target_pos, robot_vel):
        self.robot_pos = robot_pos
        self.target_pos = target_pos
        self.robot_vel = robot_vel
        self.time_array = []
        self.virtual_goal_dist_array = []


        robot_to_target = self.robot_pos - self.target_pos

        robot_to_target_dist = np.linalg.norm(robot_to_target)

        time_to_target = self.dist_interp(robot_to_target_dist)


        temp_virtual_pos = self.target_pos
        for i in range(5):
            print(f"loop {i+1}")
            virtual_goal_x = temp_virtual_pos[0] - time_to_target * (self.robot_vel[0])
            virtual_goal_y = temp_virtual_pos[1] - time_to_target * (self.robot_vel[1])

            virtual_goal = np.array([virtual_goal_x, virtual_goal_y])
            robot_to_virtual = self.robot_pos - virtual_goal

            virtual_goal_dist = np.linalg.norm(robot_to_virtual)
            new_time_to_target = self.dist_interp(virtual_goal_dist)

            self.time_array.append(new_time_to_target)
            self.virtual_goal_dist_array.append(virtual_goal_dist)

            if math.fabs(time_to_target - new_time_to_target) < 0.001:
                print(f"Converged!")
                break

            time_to_target = new_time_to_target


    def Plot(self, label="Virtual target 1"):
        plt.scatter(self.time_array, self.virtual_goal_dist_array, label=label)
        plt.xlabel('Time')
        plt.ylabel('Virtual Goal Distance')
        plt.title(label)

    def PlotShow(self, title="Virtual target distance vs. shot time iterations"):
        plt.legend()
        plt.title(title)
        plt.show()

if __name__ == '__main__':
    robot_pos = [np.array([1,2]) for i in range(4)]# x, y field relative position
    target_pos = [np.array([1,2]) for i in range(4)]# x, y hub position
    robot_vel = [np.array([1,1]), np.array([2,1]), np.array([3,1]), np.array([4,1])] # x, y field relative velocity
    labels = [f"Virtual target {t} @ robot velocity {v}" for t, v in zip(target_pos, robot_vel)]
    m_sotm = ShootOnMove()

    for r_pos, t_pos, r_vel, label in zip(robot_pos, target_pos, robot_vel, labels):
        m_sotm.Calculate(r_pos, t_pos, r_vel)
        m_sotm.Plot(label=label)

    robot_pos = [np.array([1, 2]) for i in range(4)]  # x, y field relative position
    target_pos = [np.array([5, 2]) for i in range(4)]  # x, y hub position
    robot_vel = [np.array([1, 1]),np.array([2, 1]), np.array([3, 1]), np.array([4, 1])]  # x, y field relative velocity
    labels = [f"Virtual target {t} @ robot velocity {v}" for t, v in zip(target_pos, robot_vel)]
    for r_pos, t_pos, r_vel, label in zip(robot_pos, target_pos, robot_vel, labels):
        m_sotm.Calculate(r_pos, t_pos, r_vel)
        m_sotm.Plot(label=label)

    m_sotm.PlotShow()
