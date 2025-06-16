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
def knapsack_2approx(profits, weights, capacity):
    n = len(profits)
    items = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)

    greedy_items = [0] * n
    greedy_profit = 0
    greedy_weight = 0
    intermediate_solution_count = 0

    for i in items:
        intermediate_solution_count += 1
        if greedy_weight + weights[i] <= capacity:
            greedy_items[i] = 1
            greedy_profit += profits[i]
            greedy_weight += weights[i]

    max_single_profit = max(profits, default=0)
    if max_single_profit > greedy_profit:
        best_idx = profits.index(max_single_profit)
        chosen_items = [0] * n
        chosen_items[best_idx] = 1

        return chosen_items, max_single_profit, weights[best_idx], 1
    else:
        return greedy_items, greedy_profit, greedy_weight, intermediate_solution_count


execution_time, (best_solution, best_profit, best_weight, decisions) = knapsack_2approx(profits, weights, capacity)
print(f"Время выполнения: {execution_time:.6f} секунд")
print("Лучшее решение:")
print(best_solution)
print(f"Итоговый профит: {best_profit}")
print(f"Итоговый вес: {best_weight}")
print(f"Количество решений: {decisions}")