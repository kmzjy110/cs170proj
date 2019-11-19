def dijkstra(self, node):
    # Get index of node (or maintain int passed in)
    nodenum = self.get_index_from_node(node)
    # Make an array keeping track of distance from node to any node
    # in self.nodes. Initialize to infinity for all nodes but the
    # starting node, keep track of "path" which relates to distance.
    # Index 0 = distance, index 1 = node hops
    dist = [None] * len(self.nodes)
    for i in range(len(dist)):
        dist[i] = [float("inf")]
        dist[i].append([self.nodes[nodenum]])

    dist[nodenum][0] = 0
    # Queue of all nodes in the graph
    # Note the integers in the queue correspond to indices of node
    # locations in the self.nodes array
    queue = [i for i in range(len(self.nodes))]
    # Set of numbers seen so far
    seen = set()
    while len(queue) > 0:
        # Get node in queue that has not yet been seen
        # that has smallest distance to starting node
        min_dist = float("inf")
        min_node = None
        for n in queue:
            if dist[n][0] < min_dist and n not in seen:
                min_dist = dist[n][0]
                min_node = n

        # Add min distance node to seen, remove from queue
        queue.remove(min_node)
        seen.add(min_node)
        # Get all next hops
        connections = self.connections_from(min_node)
        # For each connection, update its path and total distance from
        # starting node if the total distance is less than the current distance
        # in dist array
        for (node, weight) in connections:
            tot_dist = weight + min_dist
            if tot_dist < dist[node.index][0]:
                dist[node.index][0] = tot_dist
                dist[node.index][1] = list(dist[min_node][1])
                dist[node.index][1].append(node)
    return dist