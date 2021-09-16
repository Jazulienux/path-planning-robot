import time
import math
from copy import copy
import numpy as np
from numpy.linalg.linalg import cond


class ImprovedAstar():

    def __init__(self, path):
        self.error_obs = 0.65
        self.startP = classKirim.start
        self.endP = classKirim.end
        self.last_path = copy(path)
        self.inc = 0
        self.new_path = [self.startP]
        self.length = len(self.last_path)
        self.last_inc = 0
        print()
        print("Improved A*")

    def path_normalize(self):
        while(self.inc < self.length):
            new_len = len(self.new_path) - 1
            start_point = self.new_path[new_len]
            end_point = self.last_path[self.inc]
            counter = self.dda_algorithm(start_point, end_point)
            if(counter):
                if(self.inc == 0 or self.last_inc == self.inc):
                    self.inc += 1
                new_node = self.last_path[self.inc - 1]
                self.new_path.append(new_node)
                self.inc = len(self.last_path) - \
                    (len(self.last_path) - self.inc)
                self.last_inc = self.inc
            else:
                self.inc += 1
        else:
            self.new_path.pop(0)
            self.new_path += [self.endP]

        print(self.new_path)
        return self.new_path

    def dda_algorithm(self, start_pt, end_pt):
        try:
            condition = False

            x1, y1 = start_pt
            x2, y2 = end_pt

            dx = x2-x1
            dy = y2-y1

            step = 0
            if(abs(dx) > abs(dy)):
                step = abs(dx)
            else:
                step = abs(dy)

            step = np.rint(step).astype(int)
            if(step <= 0.):
                step = 1

            xinc = dx/step
            yinc = dy/step

            for _ in range(step):
                x1 += xinc
                y1 += yinc
                point = (x1, y1)
                obs_total = classKirim.obs
                if(classKirim.isActiveSimulasi == 1):
                    obs_total = classKirim.obs + classKirim.obsO

                for obs in obs_total:
                    new_obs = np.array(obs)
                    new_point = np.array(point)
                    err = new_obs - new_point
                    err = np.linalg.norm(err)
                    if(err <= self.error_obs):
                        condition = True
                        break

            return condition
        except Exception as e:
            print(e)
            self.new_path.append(start_pt)


class Astar():

    def __init__(self):
        super(Astar, self).__init__()
        self.path = []

    def run(self):
        self.path = []
        self.dir_row = [-0.5, -0.5, 0, +0.5, +0.5, +0.5, 0, -0.5]
        self.dir_col = [0, +0.5, +0.5, +0.5, 0, -0.5, -0.5, -0.5]

        self.cameFrom = {}

        start = classKirim.start
        end = classKirim.end

        classKirim.history_start = copy(start)
        classKirim.history_end = copy(end)

        obs = classKirim.obs
        if(classKirim.isActiveSimulasi == 1):
            obs += classKirim.obsO

        classKirim.history_obs = copy(obs)

        self.isLoop = 0

        fin = np.array(end) - np.array(start)
        fin = np.linalg.norm(fin)

        if(fin <= 1.5):
            self.isLoop = 1
            self.path = [end]
        else:
            self.startP = start
            self.endP = end

            self.gScore = {start: 0}
            self.fScore = {start: self.heuristic(start, end)}
            self.openSet = []
            self.closedSet = set()
            self.openSet.append((start, self.fScore[start]))
            self.cond_break = False
            posi = 0
            enorm_locking = 0.65  # 375
            erfin = 0.75
            while(self.isLoop == 0):
                if(len(self.openSet) > 0):
                    self.openSet.sort(reverse=False, key=lambda idx: idx[1])
                    cur = self.openSet.pop(0)[0]

                    fin = np.array(end) - np.array(cur)
                    fin = np.linalg.norm(fin)
                    if(fin <= erfin):
                        self.cond_break = True

                    if(self.cond_break == True):
                        print("Loop", posi)
                        self.path = []
                        while(cur in self.cameFrom):
                            point = cur
                            self.path.append(point)
                            cur = self.cameFrom[cur]
                        self.path = self.path[::-1]
                        self.path += [self.endP]
                        self.isLoop = 1
                        print(self.path)
                    else:
                        self.closedSet.add(cur)
                        print(cur)

                        for i in range(len(self.dir_col)):
                            rr = cur[0] + self.dir_row[i]
                            cc = cur[1] + self.dir_col[i]
                            neighbor = (rr, cc)

                            if(rr < 0 or cc < 0):
                                continue
                            if(rr > classKirim.maxX or cc > classKirim.maxY):
                                continue

                            conditional = False
                            obs_total = classKirim.obs
                            if(classKirim.isActiveSimulasi == 1):
                                obs_total = classKirim.obs + classKirim.obsO
                            for obs in obs_total:
                                new_point = np.array(obs)
                                now_node = np.array(neighbor)
                                enorm = new_point - now_node
                                enorm = np.linalg.norm(enorm)
                                if(enorm <= enorm_locking):
                                    conditional = True
                                    break

                            if(conditional):
                                continue

                            tentative_gscore = self.gScore[cur] + \
                                self.heuristic(cur, neighbor)

                            if(neighbor in self.closedSet and tentative_gscore >= self.gScore.get(neighbor, 0)):
                                continue

                            # print((cur, neighbor), tentative_gscore,
                            #       self.gScore[cur])

                            if(tentative_gscore < self.gScore.get(neighbor, 0) or neighbor not in [idx[0] for idx in self.openSet]):
                                self.cameFrom[neighbor] = cur
                                self.gScore[neighbor] = tentative_gscore
                                self.fScore[neighbor] = tentative_gscore + \
                                    self.heuristic(neighbor, end)
                                self.openSet.append(
                                    (neighbor, self.fScore[neighbor]))
                        # print()
                        # if(posi == 5):
                        #     self.openSet.sort(
                        #         reverse=False, key=lambda idx: idx[1])
                        #     print(len(self.openSet))
                        #     for i in self.openSet:
                        #         print(i)
                        #     print("****")
                        #     print(cur)
                        #     print(self.closedSet)
                        #     print("-" * 100)
                        #     break
                        posi += 1
                else:
                    self.isLoop = -1
            else:
                if(self.isLoop == 1):
                    if(len(self.path) > 1):
                        improved = ImprovedAstar(self.path)
                        self.path = improved.path_normalize()

    def heuristic(self, start, end, mode=0):
        start = np.array(start)
        end = np.array(end)

        res = 0.
        if(mode == 0):
            # Manhattan Distance
            x_ = abs(end[0] - start[0])
            y_ = abs(end[1] - start[1])
            res = x_ + y_
            # print(start,end, res)
            res = np.sum(np.abs(end - start))
            # print(res)
        elif(mode == 1):
            # Euclidiance Distance
            res = np.sqrt(np.sum((end - start)**2))

        return res


class KirimCond():
    def __init__(self):
        super(KirimCond, self).__init__()
        self.isActiveSimulasi = 0
        self.start = (2.05, 3.43)
        self.end = (1.5, 1.52)
        self.obs = [(2.98, 1.48), (2.96, 0.62), (2.08, 2.34)]
        self.robotMax = 3
        self.maxX = 9
        self.maxY = 6
        self.cImgBall = [0., 0.]
        self.cImgRobot = [0., 0.]
        self.isLoopUDP = 0
        self.checkMaster = [-1, 0]
        self.obsO = []
        self.command = 0
        self.history_start = copy(self.start)
        self.history_end = copy(self.end)
        self.history_obs = copy(self.obs) + self.obsO


if __name__ == "__main__":
    classKirim = KirimCond()
    astar = Astar()
    astar.run()
    print("Done")
