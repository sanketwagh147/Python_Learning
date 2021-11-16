def fibonacci(n):
    if n > 2:
        return fibonacci(n-2) + fibonacci(n-1)
    else:
        return 1


fibonacci(6)
