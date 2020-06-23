import sys
from queue import PriorityQueue
from constants import NODES_NAME, HEURISTIC, GRAPH



def breadth_first_search(graph, source, destination):
    try:
        traversed_path, traversed_cost = [], 0
        shortest_path, shortest_cost = [], 0

        parent, distance, total_distance, queue = [], [], [], []
        visited = set()

        for i in range(len(NODES_NAME)):
            parent.append("None")
            distance.append(-1) #sys.maxsize
            total_distance.append(-1)

        visited.add(source)
        queue.append(source)
        distance[NODES_NAME[source]] = 0
        total_distance[NODES_NAME[source]] = 0
        traversed_path.append(source)
        while queue:
            popped_vertex = queue[0]
            queue.pop(0)
            for neighbours in graph[popped_vertex]:
                # neighbours = (node, cost)
                if neighbours[0] not in visited:
                    visited.add(neighbours[0])
                    queue.append(neighbours[0])
                    distance[NODES_NAME[neighbours[0]]] = distance[NODES_NAME[popped_vertex]] + neighbours[1]
                    parent[NODES_NAME[neighbours[0]]] = popped_vertex
                    traversed_path.append(neighbours[0])
                    total_distance[NODES_NAME[neighbours[0]]] = neighbours[1]
            if popped_vertex==destination:
                # Removing extra vertices that would have been marked visited after destination
                while queue:
                    traversed_path.remove(queue[0])
                    total_distance.pop(NODES_NAME[queue[0]])
                    queue.pop(0)
                break
        

        temp_sum = 0
        for i in total_distance:
            if i != -1:
                temp_sum += i
        traversed_cost = temp_sum


        shortest_cost = distance[NODES_NAME[destination]]
        traversing_parent = parent[NODES_NAME[destination]]
        shortest_path.append(destination)
        shortest_path.append(traversing_parent)
        if traversing_parent!='None':
            while traversing_parent != source:
                traversing_parent = parent[NODES_NAME[traversing_parent]]
                shortest_path.append(traversing_parent)

        shortest_path.reverse()
        # print(shortest_path, shortest_cost)
        # print(traversed_path, traversed_cost)
        return shortest_path, shortest_cost, traversed_path, traversed_cost
    except KeyError:
        print("Source or Destination doesn't exists", file=sys.stderr)

def uniform_cost_search(graph, source, destination):
    try:
        traversed_path, traversed_cost = [], 0
        shortest_path, shortest_cost = [], 0

        parent, distance, total_distance = [], [], []
        queue = PriorityQueue()
        visited = set()

        for i in range(len(NODES_NAME)):
            parent.append("None")
            distance.append(-1) #sys.maxsize
            total_distance.append(-1)

        #visited.add(source)
        queue.put((0, source))
        distance[NODES_NAME[source]] = 0
        total_distance[NODES_NAME[source]] = 0
        traversed_path.append(source)
        while not queue.empty():
            popped_vertex = queue.get()
            popped_vertex = popped_vertex[1]
            visited.add(popped_vertex)
            for neighbours in graph[popped_vertex]:
                # neighbours = (node, cost)
                if neighbours[0] not in visited:
                    #visited.add(neighbours[0])
                    distance[NODES_NAME[neighbours[0]]] = distance[NODES_NAME[popped_vertex]] + neighbours[1]
                    queue.put((distance[NODES_NAME[neighbours[0]]], neighbours[0]))
                    parent[NODES_NAME[neighbours[0]]] = popped_vertex
                    traversed_path.append(neighbours[0])
                    total_distance[NODES_NAME[neighbours[0]]] = neighbours[1]
            if popped_vertex==destination:
                # Removing extra vertices that would have been marked visited after destination
                while not queue.empty():
                    temp = queue.get()
                    traversed_path.remove(temp[1])
                    total_distance.pop(NODES_NAME[temp[1]])
                break
        

        while traversed_path[-1] != destination:
            temp = traversed_path.pop(-1)
            total_distance[NODES_NAME[temp]] = -1
        
        temp_sum = 0
        for i in total_distance:
            if i != -1:
                temp_sum += i
        traversed_cost = temp_sum


        shortest_cost = distance[NODES_NAME[destination]]
        traversing_parent = parent[NODES_NAME[destination]]
        shortest_path.append(destination)
        shortest_path.append(traversing_parent)
        if traversing_parent!='None':
            while traversing_parent != source:
                traversing_parent = parent[NODES_NAME[traversing_parent]]
                shortest_path.append(traversing_parent)

        shortest_path.reverse()
        # print(shortest_path, shortest_cost)
        # print(traversed_path, traversed_cost)
        return shortest_path, shortest_cost, traversed_path, traversed_cost
    except KeyError:
        print("Source or Destination doesn't exists", file=sys.stderr)


def greedy_best_first_search(graph, source, destination, heuristics):
    try:
        traversed_path, traversed_cost = [], 0
        shortest_path, shortest_cost = [], 0

        parent, distance, total_distance = [], [], []
        queue = PriorityQueue()
        visited = set()

        for i in range(len(NODES_NAME)):
            parent.append("None")
            distance.append(-1) #sys.maxsize
            total_distance.append(-1)

        queue.put((heuristics[source], source))
        distance[NODES_NAME[source]] = 0
        total_distance[NODES_NAME[source]] = 0
        traversed_path.append(source)
        while not queue.empty():
            popped_vertex = queue.get()
            popped_vertex = popped_vertex[1]
            visited.add(popped_vertex)
            for neighbours in graph[popped_vertex]:
                # neighbours = (node, cost)
                if neighbours[0] not in visited:
                    distance[NODES_NAME[neighbours[0]]] = distance[NODES_NAME[popped_vertex]] + neighbours[1]
                    queue.put((heuristics[neighbours[0]], neighbours[0]))
                    parent[NODES_NAME[neighbours[0]]] = popped_vertex
                    traversed_path.append(neighbours[0])
                    total_distance[NODES_NAME[neighbours[0]]] = neighbours[1]
            if popped_vertex==destination:
                # Removing extra vertices that would have been marked visited after destination
                # while not queue.empty():
                #     temp = queue.get()
                #     traversed_path.remove(temp[1])
                #     total_distance.pop(NODES_NAME[temp[1]])
                break
        

        while traversed_path[-1] != destination:
            temp = traversed_path.pop(-1)
            total_distance[NODES_NAME[temp]] = -1

        temp_sum = 0
        for i in total_distance:
            if i != -1:
                temp_sum += i
        traversed_cost = temp_sum


        shortest_cost = distance[NODES_NAME[destination]]
        traversing_parent = parent[NODES_NAME[destination]]
        shortest_path.append(destination)
        shortest_path.append(traversing_parent)
        if traversing_parent!='None':
            while traversing_parent != source:
                traversing_parent = parent[NODES_NAME[traversing_parent]]
                shortest_path.append(traversing_parent)

        shortest_path.reverse()
        # print(shortest_path, shortest_cost)
        # print(traversed_path, traversed_cost)
        return shortest_path, shortest_cost, traversed_path, traversed_cost
    except KeyError:
        print("Source or Destination doesn't exists", file=sys.stderr) 

def depth_limit_search(graph, source, destination, depth_limit, visited, parent, traversed_path, total_distance, distance):

    if source == destination:
        return True
    
    if depth_limit <= 0:
        return False

    for neighbours in graph[source]:
        if neighbours[0] not in visited:
            visited.add(neighbours[0])
            traversed_path.append(neighbours[0])            
            parent[NODES_NAME[neighbours[0]]] = source
            total_distance[NODES_NAME[neighbours[0]]] = neighbours[1]
            distance[NODES_NAME[neighbours[0]]] = distance[NODES_NAME[source]] + neighbours[1]
            if depth_limit_search(graph, neighbours[0], destination, depth_limit-1, visited, parent, traversed_path, total_distance, distance)==True:
                return True

def iterative_depth_first_search(graph, source, destination):
    try:
        traversed_path, traversed_cost = [], 0
        shortest_path, shortest_cost = [], 0

        

        i = 0
        while True:
            parent, distance, total_distance = [], [], []
            for j in range(len(NODES_NAME)):
                parent.append("None")
                distance.append(-1) #sys.maxsize
                total_distance.append(-1)

            visited = set()
            traversed_path = []
            traversed_path.append(source)
            distance[NODES_NAME[source]] = 0
            total_distance[NODES_NAME[source]] = 0
            visited.add(source)
            #print("Depth-Limit " + str(i), file=sys.stderr)
            if depth_limit_search(graph, source, destination, i, visited, parent, traversed_path, total_distance, distance) == True:
                break
            i +=1

        temp_sum = 0
        for i in total_distance:
            if i != -1:
                temp_sum += i
        traversed_cost = temp_sum

        shortest_cost = distance[NODES_NAME[destination]]
        traversing_parent = parent[NODES_NAME[destination]]
        shortest_path.append(destination)
        shortest_path.append(traversing_parent)
        if traversing_parent!='None':
            while traversing_parent != source:
                traversing_parent = parent[NODES_NAME[traversing_parent]]
                shortest_path.append(traversing_parent)

        shortest_path.reverse()

        return shortest_path, shortest_cost, traversed_path, traversed_cost
    except KeyError:
        print("Source or Destination doesn't exists", file=sys.stderr) 

def read_from_STDIN():
    # Heuristic Table
    no_nodes = int(input())
    heuristics_dict = {}
    for i in range(no_nodes):
        heuristic = input().split()
        city_name = heuristic[0]
        heuristics_cost = int(heuristic[1])
        heuristics_dict[city_name] = heuristics_cost

    # print(heuristics_dict)

    # Graph Data
    graph = {}
    no_nodes = int(input())
    for i in range(no_nodes):
        graph_dict = input().split()
        connected_node_list = []
        no_connected_nodes = int(graph_dict[1])
        # 2nd index have node and 3rd index have cost and so on ++
        i, j = 2, 3
        while no_connected_nodes:
            connected_node = graph_dict[i]
            connected_node_cost = int(graph_dict[j])
            connected_node_list.append((connected_node, connected_node_cost))
            no_connected_nodes -= 1
            i += 2
            j += 2
        graph[graph_dict[0]] = connected_node_list
    
    source = input().split(':')[1].strip()
    destination = input().split(':')[1].strip()

    return heuristics_dict, graph, source, destination

def print_graph(graph):
    for i in range(len(graph)):
        print(graph[i], end=' ')
        if i < len(graph) - 1:
            print("->", end=' ')


def print_result(results):
    for result in results:
        print(result[4])
        print("Actual Path:", end=" ")
        print_graph(result[1])
        print("\nTotal Cost: " + str(result[0]) + "\n")
        print("Traversed Path:", end=' ')
        print_graph(result[2])
        print("\nTotal Cost: " + str(result[3]))
        print('\n\n')


if __name__ == "__main__":

    heuristics, graph, source, destination = read_from_STDIN()
    
    # heuristics, graph = HEURISTIC, GRAPH
    # source = input("Source: ").strip()
    # destination = input("Destination: ").strip()

    algo, shortest_path, shortest_cost, traversed_path, traversed_cost = [], [], [], [], []
    results = []

    for i in range(4):
        algo.append(1)
        shortest_path.append(1)
        shortest_cost.append(1)
        traversed_path.append(1)
        traversed_cost.append(1)


    algo[0] = "BFS"
    shortest_path[0], shortest_cost[0], traversed_path[0], traversed_cost[0] = breadth_first_search(graph, source, destination)
    

    algo[1] = "UCS"
    shortest_path[1], shortest_cost[1], traversed_path[1], traversed_cost[1] = uniform_cost_search(graph, source, destination)

    algo[2] = "GBFS"
    shortest_path[2], shortest_cost[2], traversed_path[2], traversed_cost[2] = greedy_best_first_search(graph, source, destination, heuristics)

    algo[3] = "IDDFS"
    shortest_path[3], shortest_cost[3], traversed_path[3], traversed_cost[3] = iterative_depth_first_search(graph, source, destination)
    
    for i in range(4):
        results.append((shortest_cost[i], shortest_path[i], traversed_path[i], traversed_cost[i], algo[i]))
    
    results.sort()
    print_result(results)
