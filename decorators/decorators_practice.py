"""
Docstring for decorators.decorators_practice
"""

from functools import wraps
import time
import timeit
from turtle import st
from loguru import logger



def time_it(fn):
    
    
    @wraps(fn)
    def decorator(*args,**kwargs):

        start_time = time.perf_counter()

        result = fn(*args,**kwargs)

        elapsed_time = time.perf_counter() - start_time
        logger.debug(f"Time taken to run {fn.__module__}.{fn.__name__} function is {elapsed_time:.4f} seconds")

        return result

    return decorator

def cache_me(fn):
    
    _cache = {}

    @wraps(fn)
    def decorator(*args):
        
        if args in _cache:
            logger.info(f"Fetching from cache for args: {args}")
            return _cache[args]

        else:
            logger.info(f"Calculating result for args: {args}")
            result = fn(*args)
            _cache[args] = result

            return result

    return decorator

@time_it
@cache_me
def sum_it_up(*args):
    time.sleep(len(args))  # Simulating a time-consuming computation
    return sum(*args)
    
    

    
@time_it
def caller():
    time.sleep(5)
    
if __name__ == "__main__":
    

    # caller()
    print(sum_it_up((1,2,3,4,5)))
    print(sum_it_up((10,20,30)))    
    print(sum_it_up((1,2,3,4,5))) 
    print(sum_it_up((10,20,30)))
    print(sum_it_up((1,2,3,4,5))) 
        