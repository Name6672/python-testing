import math

primes = []

def is_prime(num,ordered:bool=True) -> bool:
  return_value = False
  if num in primes:
    return_value = True
  elif num == 2:
    print('two found')
    return_value = True
  elif len(primes) > 0 and ordered:
    print('more and ordered')
    for prime in primes:
      if num % prime:
        return_value = False
  else:
    for test_val in range(2,math.floor(num/2)):
      if not num % test_val:
        return_value = False
  return return_value


for i in range(99999):
  if is_prime(i):
    print('prime found')
    primes.append(i)


print (primes)