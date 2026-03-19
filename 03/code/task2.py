def lambdaFuntion(b):
    x = lambda a: a * a
    print(x(b))

def stringLength(str):
    x = lambda s: len(s)
    print(x(str))

def randomNumber():
    import random
    for i in range(5):
        yield random.randint(1, 100)
    
def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        a, b = b, a + b
        if a > n:
            break

def main():
    print("Lambda Function:")
    lambdaFuntion(5)
    
    print("\nString Length:")
    stringLength("Hello, World!")
    
    print("\nRandom Numbers:")
    for num in randomNumber():
        print(num)
    
    print("\nFibonacci Sequence:")
    for num in fibonacci(10):
        print(num)

main()