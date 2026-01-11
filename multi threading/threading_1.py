import threading
import time

def print_numbers():
    for i in range(5):
        print(f"Number: {i}")
        time.sleep(1)

def print_letters():
    for letter in 'ABCDE':
        print(f"Letter: {letter}")
        time.sleep(1)

def heavy_computation():
    total = 0
    for i in range(10**6):
        time.sleep(0.00001)  # Simulate a time-consuming task
        total += i
    print(f"Heavy computation result: {total}")
    



"""
Key Thread Methods:
-------------------
- thread.start()    : Begin executing the thread's target function
- thread.join()     : Block until the thread completes
- thread.is_alive() : Check if thread is still running
- threading.current_thread() : Get reference to current thread
"""

if __name__ == "__main__":
    
    # Without threads (sequential) - takes 10 seconds:
    # print_numbers()
    # print_letters()

    # With threads (concurrent) - takes ~5 seconds:
    thread1 = threading.Thread(target=print_numbers)
    thread2 = threading.Thread(target=print_letters)
    thread3 = threading.Thread(target=heavy_computation,daemon=True) #     # DAEMON (daemon=True)
    # Program will exit after main code finishes, killing this daemon thread. This will not block program exit.

    thread3.start()  # Start thread3
    thread1.start()  # Start thread1
    thread2.start()  # Start thread2

    thread1.join()   # Wait for thread1 to finish
    thread2.join()   # Wait for thread2 to finish
    # thread3.join()   # Wait for thread3 to finish
    print("All threads completed.")