#function1
def sum(n):
    return n*(n+1)/2
print(sum(10))

#array sum
def arraysum(a):
  sum = 0
  for i in a:
    sum = sum + i
    return sum

a = [12, 3, 4, 15]
print(arraysum(a))