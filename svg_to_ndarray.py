from heapq import heappop, heappush
from math import ceil, floor
import cairosvg
from PIL import Image
import numpy as np
from svgpathtools import svg2paths2, Path


def adjust_weights(ndarray: np.ndarray):
    # Get the dimensions of the grid
    rows, cols = ndarray.shape

    # Create a copy of the grid to store the new weights
    new_weights = ndarray.copy()

    # Iterate over the grid
    for row in range(rows):
        for col in range(cols):
            if np.isinf(ndarray[row, col]):
                # Check horizontally
                left_col = col - 1
                right_col = col + 1
                left_dist = 0
                right_dist = 0

                # Find the distance to the left obstacle
                while left_col >= 0 and not np.isinf(ndarray[row, left_col]):
                    left_col -= 1
                    left_dist += 1

                # Find the distance to the right obstacle
                while right_col < cols and not np.isinf(ndarray[row, right_col]):
                    right_col += 1
                    right_dist += 1

                if right_dist > 0:
                    mid_point = right_dist // 2
                    for d in range(1, right_dist + 1):
                        value = 10 - 2 * abs(mid_point - d + 1)
                        if d <= right_dist:
                            new_weights[row, col + d] = value
                        # else:
                        #     new_weights[row, col + (d - left_dist)] = value

                # if left_dist > 0 and right_dist > 0:
                #     total_dist = left_dist + right_dist
                #     mid_point = total_dist // 2
                #     for d in range(1, total_dist + 1):
                #         value = 10 - 2 * abs(mid_point - d + 1)
                #         if d <= left_dist:
                #             new_weights[row, col - d] = value
                #         else:
                #             new_weights[row, col + (d - left_dist)] = value

                # Check vertically
                top_row = row - 1
                bottom_row = row + 1
                top_dist = 0
                bottom_dist = 0

                # Find the distance to the top obstacle
                while top_row >= 0 and not np.isinf(ndarray[top_row, col]):
                    top_row -= 1
                    top_dist += 1

                # Find the distance to the bottom obstacle
                while bottom_row < rows and not np.isinf(ndarray[bottom_row, col]):
                    bottom_row += 1
                    bottom_dist += 1

                if top_dist > 0 and bottom_dist > 0:
                    total_dist = top_dist + bottom_dist
                    mid_point = total_dist // 2
                    for d in range(1, total_dist + 1):
                        value = 10 - 2 * abs(mid_point - d + 1)
                        if d <= top_dist:
                            new_weights[row - d, col] = value
                        else:
                            new_weights[row + (d - top_dist), col] = value

        # print(row)
    return new_weights


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


def heuristic(a, b):
    # a and b are tuples of (x, y)
    # returns a float
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class FloorplanGrid:
    # define properties
    grid = None
    height = 0
    width = 0
    paths: dict[str, Path] = {}

    def __init__(self, svg_file_path):
        self.grid = svg_to_ndarray(svg_file_path)
        # save grid to file
        np.savetxt("grid.txt", self.grid, fmt="%g")
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
        heappush(open_list, (0 + heuristic(start, end), 0, start))

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
                        priority = new_cost + heuristic(neighbor, end)
                        heappush(open_list, (priority, new_cost, neighbor))
                        came_from[neighbor] = current

        return path

    def get_route(self, start_id, end_id):
        if start_id == "section_entrance":
            arr = self.get_section_rect("section_entrance")
            start = (round((arr[0] + arr[1]) / 2), arr[2])
        else:
            start = (
                tuple(map(int, start_id.split(",")))
                if "," in start_id
                else self.get_section_aisle_midpoint(start_id)
            )

        end = (
            tuple(map(int, end_id.split(",")))
            if "," in end_id
            else self.get_section_aisle_midpoint(end_id)
        )

        return self.astar(start, end)


# run
# if __name__ == "__main__":
#     # print the rows of the ndarray
#     # grid = svg_to_ndarray("./frame.svg")
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
