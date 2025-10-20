PLACEMENT_POINTS = {
    1: 12,
    2: 9,
    3: 8,
    4: 7,
    5: 6,
    6: 5,
    7: 4,
    8: 3,
    9: 2,
    10: 1,
}

KILL_POINT = 1

def calculate_points(placement: int, kills: int) -> int:
    placement_points = PLACEMENT_POINTS.get(placement, 0)
    return placement_points + kills * KILL_POINT
