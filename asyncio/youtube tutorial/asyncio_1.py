from hmac import new
import time
import asyncio

from blocking_code import simulate_io_operation, simulate_io_operation_sync
from functools import partial


async def error_fn():
    await asyncio.sleep(1)
    raise ValueError("This is an error from error_fn")


def task_done_callback(task: asyncio.Task,task_type,inputs):
    print(f"Task name is {task.get_name()} and {task_type=} callback called with inputs:")

async def main():

    start = time.time()
    # result = sync_function()


    # future = asyncio.ensure_future(simulate_io_operation())
    # future_result = await future
    # print(future_result)

    # Or using Task which is sub class of Future

    loop  = asyncio.get_running_loop()
    results = []
    tasks = []

    # for i in range(1,10):
    #     # Create task schedules the coroutine
    #     # If a async def function is called it will only return the coroutine  and return only when await is called on it but create task handles this internally
    #     task = loop.create_task(simulate_io_operation(delay=i))
    #     task.set_name(f"create_task-{i}")
    #     cb = partial(task_done_callback,task_type="create_task",inputs=i)
    #     task.add_done_callback(cb)
    #     tasks.append(task)

    # for i in range(1,10):
    #     # This will run the sync function in a separate thread and return a coroutine which can be awaited
    #     new_thread = asyncio.to_thread(simulate_io_operation_sync, delay=i)
    #     # print(type(new_thread))
    #     task = loop.create_task(new_thread)
    #     task.set_name(f"to_thread-{i}")
    #     cb = partial(task_done_callback,task_type="to_thread",inputs=i)
    #     task.add_done_callback(cb)
    #     tasks.append(task)

    # Using Gather
    # new_tasks = [asyncio.create_task(simulate_io_operation(delay=i)) for i in range(1,10)]

    # new_tasks.insert(0,asyncio.create_task(error_fn()))

    # for task in new_tasks:
    #     task.set_name(f"gather-{task.get_name()}")
    #     cb = partial(task_done_callback,task_type="gather",inputs=task)
    #     task.add_done_callback(cb)

    # tasks.extend(new_tasks)
    


    # for task in tasks:
    #     result =  await task
    #     results.append(resulte

    # if tasks needs to fail or succeed together use Task groups
    async with asyncio.TaskGroup() as tg:
        tg_tasks = [tg.create_task(simulate_io_operation(delay=i)) for i in range(1,10)]
        for task in tg_tasks:
            task.set_name(f"task-group-{task.get_name()}")
            cb = partial(task_done_callback,task_type="task-group",inputs=task)
            task.add_done_callback(cb)
        # awaits after exiting the context manager


    results = await asyncio.gather(*tasks, return_exceptions=True)

        
    # task_result = await task
    # print(results)

    ## In python there are mainly 3 types of awaitables
    # - coroutines
    # - tasks
    # - futures

    print(f"Execution :  (took {time.time() - start:.2f} seconds)")

    

    
if __name__ == "__main__":
    asyncio.run(main())