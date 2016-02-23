import copy
import time

class Node(object):
    def __init__(self, parent = None, children = None, g_n = None, h_n = None, depth = None, data = None, void_pos = ()):
        self.parent = parent
        self.children = children
        self.g_n = g_n
        self.h_n = h_n
        self.depth = depth
        self.data = data
        self.void_pos = void_pos


class State:
    def __init__(self):
        return

    def get_void_pose(self):
        return State().get_pos_of_zero(State.initial_state())

    @staticmethod
    def initial_state():
        # test case 1
        return [[1, 3, 4],
                [8, 0, 5],
                [7, 2, 6]]

        # test case 2
        # return [[1, 2, 3],
        #         [8, 0, 4],
        #         [7, 6, 5]]

        # test case 3
        # return [[1, 2, 3],
        #         [4, 5, 6],
        #         [7, 8, 0]]

    @staticmethod
    def final_state():
        # test case 1
        return [[1, 2, 3],
                [8, 0, 4],
                [7, 6, 5]]

        # test case 2
        # return [[3, 6, 4],
        #         [0, 1, 2],
        #         [8, 7, 5]]

        # test case 3
        # return [[1, 8, 2],
        #         [0, 4, 3],
        #         [7, 6, 5]]

    def get_pos_of_zero(self, arr):
        for i in xrange(arr.__len__()):
            for j in xrange(arr[i].__len__()):
                if arr[i][j] == 0:
                    return i, j

GRID_SIZE = State.initial_state().__len__()

class CalculateHeuristic:
    def __init__(self):
        return

    def pos(self, num, final):
        for i in range(0, GRID_SIZE):
            for j in range(0, GRID_SIZE):
                if final[i][j] == num:
                    return i, j

    @staticmethod
    def heuristics(initial, final, manhattan_or_not):
        if manhattan_or_not == 0:
            heuristic = 0
            diff = 0

            for i in range(0, GRID_SIZE):
                for j in range(0, GRID_SIZE):
                    _i, _j = CalculateHeuristic().pos(initial[i][j], final)
                    diff = abs(_i - i) + abs(_j - j)
                    heuristic += diff
            return heuristic

        else:
            counter = 0
            for i in range(0, GRID_SIZE):
                for j in range(0, GRID_SIZE):
                    if initial[i][j] != final[i][j]:
                        counter += 1
            return counter


class AvailableMove:
    posX = 0
    posY = 0

    def __init__(self, (x, y)):
        AvailableMove.posX = x
        AvailableMove.posY = y

    def calculate(self):
        return [self.is_moving_up_possible(), self.is_moving_down_possible(), self.is_moving_right_possible(), self.is_moving_left_possible()]

    def is_moving_right_possible(self):
        if AvailableMove.posY >= 2:
            return ()
        else:
            return ('east', self.posX, self.posY + 1)

    def is_moving_left_possible(self):
        if AvailableMove.posY <= 0:
            return ()
        else:
            return ('west', self.posX, self.posY - 1)

    def is_moving_up_possible(self):
        if AvailableMove.posX <= 0:
            return ()
        else:
            return ('north', self.posX - 1, self.posY)

    def is_moving_down_possible(self):
        if AvailableMove.posX >= 2:
            return ()
        else:
            return ('south', self.posX + 1, self.posY)

class Calculate:
    GRID_SIZE = State.initial_state().__len__()
    start = time.clock()
    frontier = []
    counter = 0
    visited =[]

    def __init__(self):
        self.frontier = []
        self.calc()

    def check_completeness(self, data):
        for i in range(0, data.__len__()):
            for j in range(0, data[i].__len__()):
                if data[i][j] != State.final_state()[i][j]:
                    return False
        return True

    def find_node_with_min_h_n(self, front):
        min_f_n = front[0].h_n + front[0].g_n
        min_f_n_node = None

        for node in front:
            f_n = node.h_n + node.g_n

            if node.parent == None:  # executes when the node passed is the root node and has no children
                min_f_n_node = front[0]
            else:  # executes when the passed node is not the root node and has children
                if f_n <= min_f_n:
                    min_f_n = f_n
                    min_f_n_node = node
                    # print 'here'

        return min_f_n_node

    def is_already_visited(self, data):
        for item in self.visited:
            if item == data:
                return True
        return False

    def calc(self):
        # initializing the initial and final states
        ini = State.initial_state()
        fi = State.final_state()

        # Calculating the Heuristic of the root node
        h_x = CalculateHeuristic.heuristics(ini, fi, MANHATTAN_OR_NOT)  # 0 -> Manhattan, 1 -> Misplaced Tiles

        # Making the Root Node
        root_node = Node(None, None, 0, h_x, 0, ini, State().get_void_pose())

        # Creating the frontier
        self.frontier.append(root_node)

        # calling the recursive compute function
        self.compute(self.frontier)


    def get_void_position(self, data):
        for i in xrange(data.__len__()):
            for j in xrange(data[i].__len__()):
                if data[i][j] == 0:
                    return i, j
        return None

    def compute(self, frontier):
        min_f_n_node = self.find_node_with_min_h_n(frontier)

        if self.check_completeness(min_f_n_node.data):
            print ''
            print 'Found in', min_f_n_node.depth, 'steps'
            print ''
            print 'Path cost:', min_f_n_node.depth
            print ''

            print 'Initial configuration'
            print '-------------------'

            for i in range(0, State.initial_state().__len__()):
                print State.initial_state()[i]
            print ''

            self.print_path(min_f_n_node)
            duration = time.clock() - Calculate.start
            print 'Time cost:', duration, 'sec'
            return

        for node in frontier:
            self.visited.append(node)

        # Get the possible moves
        possibleMoves = AvailableMove(self.get_void_position(min_f_n_node.data)).calculate()

        #remove the expanding node
        frontier.remove(min_f_n_node)

        for new_pos in possibleMoves:
            if new_pos != ():
                tempData = copy.deepcopy(min_f_n_node)
                x, y = self.get_void_position(min_f_n_node.data)
                direction, x_new, y_new = new_pos
                tempData.data[x][y], tempData.data[x_new][y_new] = tempData.data[x_new][y_new], tempData.data[x][y]
                _h_n = CalculateHeuristic.heuristics(tempData.data, State.final_state(), MANHATTAN_OR_NOT)  # 0 -> Manhattan, 1 -> Misplaced Tiles
                new_child = Node(min_f_n_node, None, min_f_n_node.g_n + 1, _h_n, min_f_n_node.depth + 1, tempData.data,(x_new, y_new))

                if not self.is_already_visited(new_child):
                    frontier.append(new_child)

                if self.check_completeness(new_child.data):
                    print ''
                    print 'Found in', new_child.depth, 'steps'
                    print ''

                    print 'Path cost:', new_child.depth
                    print ''

                    print 'Initial configuration'
                    print '-------------------'

                    for i in range(0, State.initial_state().__len__()):
                        print State.initial_state()[i]
                    print ''

                    self.print_path(new_child)
                    duration = time.clock() - Calculate.start
                    print 'Time cost:', duration, 'sec'
                    return

        self.counter += 1
        self.compute(frontier)

    def print_path(self, node):
        if node.parent != None:
            self.print_path(node.parent)

            for i in range(0, node.data.__len__()):
                print node.data[i]
            print ''

        else:
            print 'Final configuration'
            print '-------------------'

            for i in range(0, State.final_state().__len__()):
                print State.final_state()[i]
            print ''

            if MANHATTAN_OR_NOT == 0:
                print 'Heuristic Mode used: Manhattan Distance'
            else:
                print 'Heuristic Mode used: Misplaced Tiles'

            print ''
            print 'Steps to achieve goal state'
            print '---------------------------'
            return


MANHATTAN_OR_NOT = 0
Calculate()
