from utils import *
from copy import deepcopy
import math

def avg(lista):
    lis = list(lista)
    return sum(lis)/len(lis)
    
def on_segment(p, q, r):
    if r[0] <= max(p[0],q[0]) and r[0] >= min(p[0],q[0]) and r[1] <= max(p[1],q[1]) and r[1] >= min(p[1],q[1]):
        return True
    return False

def orientation(p, q, r):
    val = ((q[1]-p[1]) * (r[0]-q[0])) - ((q[0]-p[0]) * (r[1]-q[1]))
    if val == 0:
        return 0
    return 1 if val > 0 else -1

def intersects(line_seg1, line_seg2):
    p1, q1 = line_seg1
    p2, q2 = line_seg2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    
    if o1 == 0 and on_segment(p1, q1, p2): return True
    if o2 == 0 and on_segment(p1, q1, q2): return True
    if o3 == 0 and on_segment(p2, q2, p1): return True
    if o4 == 0 and on_segment(p2, q2, q1): return True

    return False

def get_points(polygons, start, goal):
    points = []
    points.append(start)
    for i in polygons:
        for j in i:          
            points.append(j)
    points.append(goal)
    return points

def get_edges(polygons):
    edges = []
    for poly in polygons:
        for i in range(len(poly)):
            edges.append([poly[i],poly[(i+1)%len(poly)]])
    
    return edges
    
def visibility_graph(polygons, points, edges):
    vis_graph = {}
    for source in points:
        vis_graph[source] = {}
        for dest in points:
            if dest == source:
                continue
            flag = True
            for e in edges:
                if (dest not in e) and (source not in e):
                    if intersects((source, dest), e):
                        flag = False
                        break
            if flag:
                def getId(pnt):
                    for i in polygons:
                        if pnt in i:
                            return polygons.index(i)
                    return -1

                def immediate_neighbors(pnt):
                    for i in polygons:
                        if pnt in i:
                            ind = i.index(pnt)
                            n = len(i)
                            return [i[(ind + n - 1) %n], i[(ind+1)%n]]

                if (getId(source) != getId(dest)) or (dest in immediate_neighbors(source)):
                    vis_graph[source][dest] = euclidean_distance(source, dest)
    return vis_graph

def generateVG(polygons, states):
    points = get_points(polygons, states['start'], states['goal'])
    edges = get_edges(polygons)
    return visibility_graph(polygons, points, edges)

# class Search_Space:
#     def __init__(self, polygons, points, edges):
#         self.polygons = polygons
#         self.points = points
#         self.edges = edges

#     def sort_func(self, point, origin, refvec = [0,1]):
#         vector = [point[0] - origin[0],point[1] - origin[1]]
#         len_vector = math.hypot(vector[0],vector[1])
        
#         if len_vector == 0:
#             return -math.pi,0

#         normalized = [vector[0]/len_vector, vector[1]/len_vector]
#         dot_prod = dot_product(normalized,refvec)
#         diff_prod = refvec[1]*normalized[0] - refvec[0]*normalized[1]
#         angle = math.atan2(diff_prod, dot_prod)

#         if angle < 0:
#             return 2*math.pi+angle, len_vector
        
#         return angle, len_vector

#     def visible_vertices(self, vertex, points, polygons):
#         vis_verts = {}
#         open_edges = []
#         vertices = deepcopy(points)
#         sorted(vertices, reverse = True, key=lambda point: self.sort_func(point, vertex))
#         vertices.remove(vertex)
#         print(vertices)
#         return vis_verts


#     def visibility_graph1(self, polygons, points, edges):
#         vis_graph = {}
        
#         for v in points:
#             vis_graph[v] = visible_vertices(v,polygons)

#         return vis_graph