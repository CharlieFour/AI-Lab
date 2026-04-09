import sorting_algorithms as sa

def smart_sort(data):
    """
    Analyzes input data characteristics to select the most suitable algorithm.
    """
    n = len(data)
    
    # Check for near-sortedness by counting inversions
    inversions = 0
    for i in range(n - 1):
        if data[i] > data[i+1]:
            inversions += 1
            
    # Selection Logic:
    # 1. For small datasets (n < 20), use Insertion Sort due to low overhead.
    if n < 20:
        print(f"Selection: Insertion Sort (Small size: {n})")
        return sa.insertion_sort(data.copy())
    
    # 2. For nearly sorted data (less than 10% out of order), use Insertion Sort.
    if (inversions / n) < 0.1:
        print(f"Selection: Insertion Sort (Nearly sorted)")
        return sa.insertion_sort(data.copy())
    
    # 3. For large, random data, use Merge Sort for O(n log n) stability.
    print(f"Selection: Merge Sort (Large random dataset: {n} elements)")
    return sa.merge_sort(data.copy())