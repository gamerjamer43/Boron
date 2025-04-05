#import Random

fn quicksort(list arr) -> list {
    if length(arr) <= 1 {  
        -> arr
    }

    int pivot = arr[length(arr) // 2]
    list left = []
    list right = []
    list equal = []

    for (int i = 0; i < length(arr); i += 1) {
        int value = arr[i]
        if value < pivot {
            left += [value]
        } else if value > pivot {
            right += [value]
        } else {
            equal += [value]
        }
    }

    -> quicksort(left) + equal + quicksort(right)
}

list sample_list = Random.fill(10, 10000)
list sorted_list = quicksort(sample_list)
out("Sorted array: " + toStr(sorted_list))

list sorted_list2 = sort(Random.fill(1000, 10000))