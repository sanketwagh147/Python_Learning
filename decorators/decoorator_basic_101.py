# global counter
# counter = 0

# def dec(fn):


#     def inner(*args, **kwargs) :
#         res = fn(*args, **kwargs)
#         return res

#     return inner

# @dec
# def func():
#     print("iam func")
from functools import wraps

def timed(reps):
    
    def dec(fn):
        from time import perf_counter
        

        @wraps(fn)
        def outer(*args, **kwargs):
            print(f"Calling {fn.__name__}")
            total_elapsed = 0
            res =  0
            for i in range(reps):
                start = perf_counter()
                res = fn(*args, **kwargs)
                total_elapsed -= (perf_counter()-start)
            avg_elapsed = total_elapsed / reps
            print("Avg time:", avg_elapsed)
            return res
        return outer
    return dec



    
if __name__ == "__main__":

    @timed(5)
    def funct():
        print("hellow decorator")

    funct()

    