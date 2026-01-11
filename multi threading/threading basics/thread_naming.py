import threading
from datetime import timedelta, datetime
import time

from Marklutz_bookcode.moda import f

def worker(name:str, time_in_seconds):
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=time_in_seconds)

    while datetime.now() < end_time:
        print(f"Running Worker {name}")
        current_thread = thread
        print(f"Current Thread Name: {threading.current_thread().name} | Worker Name: {name} | identifier: {threading.current_thread().ident}")
        time.sleep(0.5)
        
    

if __name__ == "__main__":
    # worker("Worker-1",10)
    num_workers = 4

    start_time = time.perf_counter()
    threads = []
    for i in range(num_workers):
        thread = threading.Thread(
            target=worker,
            kwargs={"name":f"Worker-{i+1}","time_in_seconds": (i+1)*i+5},
            name=f"Worker-{i+1}"  # Add this to set the thread name
        )
        thread.start()
        threads.append(thread)
        # thread.join()
    

    # for thread in threading.enumerate(): # Wait for all threads to complete including main thread
    for thread in threads:
        thread.join()

    print("All workers completed.",)
    print(f"Total time taken: {time.perf_counter() - start_time}")
        