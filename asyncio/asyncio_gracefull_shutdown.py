import asyncio
from signal import SIGTERM, SIGINT
from contextlib_asyncio import call_simulate_io_operation_sync



async def main():
    loop = asyncio.get_running_loop()

    for sig in (SIGTERM,SIGINT):
        print(sig)
        loop.add_signal_handler(sig, handler,sig)
    
    try:
        while True:
            print("App is running")
            data = await asyncio.to_thread(call_simulate_io_operation_sync,2,"http://localhost:8000/api/simulate-io-operation")
            print(data)
    except asyncio.CancelledError:
        for i in range(3):
            print("App is shutting down")
            await asyncio.sleep(1)

def handler(sig):
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()

    print(f"{sig=}, Shutting donw")
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT,lambda:None)

if __name__ == "__main__":
    asyncio.run(main())