
from functools import lru_cache, wraps


# Decorator  factories return decorators (which are parameterized)
def timed(reps):
    
    def dec(fn): # actual decorator
        from time import perf_counter
        

        @wraps(fn)
        def inner(*args, **kwargs):
            print(f"Calling {fn.__name__}")
            total_elapsed = 0
            res =  0
            for _ in range(reps):
                start = perf_counter()
                res = fn(*args, **kwargs)
                run_time =perf_counter()-start 
                print(run_time)
                total_elapsed += run_time
            avg_elapsed = total_elapsed / reps
            print(f"Average Runtime is : {avg_elapsed:.6f}")
            return res
        return inner
    return dec


@lru_cache()
def cal_fib_recurse(n):
    return 1 if n <3 else cal_fib_recurse(n-2) + cal_fib_recurse(n-1)


@timed(500) # are decorator factories
def fib(n):
    return cal_fib_recurse(n)

fib(300)