import random
import time

def quicksort(arr):
    # Base case: arrays with 0 or 1 element are already sorted.
    if len(arr) <= 1:
        return arr
    # Choose pivot element (middle element)
    pivot = arr[len(arr) // 2]
    # Partition the array into three lists: less, equal, and greater than the pivot.
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    # Recursively apply quicksort to left and right partitions and combine the results.
    return quicksort(left) + middle + quicksort(right)

# Generate a list of 21 random integers between 0 and 100.
random_list = [random.randint(0, 10000) for _ in range(10000)]
print("Original list:", random_list)

# Time the quicksort execution.
start_time = time.time()
sorted_list = quicksort(random_list)
end_time = time.time()

print("Sorted list:", sorted_list)
print("Execution time: {:.3f} ms".format((end_time - start_time) * 1000))
