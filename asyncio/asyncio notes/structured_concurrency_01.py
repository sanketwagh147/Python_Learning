import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import http
import time
from typing import Iterable 

from blocking_code import simulate_io_operation, simulate_io_operation_sync,simulate_http_error, simulate_http_error_sync, simulate_cpu_bound_task


async def get_data() -> None:

    try:
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(simulate_io_operation("first task"))
            t2= tg.create_task(simulate_io_operation("second task", delay=2))
            t3 = tg.create_task(simulate_io_operation("third task", delay=3))
            t4 = tg.create_task(simulate_io_operation("fourth task", delay=4))
            t5 = tg.create_task(simulate_io_operation("fifth task", delay=5))
            t6 = tg.create_task(asyncio.to_thread(simulate_io_operation_sync, "sixth task", delay=6))
            # t6 = tg.create_task(simulate_http_error(503))
    except* Exception as e:
        print("An error occurred:")

    print("task 1 result:", t1.result())
    print("task 2 result:", t2.result())
    print("task 3 result:", t3.result())
    print("task 4 result:", t4.result())
    print("task 5 result:", t5.result())
    print("task 6 result:", t6.result())
    print("All tasks completed")


async def demonstrate_timeout_and_cancellation() -> None:
    print("\n--- Starting Timeout & Cancellation Example ---")
    try:
        # Set a timeout of 2.5 seconds for the entire block
        async with asyncio.timeout(2.5):
            async with asyncio.TaskGroup() as tg:
                # This task finishes in 1s (within timeout)
                t1 = tg.create_task(simulate_io_operation("fast task", delay=1))
                # This task finishes in 5s (will be CANCELLED)
                t2 = tg.create_task(simulate_io_operation("slow task", delay=5))
    
    except TimeoutError:
        print("\n\U000023F0  Timeout triggered! 'slow task' was cancelled.")
    
    # Check results (t2 will be cancelled, so no result)
    if not t1.cancelled():
        print(f"Fast task result: {t1.result()}")
    
    print("--- End Example ---\n")


async def run_in_process_pool(numbers:Iterable[int])-> list[int]:

    def success_callback(task,msg):
        print(f"Done: {msg}")

    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as pool:
        
        tasks: list[asyncio.Future[int]] = [loop.run_in_executor(pool, simulate_cpu_bound_task,"test", n) for n in numbers]
        for task in tasks:
            task.add_done_callback(partial(success_callback, msg="done"))

        results = await asyncio.gather(*tasks)

        return results

async def main():
    start_time = time.perf_counter()
    
    # Run the timeout/cancellation example
    # await demonstrate_timeout_and_cancellation()

    # await get_data()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(get_data())
        tg.create_task(run_in_process_pool([1,2,3,4,5,6]))

    # Using process pool

    # simulate_cpu_bound_task("task",1)
    # simulate_cpu_bound_task("task",2)
    # simulate_cpu_bound_task("task",3)
    # for each in result:
    #     print(each)


    print(f"Finished in {time.perf_counter() - start_time}")
    

if __name__ == "__main__":
    asyncio.run(main())