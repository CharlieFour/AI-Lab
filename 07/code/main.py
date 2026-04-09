from smart_framework import smart_sort
import random

def run_tests():
    # Scenario A: Small list
    test_1 = [5, 1, 9, 3, 2]
    print("Testing Small List:")
    print(f"Result: {smart_sort(test_1)}\n")

    # Scenario B: Large nearly-sorted list
    test_2 = list(range(100))
    test_2[10], test_2[11] = test_2[11], test_2[10] # Small swap
    print("Testing Nearly Sorted List:")
    sorted_2 = smart_sort(test_2)
    print(f"Result (first 10): {sorted_2[:10]}...\n")

    # Scenario C: Large random list
    test_3 = random.sample(range(1000), 100)
    print("Testing Large Random List:")
    sorted_3 = smart_sort(test_3)
    print(f"Result (first 10): {sorted_3[:10]}...\n")

if __name__ == "__main__":
    run_tests()