'''
Code written by Anchit Verma for Assignment 2, COMP 9021, 2018 S2.

'''

class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze(MazeError):

    def __init__(self, input_file):
        self.value = self.file_read(input_file)
        self.width = len(self.value[0])
        self.length = len(self.value)
        self.maze_check()
        self.lis = []
        self.culdesac_points = []
        self.inaccessible_points = set()
        self.accessible = set()
        self.maze, self.direction = self.matrix()
        self.name = input_file
        self.checklist = 0
        self.check = False


    def file_read(self, input_file):
        with open(input_file) as file:
            value = file.read()

        try:
            val = []
            some =[]
            for x in value.split('\n'):
                for y in x.strip():
                    if not y.isspace() and y:
                        some.append(int(y))

                if some:
                    val.append(some.copy())
                    if len(some) != len(val[0]):
                        raise MazeError('Incorrect input.')
                    some.clear()

            if not (2 <= len(val) <= 41 and 2 <= len(val[0]) <= 31):
                raise MazeError('Incorrect input.')

        except ValueError:
            raise MazeError('Incorrect input.')

        return val


    def maze_check(self):
        x = self.value
        for i in range(self.length):
            for j in range(self.width):

                if x[i][j] not in {0,1,2,3}:
                    raise MazeError('Incorrect input.')

            if x[i][-1] == 1 or x[i][-1] == 3:
                raise MazeError('Input does not represent a maze.')

            if x[-1][j] == 2 or x[-1][j] == 3:
                raise MazeError('Input does not represent a maze.')

        return


    def matrix(self):
        maze = [[0] * (self.width - 1) for _ in range(self.length - 1)]
        direction = [[''] * (self.width - 1) for _ in range(self.length - 1)]

        for i in range(self.length - 1):
            for j in range(self.width - 1):
                self.inaccessible_points.add((j, i))
                if self.value[i][j] == 0:
                    maze[i][j] += 4
                    direction[i][j] += 'NSEW'

                elif self.value[i][j] == 1:
                    maze[i][j] += 3
                    direction[i][j] += 'SEW'
                    if i-1 >= 0:
                        maze[i-1][j] -= 1
                        direction[i - 1][j] = direction[i-1][j].replace('S', '')

                elif self.value[i][j] == 2:
                    maze[i][j] += 3
                    direction[i][j] += 'NSE'
                    if j - 1 >= 0:
                        maze[i][j-1] -= 1
                        direction[i][j-1] = direction[i][j-1].replace('E', '')

                elif self.value[i][j] == 3:
                    maze[i][j] += 2
                    direction[i][j] += 'SE'
                    if i - 1 >= 0:
                        maze[i - 1][j] -= 1
                        direction[i - 1][j] = direction[i-1][j].replace('S', '')

                    if j - 1 >= 0:
                        maze[i][j - 1] -= 1
                        direction[i][j - 1] = direction[i][j-1].replace('E', '')


                if i == self.length - 2 and self.value[i + 1][j] == 1:
                    maze[i][j] -= 1
                if j == self.width - 2 and self.value[i][j + 1] == 2:
                    maze[i][j] -= 1

        return maze, direction


    def analyse(self):
        g = self.gates()
        w = self.connected_walls()
        i,a = self.accessible_areas()
        c = self.culdesacs()
        u = self.unique_paths()
        if not self.check:
            self.print_analyse(g, w, i, a, c, u)
        self.check = True


    def print_analyse(self, num_gates, num_walls, num_inaccessible, num_accessible, num_culdesacs, num_paths):
        if num_gates == 0:
            print(f'The maze has no gate.')
        elif num_gates == 1:
            print(f'The maze has a single gate.')
        else:
            print(f'The maze has {num_gates} gates.')

        if num_walls == 0:
            print(f'The maze has no wall.')
        elif num_walls == 1:
            print(f'The maze has walls that are all connected')
        else:
            print(f'The maze has {num_walls} sets of walls that are all connected.')

        if num_inaccessible == 0:
            print(f'The maze has no inaccessible inner point.')
        elif num_inaccessible == 1:
            print(f'The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {num_inaccessible} inaccessible inner points.')

        if num_accessible == 0:
            print(f'The maze has no accessible area.')
        elif num_accessible == 1:
            print(f'The maze has a unique accessible area.')
        else:
            print(f'The maze has {num_accessible} accessible areas.')

        if num_culdesacs == 0:
            print(f'The maze has no accessible cul-de-sac.')
        elif num_culdesacs == 1:
            print(f'The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {num_culdesacs} sets of accessible cul-de-sacs that are all connected.')

        if num_paths == 0:
            print(f'The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif num_paths == 1:
            print(f'The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {num_paths} entry-exit paths with no intersections not to cul-de-sacs.')


    def gates(self):
        maze = self.value
        num_gates = 0
        self.gates_list = []

        for i in range(self.width - 1):
            if maze[0][i] == 0 or maze[0][i] == 2:
                self.gates_list.append((0,i))
                num_gates += 1

            if maze[-1][i] == 0:
                self.gates_list.append((self.length-2, i))
                num_gates += 1

        for i in range(self.length - 1):
            if maze[i][0] == 0 or maze[i][0] == 1:
                self.gates_list.append((i,0))
                num_gates += 1

            if maze[i][-1] == 0:
                self.gates_list.append((i, self.width-2))
                num_gates += 1

        return num_gates


    def connected_walls(self):
        num_walls = 0

        for i in range(self.length):
            for j in range(self.width):
                num_walls += self._connected_walls(i, j)

        return num_walls

    def _connected_walls(self, i, j):
        if (i,j) in self.lis:
            return 0

        self.lis.append((i,j))

        # East
        if (j+1 <= self.width-1) and (self.value[i][j] in {1, 3}):
            self._connected_walls(i, j+1)

        # South
        if (i+1 <= self.length-1) and (self.value[i][j] in {2, 3}):
            self._connected_walls(i+1, j)

        # North
        if (0 <= i-1) and (self.value[i-1][j] in {2, 3}):
            self._connected_walls(i-1, j)

        # West
        if (0 <= j-1) and (self.value[i][j-1] in {1, 3}):
            self._connected_walls(i, j-1)

        if self.value[i][j] == 0:
            return 0

        return 1


    def accessible_areas(self):
        num_accessible = 0

        for i in range(self.length - 1):
            if self.value[i][0] == 0 or self.value[i][0] == 1:
                num_accessible += self._accessible_areas(i, 0)

            if self.value[i][-1] == 0:
                num_accessible += self._accessible_areas(i, self.width - 2)

        for j in range(self.width - 1):
            if self.value[0][j] == 0 or self.value[0][j] == 2:
                num_accessible += self._accessible_areas(0, j)

            if self.value[-1][j] == 0:
                num_accessible += self._accessible_areas(self.length-2, j)

        self.inaccessible_points = self.inaccessible_points - self.accessible
        num_inaccessible = len(self.inaccessible_points)

        return num_inaccessible, num_accessible

    def _accessible_areas(self, i, j):

        if (j, i) in self.accessible:
            return 0

        self.accessible.add((j, i))

        # East
        if (j + 1 < self.width - 1) and (self.value[i][j+1] in {0, 1}):
            self._accessible_areas(i, j + 1)

        # South
        if (i + 1 < self.length - 1) and (self.value[i+1][j] in {0, 2}):
            self._accessible_areas(i + 1, j)

        # North
        if (0 <= i - 1) and (self.value[i][j] in {0, 2}):
            self._accessible_areas(i - 1, j)

        # West
        if (0 <= j - 1) and (self.value[i][j] in {0, 1}):
            self._accessible_areas(i, j - 1)

        return 1


    def culdesacs(self):
        self.num_culdesacs = 0

        for i in range(self.length - 1):
            for j in range(self.width - 1):
                self.num_culdesacs += self._culdesacs(i, j)

        return self.num_culdesacs + self.checklist

    def _culdesacs(self, i, j, direction = 'X'):
        num = 0

        if self.maze[i][j] == 1:
            self.maze[i][j] = -1

            if (j,i) in self.inaccessible_points:
                return num

            self.culdesac_points.append((j+0.5,i+0.5))

            num += self.check_check(i,j,direction)

            # North
            if (0 <= i-1) and 'N' in self.direction[i][j]:
                self.maze[i - 1][j] -= 1
                self._culdesacs(i - 1, j, 'N')

            # South
            if (i + 1 < self.length - 1) and 'S' in self.direction[i][j]:
                self.maze[i + 1][j] -= 1
                self._culdesacs(i + 1, j, 'S')

            # East
            if (j + 1 < self.width - 1) and 'E' in self.direction[i][j]:
                self.maze[i][j + 1] -= 1
                self._culdesacs(i, j + 1, 'E')

            # West
            if (0 <= j - 1) and 'W' in self.direction[i][j]:
                self.maze[i][j - 1] -= 1
                self._culdesacs(i, j - 1, 'W')

            num += 1

        return num

    def check_check(self,i,j, direction):
        num = 0

        if (0 <= i-1) and direction != 'S' and ((j + 0.5, i - 0.5) in self.culdesac_points) and 'N' in self.direction[i][j]:
            self.checklist -= 1
            num -= 1

        if (i + 1 < self.length - 1) and direction != 'N' and ((j + 0.5, i + 1.5) in self.culdesac_points) and 'S' in self.direction[i][j]:
            self.checklist -= 1
            num -= 1

        if (j + 1 < self.width - 1) and direction != 'W' and ((j + 1.5, i + 0.5) in self.culdesac_points) and 'E' in self.direction[i][j]:
            num -= 1
            self.checklist -= 1

        if (0 <= j - 1) and direction != 'E' and ((j - 0.5, i + 0.5) in self.culdesac_points) and 'W' in self.direction[i][j]:
            num -= 1
            self.checklist -= 1

        return num


    def unique_paths(self):
        self.paths = []

        for e in self.gates_list:
            path = []
            path = self._unique_paths(e[0], e[1], path)
            if path and path[-1] in self.gates_list:
                self.paths.append(path)

        num_paths = len(self.paths)

        return num_paths

    def _unique_paths(self, i, j, path):

        if self.maze[i][j] == 2:

            path.append((i,j))

            self.maze[i][j] = -1

            if i+1 < self.length - 1 and 'S' in self.direction[i][j]:
                self._unique_paths(i+1, j, path)
            if j+1 < self.width - 1 and 'E' in self.direction[i][j]:
                self._unique_paths(i, j+1, path)

            if 0 <= i-1 and 'N' in self.direction[i][j]:
                self._unique_paths(i-1, j, path)
            if 0 <= j-1 and 'W' in self.direction[i][j]:
                self._unique_paths(i, j-1, path)

            if (i,j) in self.gates_list:
                return path

        elif self.maze[i][j] != -1:
            path.clear()


    def list_of_pillars(self):
        pillars_list = []

        for i in range(self.length):
            for j in range(self.width):
                if 0 <= i-1 and (self.value[i-1][j] == 2 or self.value[i-1][j] == 3):
                    continue
                elif 0 <= j-1 and (self.value[i][j-1] == 1 or self.value[i][j-1] == 3):
                    continue
                if self.value[i][j] == 0:
                    pillars_list.append((j, i))

        return pillars_list


    def display(self):
        if not self.check:
            self.check = True
            self.analyse()

        file_name = self.name.replace('.txt', '.tex')

        with open(file_name, 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
                    '\\usepackage{tikz}\n'
                    '\\usetikzlibrary{shapes.misc}\n'
                    '\\usepackage[margin=0cm]{geometry}\n'
                    '\\pagestyle{empty}\n'
                    '\\tikzstyle{every node}=[cross out, draw, red]\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\\vspace*{\\fill}\n'
                    '\\begin{center}\n'
                    '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]', file = tex_file)

            print('% Walls', file = tex_file)
            self.display_walls(tex_file)

            print('% Pillars', file = tex_file)
            for i in self.list_of_pillars():
                print(f'    \\fill[green] ({i[0]},{i[1]}) circle(0.2);', sep = '', file = tex_file)

            print('% Inner points in accessible cul-de-sacs', file=tex_file)
            for i in sorted(self.culdesac_points, key = lambda x: (x[1], x[0])):
                    print(f'    \\node at ({i[0]},{i[1]}) {{}};', file = tex_file)

            print('\\end{tikzpicture}\n'
                    '\\end{center}\n'
                    '\\vspace*{\\fill}\n'
                    '\n'
                    '\\end{document}', file = tex_file)


    def display_walls(self, tex_file):
        x = 0
        for i in range(self.length):
            for j in range(1, self.width):
                if (self.value[i][j - 1] == 3 or self.value[i][j - 1] == 1) and x == 0:
                    print(f'    \\draw ({j-1},{i}) -- ', end='', file=tex_file)
                    x += 1

                if self.value[i][j] == 1 or self.value[i][j] == 3:
                    continue

                if x > 0:
                    print(f'({j},{i});', sep='', file=tex_file)
                    x = 0

        for j in range(self.width):
            for i in range(1, self.length):
                if (self.value[i - 1][j] == 3 or self.value[i - 1][j] == 2) and x == 0:
                    print(f'    \\draw ({j},{i-1}) -- ', end='', file=tex_file)
                    x += 1

                if self.value[i][j] == 2 or self.value[i][j] == 3:
                    continue

                if x > 0:
                    print(f'({j},{i});', sep='', file=tex_file)
                    x = 0


    def sort_paths(self):
        list_paths = self.paths
        combined_paths = []

        for i in range(len(list_paths)):
            x = list_paths[i][0]
            for j in range(len(list_paths[i])):
                if 0 <= j - 1 < len(list_paths[i])-1 and list_paths[i][j][0] == list_paths[i][j - 1][0]:
                    continue
                else:
                    combined_paths.append((x, list_paths[i][j - 1]))
                    x = list_paths[i][j]

        for i in range(len(self.paths)):
            x = list_paths[i][0]
            for j in range(len(list_paths[i])):
                if 0 <= j - 1 < len(list_paths[i])-1 and list_paths[i][j][1] == list_paths[i][j - 1][1]:
                    continue
                else:
                    combined_paths.append((x, list_paths[i][j - 1]))
                    x = list_paths[i][j]

        return combined_paths
