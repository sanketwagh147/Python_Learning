from asyncio import Future,sleep
import asyncio


async def coroutine(f:Future):
    await sleep(3.0)
    return f.set_result("Done")

    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = Future()
    task = loop.create_task(coroutine(future))
    print(type(task))

    # def cb(task):
    #     return future.set_result(task.result())

    # task.add_done_callback(lambda f: future.set_result(f.result()))
    # task.add_done_callback(cb)
    print(future.done())
    result = loop.run_until_complete(future)
        
    print(future.done())
    print(future.result())