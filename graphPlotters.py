import matplotlib.pyplot as plt
def plotPolygon(polygon):
    xaxes = [point[0] for point in polygon]
    yaxes = [point[1] for point in polygon]
    xaxes.append(polygon[0][0])
    yaxes.append(polygon[0][1])
    plt.plot(xaxes, yaxes, marker='.', color='k', markersize=5, linewidth=1.0)

def plotVG(vgd):
    for i in vgd:
        for j in vgd[i].keys():
            plt.plot([i[0], j[0]], [i[1], j[1]],
                     marker='.', markersize=5, color='g', linewidth=0.1)

def plotAll(vg, polygons, states):
    for i in polygons:
        plotPolygon(i)
    plotVG(vg.graph_dict)
    plt.text(states['start'][0], states['start'][1], 'S',fontsize=12, color='r', horizontalalignment='right')
    plt.text(states['goal'][0], states['goal'][1], 'G',fontsize=12, color='g', horizontalalignment='left')
    plt.scatter(states['start'][0], states['start'][1], marker='s', c='blue')
    plt.scatter(states['goal'][0], states['goal'][1], marker='s', c='blue')
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.title("Visibility Graph")
    plt.show()

def plotPath(node_path, polygons, searcher_name,states):
    for i in polygons:
        plotPolygon(i)
    line = [i.state for i in node_path]
    xaxes = [point[0] for point in line]
    yaxes = [point[1] for point in line]
    plt.plot(xaxes, yaxes, marker='o', color='r', markersize=5, linewidth=0.5)
    plt.text(states['start'][0], states['start'][1], 'S',fontsize=12, color='r', horizontalalignment='right')
    plt.text(states['goal'][0], states['goal'][1], 'G',fontsize=12, color='g', horizontalalignment='left')
    plt.scatter(states['start'][0], states['start'][1], marker='s', c='blue')
    plt.scatter(states['goal'][0], states['goal'][1], marker='s', c='blue')
    plt.xlabel('X-Axis')
    plt.ylabel('Y-Axis')
    plt.title(searcher_name)
    plt.show()



