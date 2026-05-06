def solve():
    adj = {}
    try:
        with open("tasks/day11/input.txt", "r") as f:
            for line in f:
                if ":" not in line:
                    continue
                node, neighbors = line.split(":")
                adj[node.strip()] = neighbors.split()
    except FileNotFoundError:
        return

    memo = {}

    def count_paths(current_node):
        if current_node == "out":
            return 1
        if current_node not in adj:
            return 0
        if current_node in memo:
            return memo[current_node]
        
        total_paths = 0
        for neighbor in adj[current_node]:
            total_paths += count_paths(neighbor)
            
        memo[current_node] = total_paths
        return total_paths

    print(count_paths("you"))

if __name__ == "__main__":
    solve()