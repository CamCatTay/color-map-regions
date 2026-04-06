import heapq

GRAPH = {
    "A": [("C", 3),  ("B", 12), ("E", 6)],
    "B": [("A", 12), ("C", 15), ("D", 5),  ("E", 5)],
    "C": [("A", 3),  ("B", 15), ("F", 18)],
    "D": [("B", 5),  ("F", 4),  ("H", 19)],
    "E": [("A", 6),  ("B", 5),  ("G", 22)],
    "F": [("C", 18), ("D", 4),  ("H", 10)],
    "G": [("E", 22), ("H", 4)],
    "H": [("D", 19), ("F", 10), ("G", 4)],
}


def dijkstra_algorithm(graph, source):
    dist = {node: float("inf") for node in graph}
    prev = {node: None for node in graph}
    dist[source] = 0

    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist > dist[u]:
            continue

        for neighbor, weight in graph[u]:
            candidate = dist[u] + weight
            if candidate < dist[neighbor]:
                dist[neighbor] = candidate
                prev[neighbor] = u
                heapq.heappush(heap, (candidate, neighbor))

    return dist, prev

def print_results(dist, prev, source):
    print(f"\nDijkstra's dijkstra_algorithm Source: {source}")
    print("-" * 48)
    print(f"{'Node':<8} {'Distance':<12} {'Optimal Path'}")
    print("-" * 48)

    for node in sorted(dist):
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        path_str = " -> ".join(path)
        print(f"{node:<8} {dist[node]:<12} {path_str}")

    print("-" * 48)


def main():
    source = "A"
    dist, prev = dijkstra_algorithm(GRAPH, source)

    print_results(dist, prev, source)


if __name__ == "__main__":
    main()
