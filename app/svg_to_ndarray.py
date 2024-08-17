from heapq import heappop, heappush
import itertools
from math import ceil, floor
import time
import cairosvg
from PIL import Image
import numpy as np
from svgpathtools import svg2paths2, Path


# Function to convert SVG to PNG and then to a numpy array
def svg_to_ndarray(svg_file_path):
    png_file_path = svg_file_path.replace(".svg", ".png")
    cairosvg.svg2png(url=svg_file_path, write_to=png_file_path)

    image = Image.open(png_file_path).convert("L")  # Convert to grayscale

    ndarray = np.array(image, dtype=np.float32)

    ndarray[ndarray > 0] = 10000
    ndarray[ndarray == 0] = 1

    # ndarray = adjust_weights(ndarray)

    return ndarray


# TODO: move to utils.py
def manhattan_distance(a, b):
    # a and b are tuples of (x, y)
    # returns a float
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def held_karp(coords):
    # TODO: modify to account for the fact that we probably want to end at section_checkout
    n = len(coords)

    # precompute the euclidean distance between each pair of coordinates
    distance = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            # We use the manhattan distance as an approximation of ditance between 2 locations. The actual distance would be given by the astar algorithm, however that would be too expensive to compute for all pairs of sections (n^2). The manhattan distance is a good approximation for the held-karp algorithm.
            distance[i, j] = distance[j, i] = manhattan_distance(coords[i], coords[j])

    # memoization table for the held-karp algorithm
    memo = {}

    # We initialize the memoization table with the distance between the starting point and each of the coordinates.
    # The key is a tuple of the form (bitmask, last) where bitmask is a binary representation of the visited nodes. The bitmask is an efficient way to store the list of visited nodes in the memoization table. (.e.g (0000110, 1) would mean that nodes 1 and 2 have been visited and the last node visited was 1).
    for i in range(1, n):
        memo[(1 << i, i)] = (distance[0, i], [0, i])

    # Iterate over increasing subset sizes
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                # This is basically equivalent to bits = bits | 1 << bit, which means shift 1 left by bit positions (e.g. 1 << 4 = 10000), and then do bits = bits | 10000 (which means flip to 1 wherever 1 is in either side, e.g. 00101 | 10100 = 10101). This new number basically tells us positions 4, 2 and 0 are visited.
                bits |= 1 << bit

            # Explore the minimum path for this subset
            for k in subset:
                prev_bits = bits & ~(1 << k)
                res = float("inf")
                best_path = []
                for m in subset:
                    if m == k:
                        continue
                    if (prev_bits, m) in memo:
                        cost = memo[(prev_bits, m)][0] + distance[m, k]
                        if cost < res:
                            res = cost
                            best_path = memo[(prev_bits, m)][1] + [k]
                memo[(bits, k)] = (res, best_path)
                # res = min(res, memo[(prev_bits, m)] + distance[m][k])
                # memo[(bits, k)] = res

    # Calculate the optimal path
    bits = (1 << n) - 2  # bitmask for all nodes except 0
    res = float("inf")
    best_path = []
    for k in range(1, n):
        if (bits, k) in memo:
            cost = memo[(bits, k)][0]
            if cost < res:
                res = cost
                best_path = memo[(bits, k)][1]

    return best_path


class FloorplanGrid:
    # define properties
    grid = None
    height = 0
    width = 0
    paths: dict[str, Path] = {}

    def __init__(self, svg_file_path):
        self.grid = svg_to_ndarray(svg_file_path)

        self.height, self.width = self.grid.shape
        paths, attributes, svg_attributes = svg2paths2(svg_file_path)

        for i, path in enumerate(paths):
            if attributes[i].get("id") is not None:
                self.paths[attributes[i].get("id")] = path

    def get_section_rect(self, section_id: str):
        section = self.paths[section_id]

        if section:
            bbox = section.bbox()
            # round to nearest integer
            bbox = [round(x) for x in bbox]
            return bbox
        else:
            return None

    def get_section_rect_with_padding(self, section_id: str, padding: int):
        bbox = self.get_section_rect(section_id)

        # bbox is always (xo, x1, y0, y1)

        if bbox:
            return (
                floor(bbox[0] - padding),
                ceil(bbox[1] + padding),
                floor(bbox[2] - padding),
                ceil(bbox[3] + padding),
            )
        else:
            return None

    def get_section_aisle_midpoint(self, section_id: str):
        bbox = self.get_section_rect_with_padding(section_id, 1)

        if not bbox:
            return None

        sides = [
            (bbox[0], round((bbox[2] + bbox[3]) / 2)),
            (bbox[1], round((bbox[2] + bbox[3]) / 2)),
            (round((bbox[0] + bbox[1]) / 2), bbox[2]),
            (round((bbox[0] + bbox[1]) / 2), bbox[3]),
        ]

        # filter out invalid sides
        sides = [
            side
            for side in sides
            if 0 <= side[0] < self.width
            and 0 <= side[1] < self.height
            and self.grid[int(side[1]), int(side[0])] == 1
        ]

        return sides[0] if sides else None

    # TODO: increase the score for cells between 2 sections (2 infs). if for example, there are 10 cells between them, then the midpoint should be 1 and increase outwards from there.
    # Also at the moment, 2 sections are so close but have an empty pixel between them throughe which routes go, need to modify the floor plan to remove that space (or modify the recommendation above so that the cost of going through that space is higher than going around it)
    def astar(self, start, end):
        # start and end are tuples of (x, y)
        # grid is a numpy array with inf for obstacles
        # returns a list of tuples from start to end
        # Create a priority queue and push the starting point onto it

        # flip the start abd end x,y coordinates to y,x
        start = (start[1], start[0])
        end = (end[1], end[0])

        # Create a priority queue and push the starting point onto it
        open_list = []
        heappush(open_list, (0 + manhattan_distance(start, end), 0, start))

        # Create dictionaries for tracking the path and the costs
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        # Define movements (up, down, left, right)
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while open_list:
            current_priority, current_cost, current = heappop(open_list)

            # If we reached the end, reconstruct the path
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            # Check neighbors
            for movement in movements:
                neighbor = (current[0] + movement[0], current[1] + movement[1])

                # Ensure the neighbor is within bounds
                if (
                    0 <= neighbor[0] < self.grid.shape[0]
                    and 0 <= neighbor[1] < self.grid.shape[1]
                ):
                    new_cost = current_cost + self.grid[neighbor[0], neighbor[1]]

                    # If this path to the neighbor is better, record it
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = new_cost + manhattan_distance(neighbor, end)
                        heappush(open_list, (priority, new_cost, neighbor))
                        came_from[neighbor] = current

        return path

    def get_start_coords(self, start_id):
        if start_id == "section_entrance":
            arr = self.get_section_rect("section_entrance")
            start = (round((arr[0] + arr[1]) / 2), arr[2])
        else:
            start = (
                tuple(map(int, start_id.split(",")))
                if "," in start_id
                else self.get_section_aisle_midpoint(start_id)
            )

        return start

    def get_route(self, start_id, end_id):
        start = self.get_start_coords(start_id)

        end = (
            tuple(map(int, end_id.split(",")))
            if "," in end_id
            else self.get_section_aisle_midpoint(end_id)
        )

        return self.astar(start, end)

    def get_optimal_routes(self, start_id, section_ids):
        start = self.get_start_coords(start_id)
        sections = [
            self.get_section_aisle_midpoint(section_id) for section_id in section_ids
        ]

        # filter out invalid sections
        sections = [section for section in sections if section]

        merged = [start, *sections]

        # get the optimal route to traverse from start to all sections. optimal_path is a list of indices of the sections in the merged list
        optimal_path = held_karp(merged)

        path_ids = [
            section_ids[i - 1] if i != 0 else "section_entrance" for i in optimal_path
        ]
        optimal_path_coords = [merged[p] for p in optimal_path]

        # get the route from each section to the next
        routes = [
            (
                path_ids[i + 1],
                self.astar(optimal_path_coords[i], optimal_path_coords[i + 1]),
            )
            for i in range(len(optimal_path_coords) - 1)
        ]

        return routes


# run
# if __name__ == "__main__":
#     # print by row, inf should be printed as -
#     # for row in grid:
#     #     print(",".join(["-" if x == np.inf else "1" for x in row]))
#     floorplan = FloorplanGrid("./floor_plan.svg")
#     # print(floorplan.get_section_rect("section_0"))
#     # print(floorplan.get_section_rect_with_padding("section_0", 1))
#     # print(floorplan.get_section_aisle_midpoint("section_0"))

#     arr = floorplan.get_section_rect("section_entrance")

#     # print(floorplan.get_section_rect_with_padding("section_2", 1))

#     start = (round((arr[0] + arr[1]) / 2), arr[2])
#     end = floorplan.get_section_aisle_midpoint("section_34")

#     print(start, end)

#     # print column 38 of grid
#     # print(",".join(["-" if x == np.inf else "1" for x in floorplan.grid[:, 38]]))

#     path = floorplan.astar(start, end)
#     print(path)
