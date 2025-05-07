def max_positive_sum(arr):
  """
    Finds the maximum positive sum of any contiguous range within the array.
  Args:
    arr: An unsorted array of integer values.
  Returns:
    The maximum positive sum of any contiguous range within the array.
  """
  max_sum = 0
  for i in range(len(arr)):
    current_sum = 0
    for j in range(i, len(arr)):
      current_sum += arr[j]
      if current_sum > 0:
        max_sum = max(max_sum, current_sum)
  return max_sum

print(max_positive_sum([3,-4,8,7,-10,19,-3]))
print(max_positive_sum([-8,-10,-12,-2,-3,5]))