import time
from functools import wraps

with open("benchmarks/p1/cap.txt", "r") as f:
    capacity = int(f.readline().strip())

profits = []
with open("benchmarks/p1/prof.txt", "r") as f:
    for line in f:
        profits.append(int(line.strip()))

weights = []
with open("benchmarks/p1/weig.txt", "r") as f:
    for line in f:
        weights.append(int(line.strip()))

def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start

        return execution_time, result

    return wrapper

@count_time
def knapsack_dp(profits, weights, capacity):
    n = len(profits)

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    intermediate_solution_count = 0

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i-1] <= w:
                dp[i][w] = max(profits[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
                intermediate_solution_count += 1
            else:
                dp[i][w] = dp[i-1][w]
                intermediate_solution_count += 1

    chosen_items = [0] * n
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen_items[i-1] = 1
            w -= weights[i-1]

    total_profit = dp[n][capacity]
    total_weight = sum(weights[i] for i in range(n) if chosen_items[i])

    return chosen_items, total_profit, total_weight, intermediate_solution_count


execution_time, (best_solution, best_profit, best_weight, decisions) = knapsack_dp(profits, weights, capacity)
print(f"Время выполнения: {execution_time:.6f} секунд")
print("Лучшее решение:")
print(best_solution)
print(f"Итоговый профит: {best_profit}")
print(f"Итоговый вес: {best_weight}")
print(f"Количество решений: {decisions}")
