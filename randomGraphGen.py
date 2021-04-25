from search_space import *
from random import *
from pyrival import convex_hull

def generate_state_space(val):
    m, n = val, val
    i = 0
    N = randint(7, 12)
    wid = 200
    polygons = []

    for i in range(0, m, wid):
        for j in range(10, n, wid):
            points = []
            for k in range(N):
                x, y = randint(i+20, i+180), randint(j+20, j+180)
                points.append((x, y))
            polygons.append(convex_hull.convex_hull(points))
    return polygons


def generateStates(val):
    m, n = val, val
    st = {}
    st['start'] = (round(random()*10,1), round(random()*n,1))
    st['goal'] = (m + round(random()*10, 1), round(random()*n, 1))
    return st
