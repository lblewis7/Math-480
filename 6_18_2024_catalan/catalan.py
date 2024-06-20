import itertools

def parenthesizations(n):
  """
  Returns a list of all possible parenthesizations of length n.

  Parameters:
    n (int): The length of the parenthesizations.

  Returns:
    A list of strings, where each inner string represents a valid parenthesization of length n.
  
  Example:
  >>> parenthesizations(3)
  {'((()))', '(()())', '(())()', '()(())', '()()()'}
  """
  if n == 0:
    return {""}
  elif n == 1:
    return {"()"}
  else:

    # the set of all possible parenthesizations of length n
    set1 = set()

    # add cases that are not fully contained in an outer set of parentheses 
    for i in range(1, n):
      set1a = parenthesizations(i)
      set1b = parenthesizations(n-i)
      for a in set1a: 
        for b in set1b: 
          set1.add(a+b)

    # add cases that are fully contained in an outer set of parentheses
    set2 = parenthesizations(n-1)
    for i in set2:
      set1.add("(" + i + ")")

    # return the set of all possible parenthesizations of length n
    return set1

def product_orders(n):
  """
  Returns a list of all possible ways to multiply of n elements.

  Parameters:
    n (int): The number of elements multiplied.

  Returns:
    A set of strings where each string represents a way to multiply n elements.
  
  Example:
  >>> product_orders(4)
  {'((?*?)*?)*?', '(?*(?*?))*?', '(?*?)*(?*?)', '?*((?*?)*?)', '?*(?*(?*?))'}

  """
  if n == 0:
    return {""}
  elif n == 1:
    return {"?"}
  elif n == 2:
    return {"?*?"}
  else:

    # the set of all ways to multiply n elements
    set1 = set()

    # add cases where the final multiplication is betweenn two calculated terms
    for i in range(2, n-1):
      set1a = product_orders(i)
      set1b = product_orders(n-i)
      for a in set1a: 
        for b in set1b: 
          set1.add("(" + a + ")*(" + b + ")")

    # add cases where the final multiplication is with the leftmost or rightmost number
    set2 = product_orders(n-1)
    for i in set2:
      set1.add("?*(" + i + ")")
      set1.add("(" + i + ")*?")
      
    # return the set of all ways to multiply n elements
    return set1

def permutations_avoiding_231(n):
  """
  Returns a list of permutations of length n avoiding the pattern 2-3-1.
  
  Parameters:
    n (int): The length of the permutation.
  
  Returns:
    A list of permutations of length n that do not contain the pattern 2-3-1.
  
  Example:
  >>> permutations_avoiding_231(4)
  {(1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (1, 4, 2, 3), (1, 4, 3, 2), (2, 1, 3, 4), (2, 1, 4, 3), (3, 1, 2, 4), (3, 2, 1, 4), (4, 1, 2, 3), (4, 1, 3, 2), (4, 2, 1, 3), (4, 3, 1, 2), (4, 3, 2, 1)}
  """
  if n < 3:
    return set(itertools.permutations(range(1, n+1)))
  else: 
    # create a set of all possible permutations of length n
    permutations = set(itertools.permutations(list(range(1, n+1))))

    # create a set of all possible permutations of length n that do not contain the pattern 2-3-1
    avoiding_perms = permutations.copy()

    # remove all permutations that contain the pattern 2-3-1
    for x in permutations:
      for i in range(0, n-2):
        for j in range(i+1, n-1):
          for k in range(j+1, n):
            if x[k] < x[i] and x[i] < x[j]:
              avoiding_perms.remove(x)
              # print("removed " + str(x))
              break
          else:
            continue
          break
        else:
          continue
        break
              
    # return the set of all permutations of length n that do not contain the pattern 2-3-1
    return avoiding_perms

def triangulations(n):
  """
  Returns a list of all possible triangulations of an n-sided polygon. A triangulation
  is represented as a list of internal edges. Vertices are labeled 0 through n-1 clockwise.

  Parameters:
    n (int): The number of sides of the polygon.

  Returns:
    A set of tuple of pairs, where each pair represents an internal edge in the triangulation.
  
  Example:
  >>> triangulations(5)
  {((0, 3), (1, 3)), ((1, 4), (2, 4)), ((1, 3), (1, 4)), ((0, 2), (2, 4)), ((0, 2), (0, 3))}
  """
  if n < 3:
    return set()
  elif n == 3:
    return {tuple()}
  else:

    """ this codium optimization attempt failed D:
    triangulations_list = []
    for i in range(0, n-2):
      for j in range(i+2, n):
        if (j-i > 1 and (i+n)-j > 1):
          triangulations_list.extend([((i, j), t) for t in triangulations(j-i+1)])
          triangulations_list.extend([((i, j), t) for t in triangulations(n-(j-i)+1)])
    return set(tuple(sorted(pair)) for pair in triangulations_list)
    """

    # the set of all possible triangulations of an n-sided polygon
    set1 = set()

    for i in range(0, n-2): # starting vertex of the edge
      for j in range(i+2, n): # ending vertex of the edge
        if (j-i > 1 and (i+n)-j > 1): # check if the edge is internal
          set1a = triangulations(j-i+1) # get the set of all possible triangulations of the left side
          set1b = triangulations(n-(j-i)+1) # get the set of all possible triangulations of the right side
          #print("set1b: " + str(set1b))

          for a in set1a: 
            for b in set1b:
              #print("b: " + str(b))

              # add the splitting edge to the current triangulation
              current = [(i, j)]

              # add the edges of the left and right sides to the current triangulation
              if j-i > 2 and n-(j-i) > 2:
                for a0 in a:
                  for b0 in b:
                    if ((a0[0] + i) % n) < ((a0[1] + i) % n): a1 = ((a0[0] + i) % n, (a0[1] + i) % n)
                    else:                                     a1 = ((a0[1] + i) % n, (a0[0] + i) % n)
                    if ((b0[0] + j) % n) < ((b0[1] + j) % n): b1 = ((b0[0] + j) % n, (b0[1] + j) % n)
                    else:                                     b1 = ((b0[1] + j) % n, (b0[0] + j) % n)
                    current.append(a1)
                    current.append(b1)
              elif j-i > 2:
                for a0 in a:
                  if ((a0[0] + i) % n) < ((a0[1] + i) % n): a1 = ((a0[0] + i) % n, (a0[1] + i) % n)
                  else:                                     a1 = ((a0[1] + i) % n, (a0[0] + i) % n)
                  current.append(a1)
              elif n-(j-i) > 2:
                for b0 in b:
                  if ((b0[0] + j) % n) < ((b0[1] + j) % n): b1 = ((b0[0] + j) % n, (b0[1] + j) % n)
                  else:                                     b1 = ((b0[1] + j) % n, (b0[0] + j) % n)
                  current.append(b1)

              # add the current triangulation to the set of all possible triangulations
              current.sort()
              set1.add(tuple(current))

    # return the set of all possible triangulations
    return set1