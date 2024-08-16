# I no longer remember what this is for. I forgot to add comments unfortunately. Thankfully, it's not being used


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
