import sys

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

    # state is (current_node, visited_dac, visited_fft)
    memo = {}

    def count_paths(u, v_dac, v_fft):
        # Update visited status for current node
        now_dac = v_dac or (u == "dac")
        now_fft = v_fft or (u == "fft")
        
        if u == "out":
            return 1 if (now_dac and now_fft) else 0
        
        state = (u, now_dac, now_fft)
        if state in memo:
            return memo[state]
        
        if u not in adj:
            return 0
        
        total = 0
        for v in adj[u]:
            total += count_paths(v, now_dac, now_fft)
            
        memo[state] = total
        return total

    # Set recursion limit higher for deep graphs if necessary
    sys.setrecursionlimit(2000)
    print(count_paths("svr", False, False))

if __name__ == "__main__":
    solve()