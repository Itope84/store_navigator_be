import random
import time
from ..route_generation import FloorplanGrid, svg_to_ndarray


def test_optimal_route_generation():

    floorplan = FloorplanGrid("app/floor_plan.svg")

    shelf_count_to_time = {}

    for n in range(5, 21):
        start_time = time.time()
        indexes = random.sample(range(1, 81), n)
        shelf_ids = [f"section_{i}" for i in indexes]

        route = floorplan.get_optimal_routes("section_entrance", shelf_ids)
        end_time = time.time()

        shelf_count_to_time[n] = end_time - start_time

        print(f"Time taken: {end_time - start_time} seconds")

    print(shelf_count_to_time)
