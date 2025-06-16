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
def knapsack_branch_and_bound(profits, weights, capacity):
    n = len(profits)

    items = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)

    best_value = 0
    best_items = [0] * n
    intermediate_solution_count = 0

    def upper_bound(index, current_profit, current_weight):
        if current_weight >= capacity:
            return current_profit
        bound = current_profit
        remaining_capacity = capacity - current_weight
        for i in items[index:]:
            weight = weights[i]
            if weight <= remaining_capacity:
                bound += profits[i]
                remaining_capacity -= weight
            else:
                bound += profits[i] * (remaining_capacity / weight)
                break
        return bound

    def backtrack(index, current_profit, current_weight, selected):
        nonlocal best_value, best_items, intermediate_solution_count

        if index == n:
            if current_profit > best_value:
                best_value = current_profit
                best_items = selected.copy()
            return

        item_index = items[index]
        weight = weights[item_index]
        profit = profits[item_index]

        if current_weight + weight <= capacity:
            selected[item_index] = 1
            intermediate_solution_count += 1
            backtrack(index + 1, current_profit + profit, current_weight + weight, selected)
            selected[item_index] = 0

        if upper_bound(index + 1, current_profit, current_weight) > best_value:
            intermediate_solution_count += 1
            backtrack(index + 1, current_profit, current_weight, selected)

    backtrack(0, 0, 0, best_items.copy())

    total_weight = sum(weights[i] for i in range(n) if best_items[i] == 1)

    return best_items, best_value, total_weight, intermediate_solution_count


execution_time, (best_solution, best_profit, best_weight, decisions) = knapsack_branch_and_bound(profits, weights, capacity)
print(f"Время выполнения: {execution_time:.6f} секунд")
print("Лучшее решение:")
print(best_solution)
print(f"Итоговый профит: {best_profit}")
print(f"Итоговый вес: {best_weight}")
print(f"Количество решений: {decisions}")