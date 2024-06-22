import itertools
import random

def is_valid_SYT(candidate):
  """
  Check if the given candidate tableau is a valid standard Young tableau.

  Parameters:
  - candidate (Tuple[Tuple[int]]): The tableau to be checked.

  Returns:
  - bool: True if the matrix is valid, False otherwise.

  The function checks if the given matrix is a valid SYT matrix by verifying that:
  1. The elements in each column are in strictly increasing order.
  2. The elements in each row are in strictly increasing order.

  Example:
  >>> is_valid_SYT(((1, 2, 3), (4, 5, 6), (7, 8, 9)))
  True
  >>> is_valid_SYT(((1, 2, 3), (5, 4), (6))
  False
  """
  for row in range(len(candidate)):
    for col in range(len(candidate[row])):
      #print(candidate[row][col])
      if col > 0:
        if candidate[row][col] <= candidate[row][col - 1]: # check if elements in each column are in strictly increasing order
          return False
      if row > 0:
        if candidate[row][col] <= candidate[row - 1][col]: # check if elements in each row are in strictly increasing order
          return False
  return True

def reshape_perm(perm, shape):
  """
  Reshapes a permutation into a tableau based on the given shape.

  Parameters:
  - perm (Tuple[int]): The permutation to be reshaped.
  - shape (Tuple[int]): The shape of the resulting tableau as a weakly decreasing tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A tuple of tuples representing the reshaped permutation as a tableau.

  Example:
  >>> reshape_perm((1, 2, 3, 4, 5, 6), (3, 2, 1))
  ((1, 2, 3), (4, 5), (6,))
  """
  tableau = [None] * len(shape)
  i = 0
  for n in range(len(shape)):
    #print(f"n: {n}")
    #print(f"i: {i}")
    tableau[n] = tuple(perm[i:i+shape[n]])
    i += shape[n]
  return tuple(tableau)

def SYTs(shape):
  """
  Generates SYTs (Standard Young Tableaux) of on the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYTs as a tuple of integers.

  Returns:
  - List[Tuple[Tuple[int]]]: A list of valid SYTs generated based on the given shape.

  Example:
  >>> SYTs((2, 1))
  [((1, 2), (3,)), ((1, 3), (2,))]
  """

  n = sum(shape)
  results = []

  for perm in itertools.permutations(range(1, n+1)):
    if is_valid_SYT(reshape_perm(perm, shape)):
      results.append(reshape_perm(perm, shape))

  return results

def random_SYT(shape):
  """
  Generates a random Standard Young Tableau (SYT) of the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYT as a tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A random valid SYT generated based on the given shape.

  This function generates a random permutation of numbers from 1 to n+1, where n is the sum of the elements in the `shape` tuple. It then reshapes the permutation into a tableau using the `reshape_perm` function. If the resulting tableau is not valid, it shuffles the permutation and tries again. The function continues this process until a valid SYT is found, and then returns the reshaped permutation as a tableau.

  Example:
  >>> random_SYT((2, 1))
  ((1, 2), (3,))
  """
  n = sum(shape)
  while True:
    perm = tuple(random.sample(range(1, n+1), n))
    if is_valid_SYT(reshape_perm(perm, shape)):
      return reshape_perm(perm, shape)

def random_SYT_2(shape):
  """
  Generates a random Standard Young Tableau (SYT) of the given shape.

  Parameters:
  - shape (Tuple[int]): The shape of the resulting SYT as a tuple of integers.

  Returns:
  - Tuple[Tuple[int]]: A random valid SYT generated based on the given shape.

  The function generates a random SYT by starting off with the all zeroes tableau and greedily filling in the numbers from 1 to n. The greedy generation is repeated until a valid SYT is produced.

  Example:
  >>> random_SYT_2((2, 1))
  ((1, 2), (3,))
  """
  n = sum(shape) # number of elements

  # if the given shape is invalid (specifically if the number of elements is less than 1), return an empty tuple
  if n <= 0:
    return tuple()
  
  # if the given shape has exactly one cell, there is only one possible SYT
  if n == 1:
    return ((1,),)

  next = [] # all cells that may be able to contain the next element
  if (shape[0] > 1):
    next.append((0, 1))
  if (len(shape) > 1):
    next.append((1, 0))

  valid = next.copy() # subset of next that can actually be filled now

  # find the height of each column for later use
  col_height = []
  for i in range(shape[0]):
    current_height = 0
    for j in range(len(shape)):
      if shape[j] > i:
        current_height += 1
      else:
        break
    col_height.append(current_height)
  
  # generate a random tableau of the given shape
  tableau = [1]
  tableau.extend([0] * (n - 1))
  tableau = list(reshape_perm(tableau, shape))
  for i in range(len(tableau)):
    tableau[i] = list(tableau[i])
  for i in range(2, n+1):

    # generate a random cell that can contain the next element
    x = random.randint(0, len(valid) - 1)
    (a, b) = valid[x]

    # update next for the new element and prepare valid to be reassigned
    valid = []
    next.remove((a, b))

    # if in bounds and not already present, add the cells to the right and below the new element to next
    if (not (a + 1, b) in next) and a + 1 < col_height[b]:
      next.append((a + 1, b))
    if (not (a, b + 1) in next) and b + 1 < len(tableau[a]):
      next.append((a, b + 1))

    # fill in the new element
    tableau[a][b] = i

    # find all valid cells for the next element
    for (i, j) in next:
      flag = True

      # check if the cell is valid for the next element to be placed in
      if i - 1 >= 0:
        if tableau[i - 1][j] == 0:
          flag = False
      if j - 1 >= 0:
        if tableau[i][j - 1] == 0:
          flag = False

      # if so, add it to valid
      if flag:
        valid.append((i, j))

    # if no valid cells remain, return the tableau
    if len(valid) == 0:
      for i in range(len(tableau)):
        tableau[i] = tuple(tableau[i])
      return tuple(tableau)
    
  # if the above for loop has finished without returning, the code has broken in some way  
  print("This should never be reached")
  return tuple()