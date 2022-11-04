import numpy as np
from matplotlib import pyplot as plt
import time


class PuzzlePiece:
    def __init__(self, name, complexity, book_order, shape):
        self.name = name
        self.shape = shape
        self.dimensions = shape.shape
        self.variations = self.variations()
        self.complexity = complexity
        self.book_order = book_order

    def is_square(self):
        return self.dimensions[0] == self.dimensions[1]

    def variations(self):
        variations = [self.shape]

        if np.equal(self.shape, np.flip(self.shape, axis=1)).all():

            if np.equal(self.shape, np.flip(self.shape, axis=0)).all():

                if self.is_square() and np.equal(self.shape, np.rot90(self.shape)).all():
                    pass

                else:
                    variations.append(np.rot90(self.shape))

            else:

                if self.dimensions[0] == self.dimensions[1] and np.equal(self.shape, np.rot90(
                        self.shape)).all():
                    pass

                else:
                    variations.append(np.rot90(self.shape))
                    variations.append(np.flip(self.shape, axis=0))
                    variations.append(np.rot90(np.flip(self.shape, axis=0)))

        else:

            if np.equal(self.shape, np.flip(self.shape, axis=0)).all():

                if self.dimensions[0] == self.dimensions[1] and np.equal(self.shape, np.rot90(
                        self.shape)).all():
                    pass

                else:
                    variations.append(np.rot90(self.shape))
                    variations.append(np.flip(self.shape, axis=1))
                    variations.append(np.rot90(np.flip(self.shape, axis=1)))

            else:

                if self.dimensions[0] == self.dimensions[1] and np.equal(self.shape, np.rot90(
                        self.shape)).all():
                    variations.append(np.rot90(self.shape))

                else:
                    variations.append(np.rot90(self.shape))
                    variations.append(np.flip(self.shape))
                    variations.append(np.rot90(np.flip(self.shape)))
                    variations.append(np.flip(self.shape, axis=0))
                    variations.append(np.rot90(np.flip(self.shape, axis=0)))
                    variations.append(np.flip(self.shape, axis=1))
                    variations.append(np.rot90(np.flip(self.shape, axis=1)))

        return variations



    def set_variations_to_grid(self, grid):
        new_vars = []
        for variation in self.variations:
            if variation.shape[0] <= grid[0] and variation.shape[1] <= grid[1]:
                new_vars.append(variation)
        self.variations = new_vars
        return

    def possible_positions(self, grid):
        grid = grid + np.array([1, 1])
        posibilities = 0
        for shape in self.variations:
            posibilities += np.prod(grid - shape.shape)

        return posibilities

def shape_on_grid(shape, grid, position):
    full_grid = np.zeros(grid)
    for x in range(shape.shape[0]):
        for y in range(shape.shape[1]):
            full_grid[x + position[0]][y + position[1]] = shape[x][y]
    return full_grid.astype(int)

def max_position(grid, shape):
    return grid - shape.shape + np.array([1, 1])

def possibilities(grid, shapes):
    possibilities = 1
    for shape in shapes:
        possibilities *= shape.possible_positions(grid)
    return possibilities

def possible_zero_splits(matrix):
    full_columns = np.prod(matrix, axis=0)
    full_rows = np.prod(matrix, axis=1)
    width = matrix.shape[1]
    for i in np.where(full_columns == 1)[0]:
        if np.sum(matrix[:, :i]) % 5 != 0:
            return False
    for i in np.where(full_rows == 1)[0]:
        if (i * width - np.sum(matrix[:i, :])) % 5 != 0:
            return False

    return True

def zero_patches(matrix):
    visited = np.zeros(matrix.shape).astype(bool)
    xlim, ylim = matrix.shape
    path = []

    def find_path(pos):
        if visited[pos[0], pos[1]]:
            return

        visited[pos[0], pos[1]] = True

        if matrix[pos[0], pos[1]] == 0:
            path.append(pos)
            down = (pos[0] + 1, pos[1])
            right = (pos[0], pos[1] + 1)
            up = (pos[0] - 1, pos[1])
            left = (pos[0], pos[1] - 1)

            if down[0] < xlim:
                find_path(down)

            if right[1] < ylim:
                find_path(right)

            if -1 < up[0]:
                find_path(up)

            if -1 < left[1]:
                find_path(left)

    for i in range(xlim):
        for j in range(ylim):
            path = []
            if not visited[i, j]:
                find_path((i, j))
            if len(path) % 5 != 0:
                return False

    return True





colors = {'br':(165,42,42), 'or':(255,150,0), 'gr':(2, 161, 34), 'lg':(35, 224, 1), 'yl':(226, 255, 3),
          'pr':(163, 2, 216), 'pk':(255, 0, 195), 'lb':(0, 227, 255), 'rd':(255, 0, 0), 'tl':(0, 255, 171),
          'gy':(151, 151, 151), 'bl':(0, 96, 255)}

brown = PuzzlePiece('br', 8, 3, np.array([[1, 0],
                                      [1, 1],
                                      [1, 0],
                                      [1, 0]]))

orange = PuzzlePiece('or', 6, 2, np.array([[1, 1],
                                       [1, 0],
                                       [1, 0],
                                       [1, 0]]))

green = PuzzlePiece('gr', 8, 10, np.array([[1, 1, 1],
                                    [0, 1, 0],
                                    [0, 1, 0]]))

light_green = PuzzlePiece('lg', 10, 11, np.array([[1, 0, 0],
                                           [1, 1, 0],
                                           [0, 1, 1]]))

yellow = PuzzlePiece('yl', 8, 7, np.array([[1, 1],
                                       [1, 0],
                                       [1, 1]]))

purple = PuzzlePiece('pr', 8, 4, np.array([[1, 0],
                                       [1, 0],
                                       [1, 1],
                                       [0, 1]]))

pink = PuzzlePiece('pk', 6, 6, np.array([[1, 0],
                                   [1, 1],
                                   [1, 1]]))

light_blue = PuzzlePiece('lb', 8, 8, np.array([[1, 0, 0],
                                           [1, 1, 1],
                                           [0, 0, 1]]))

red = PuzzlePiece('rd', 12, 12, np.array([[0, 1, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]]))

teal = PuzzlePiece('tl', 6, 5, np.array([[1, 1, 1],
                                   [1, 0, 0],
                                   [1, 0, 0]]))

gray = PuzzlePiece('gy', 10, 9, np.array([[1, 0, 0],
                                   [1, 1, 1],
                                   [0, 1, 0]]))

blue = PuzzlePiece('bl', 4, 1, np.array([[1],
                                   [1],
                                   [1],
                                   [1],
                                   [1]]))

shapes = [pink, yellow, gray, brown, green, purple]

# Sorting by book order
shapes = sorted(shapes, key=lambda x: x.book_order, reverse=True)

grid = np.array([5, len(shapes)])

# Gets rid of variations that don't fit in the grid
for shape in shapes:
    shape.set_variations_to_grid(grid)


def get_solution(grid, shapes, get_all=False):

    loops = 0

    solutions = []

    solution_count = 0
    unique_solution_count = 0

    solution = []
    shape_index = 0
    var_index = 0
    xy = [0, 0]
    previous_shape_on_grid = np.zeros(grid)

    def check_if_repeat(solution):

        for unique_solution in solutions:
            if (np.equal(solution, np.flip(unique_solution, axis=0)).all() or
                    np.equal(solution, np.flip(unique_solution, axis=1)).all() or
                    np.equal(solution, np.flip(np.flip(unique_solution, axis=1), axis=0)).all()):
                return False
            if solution.shape[0] == solution.shape[1]:
                if (np.equal(solution, np.rot90(unique_solution)).all() or
                np.equal(solution, np.rot90(unique_solution)).all() or
                np.equal(solution, np.rot90(np.flip(unique_solution, axis=0))).all() or
                np.equal(solution, np.rot90(np.flip(unique_solution, axis=1))).all() or
                np.equal(solution, np.rot90(np.flip(np.flip(unique_solution, axis=1), axis=0))).all()):
                    return False

        return True

    def make_solution(solution):
        final_grid = np.zeros((grid[0], grid[1], 3)).astype(int)
        for i in range(len(solution)):
            shape = shape_on_grid(shapes[i].variations[solution[i]['var']], grid, solution[i]['pos'])
            for x in range(grid[0]):
                for y in range(grid[1]):
                    if shape[x][y] == 1:
                        final_grid[x][y] = np.array(colors[solution[i]['name']])

        return final_grid

    moving_forward = True

    while True:
        loops += 1
        next = previous_shape_on_grid + shape_on_grid(shapes[shape_index].variations[var_index], grid, xy)

        # There are no errors so far
        if moving_forward and 2 not in next and zero_patches(next):
            solution.append(dict(name=shapes[shape_index].name, var=var_index, pos=xy))

            # We've made it
            if len(shapes) == shape_index + 1:
                if get_all:
                    solution_count += 1
                    solution_grid = make_solution(solution)
                    if check_if_repeat(solution_grid):
                        unique_solution_count += 1
                        solutions.append(solution_grid)
                    print(f'Solutions Found: {solution_count}     Unique: {unique_solution_count}')
                    solution.pop()
                    moving_forward = False

                else:
                    return make_solution(solution)

            # We haven't made it yet so to the next shape
            else:
                previous_shape_on_grid = next
                shape_index += 1
                var_index = 0
                xy = [0, 0]

        # Next row
        elif xy[0] + 1 < max_position(grid, shapes[shape_index].variations[var_index])[0]:
            moving_forward = True
            xy[0] += 1

        # Next column
        elif xy[1] + 1 < max_position(grid, shapes[shape_index].variations[var_index])[1]:
            moving_forward = True
            xy[0] = 0
            xy[1] += 1

        # Next Variation
        elif var_index + 1 < len(shapes[shape_index].variations):
            moving_forward = True
            xy = [0, 0]
            var_index += 1

        else:
            shape_index = len(solution) - 1
            if shape_index < 0:
                if len(solutions) == 0:
                    print('There are no solutions.')
                return solutions, solution_count, unique_solution_count
            var_index = solution[shape_index]['var']
            xy = solution[shape_index]['pos']
            previous_shape_on_grid = previous_shape_on_grid - shape_on_grid(shapes[shape_index].variations[var_index], grid, xy)
            solution.pop()

            moving_forward = False

def show_solutions(solutions, solution_count, unique_count):
    count = len(solutions)
    cols = int(np.ceil(np.sqrt(count)))
    rows = int(np.ceil(count / cols))
    fig, ax = plt.subplots(rows, cols, figsize=(15, 10))

    if count == 1:
        ax.imshow(solutions[0])
        ax.tick_params(
            axis='both',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            right=False,
            left=False,
            labelbottom=False,
            labelleft=False)

    elif count == 2:
        for i in range(count):
            ax[i].imshow(solutions[1])
            ax[i].tick_params(
            axis='both',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            right=False,
            left=False,
            labelbottom=False,
            labelleft=False)

    else:
        for i in range(count):
            x = i // cols
            y = i % cols
            ax[x, y].imshow(solutions[i])
            ax[x, y].tick_params(
            axis='both',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            right=False,
            left=False,
            labelbottom=False,
            labelleft=False)

        for i in range(count, cols * rows):
            x = i // cols
            y = i % cols
            ax[x, y].axis('off')

    fig.suptitle(f'Total Solutions: {solution_count}     Unique Solutions: {unique_count}', fontsize=24)
    plt.show()


start = time.time()
solutions, solution_count, unique_count = get_solution(grid, shapes, get_all=True)
stop = time.time()
print(stop - start)
show_solutions(solutions, solution_count, unique_count)
