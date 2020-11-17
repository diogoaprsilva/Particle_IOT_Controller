import time

def fibo(n):
   if n == 1:
       return 0
   elif n == 2:
       return 1
   else:
       return(fibo(n-1) + fibo(n-2))

nterms = 20
fizz = 0
buzz = 0
fizzbuzz = 0


start = time.time()

if nterms <= 0:
   print("Please enter a positive integer")
else:
   print("Fibonacci sequence:")
   for i in range(1,nterms):
    n = (fibo(i))
    if n % 3 == 0 and n % 5 == 0:
        print("FizzBuzz")
        fizzbuzz = fizzbuzz + 1
    elif n % 3 == 0:
        print ("Fizz")
        fizz = fizz + 1
    elif n % 5 == 0:
        print ("Buzz")
        buzz = buzz + 1
    else:
        print (n)
print("FINISHED")
print ("FIZZ NUMBER:")
print (fizz)
print ("BUZZ NUMBER:")
print (buzz)
print ("FIZZBUZZ NUMBER:")
print (fizzbuzz)
print ("TIME:")
end = time.time()

print(end - start)