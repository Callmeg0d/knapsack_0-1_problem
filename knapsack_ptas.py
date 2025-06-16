import time
from functools import wraps
from itertools import combinations

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
def knapsack_ptas(profits, weights, capacity, k):
    n = len(profits)
    items = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)

    initial_solution, initial_profit, initial_weight, _ = knapsack_2approx(profits, weights, capacity)

    best_subset = initial_solution
    best_value = initial_profit
    intermediate_solution_count = 0

    def greedy_fill(selected_items, current_weight, current_profit):
        nonlocal best_value, best_subset, intermediate_solution_count
        for i in items:
            if i not in selected_items and current_weight + weights[i] <= capacity:
                current_weight += weights[i]
                current_profit += profits[i]
                selected_items.add(i)

        if current_profit > best_value:
            best_value = current_profit
            best_subset = [1 if i in selected_items else 0 for i in range(n)]

    for size in range(0, k + 1):
        for indices in combinations(items, size):
            intermediate_solution_count += 1
            total_weight = sum(weights[i] for i in indices)
            if total_weight > capacity:
                continue
            total_profit = sum(profits[i] for i in indices)
            remaining_profits = [p for i, p in enumerate(profits) if i not in indices]
            if total_profit + sum(remaining_profits) <= best_value:
                continue
            greedy_fill(set(indices), total_weight, total_profit)

    total_weight = sum(weights[i] for i in range(n) if best_subset[i] == 1)
    return best_subset, best_value, total_weight, intermediate_solution_count


execution_time, (best_solution, best_profit, best_weight, decisions ) = knapsack_ptas(profits, weights, capacity, k=3)
print(f"Время выполнения: {execution_time:.6f} секунд")
print("Лучшее решение:")
print(best_solution)
print(f"Итоговый профит: {best_profit}")
print(f"Итоговый вес: {best_weight}")
print(f"Количество решений: {decisions}")