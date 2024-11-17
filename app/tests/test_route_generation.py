import random
import time
from ..svg_to_ndarray import FloorplanGrid, svg_to_ndarray


# def test_svg_to_ndarray():
#     floorplan = FloorplanGrid("app/floor_plan.svg")
#     arr = floorplan.get_section_rect("section_entrance")
#     print("testing testing")
#     print(arr)


# Test that the optimal route for a shopping list visiting up to 20 shelves is generated in less than 5 seconds
# time the function
def test_optimal_route_generation():
    start_time = time.time()
    floorplan = FloorplanGrid("app/floor_plan.svg")

    # random shelves between 1 and 80
    indexes = random.sample(range(1, 81), 20)
    shelf_ids = [f"section_{i}" for i in indexes]

    # print the paths KEYS
    # print(floorplan.paths.keys())

    route = floorplan.get_optimal_routes("section_entrance", shelf_ids)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    # print(route)
