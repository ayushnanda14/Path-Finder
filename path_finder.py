import math
from time import process_time

from graphPlotters import *
from randomGraphGen import *
from search import *
from search_space import *

#Change the value below to modify the no. of instances
Num_instances = 1
polygons_list = [generate_state_space(1000) for i in range(Num_instances)]
states_list = [generateStates(1000) for i in range(Num_instances)]

class PathFinder_GraphProblem(GraphProblem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal, graph)

    def h(self, node):
        return euclidean_distance(node.state, self.goal)
    def value(self, state):
        return euclidean_distance(state, self.goal)

cnt = 0


def custom_searchers(polygons, states, problems, header, searchers=[hill_climbing, astar_search, k_hill_climbing, k_hill_climbing, k_hill_climbing, k_hill_climbing]):
    def do(searcher, problem, k=1):
        p = InstrumentedProblem(problem)
        if name(searcher) == "k_hill_climbing":
            global cnt
            s = searcher(p,k+cnt)
            cnt += 1
            plotPath(s.path(), polygons, name(searcher),states)
            return p

        else:
            cnt = 0
            s = searcher(p)
            plotPath(s.path(), polygons, name(searcher),states)

        return p


    slen = len(searchers)
    plen = len(problems)
    avg_succs = [0 for i in range(slen)]
    avg_goal_tests = [0 for i in range(slen)]
    avg_states = [0 for i in range(slen)]
    avg_path_cost = [0 for i in range(slen)]
    avg_times = []

    data = []
    for s in searchers:
        tmp = []
        time_start = process_time()
        for p in problems:
            tmp.append(do(s, p))
        time_end = process_time()
        data.append(tmp)

        avg_times.append((time_end - time_start) / plen)

    for k in range(slen):
        avg_succs[k] = sum([data[k][i].succs for i in range(plen)]) // plen
        avg_goal_tests[k] = sum([data[k][i].goal_tests for i in range(plen)]) // plen
        avg_states[k] = sum([data[k][i].states for i in range(plen)]) // plen
        avg_path_cost[k] = sum([data[k][i].pathCost for i in range(plen)]) // plen

    return([avg_succs, avg_goal_tests, avg_states, avg_path_cost, avg_times])

def custom_graph_searchers(vis_graph, polygons, states):
    for i in polygons:
        plotPolygon(i)
    plotAll(vis_graph, polygons, states)
    searchers = ["hill_climbing\t", "astar_search\t","k_hill_climbing(dp = 2)", "k_hill_climbing(dp = 3)", "k_hill_climbing(dp = 4)", "k_hill_climbing(dp = 5)"]
    a = custom_searchers(polygons,states,problems=[PathFinder_GraphProblem(states['start'], states['goal'], vis_graph)], header=['<Searcher', 'Successors/ Goal Tests/ States/ Goal State>, Path Cost'])
    dic = {}
    for i in range(len(searchers)):
        dic[searchers[i]] = [a[j][i] for j in range(5)]
    return dic

def final(polygons_list, states_list):
    n = len(polygons_list)
    tot_time = 0
    searchers = ["hill_climbing\t", "astar_search\t",
                 "k_hill_climbing(dp = 2)", "k_hill_climbing(dp = 3)", "k_hill_climbing(dp = 4)", "k_hill_climbing(dp = 5)"]
    print("Trying for %d instances"%(n))
    dic = {}
    for i in searchers:
        dic[i] = []
    cnt = 0
    for polygons, states in zip(polygons_list, states_list):
        lenn = len(polygons)
        print(cnt+1)
        cnt+=1
        print("Generating visibility graph for %d polygons..."%lenn)
        gg_st = process_time()
        vis_graph = UndirectedGraph(generateVG(polygons, states))
        gg_en = process_time()
        tot_time += (gg_en - gg_st)
        print("Performing Graph Searches...\n")
        gs = custom_graph_searchers(vis_graph, polygons, states)
        for search in gs:
            dic[search].append(gs[search])
    
        print("\n\nName\t\t\t\tSuccessors\tGoal Tests\tStates\t\tPath Cost\tTime")
        for i in dic:
            ln = len(dic[i])
            suc = sum([j[0] for j in dic[i]])/ln
            gt  = sum([j[1] for j in dic[i]])/ln
            st  = sum([j[2] for j in dic[i]])/ln
            pc  = sum([j[3] for j in dic[i]])/ln
            tt  = sum([j[4] for j in dic[i]])/ln
            
            name = i
            print("%s\t\t%d\t\t%d\t\t%d\t\t%.2f\t\t%.4f"%(name,suc,gt,st,pc,tt))
    print("\nAverage Time Taken for generating Visibility Graph = ",tot_time/n)
final(polygons_list, states_list)


