# Thread States and Lifecycle

## Thread Lifecycle
# Created → Started → Running → Finished

# 1. **Created**: Thread object is created but not yet started
# . **Started**: `start()` is called, thread is scheduled to run
# . **Running**: Thread is actively executing its target function
# . **Finished**: Thread has completed execution

## Key Method: `is_alive()`
import threading
import time
import logging

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


def worker(duration):
    logging.info(f"Worker started running for {duration=}")
    time.sleep(duration)
    logging.info("work is finished")


def check_thread_status(duration):

    # Step 1 : Create thread
    thread = threading.Thread(target=worker, args=(duration,), name=worker.__name__)

    # thread is created but not started
    print(f"{thread.is_alive()=}")

    # step 2 : Start thread
    thread.start()
    print(f"{thread.is_alive()=}")
    start_time = time.time()

    while time.time() - start_time < 7:
        print(f"{thread.is_alive()=}")
        time.sleep(1)

    print(f"{thread.is_alive()=} Still")

    # Wait for completion
    thread.join()
    print("Thread working complete")
    print(f"{thread.is_alive()=}")


def monitor_multiple_thread():

    def task(task_id, duration):
        task_id = f"Task-Id-{task_id}, {duration=}"
        logging.info(f"{task_id=} Started")
        time.sleep(duration)

    threads = []

    for i in range(5):
        t = threading.Thread(target=task, args=(i + 1, i + 5), name=f"Task-Id-{i + 1}")
        threads.append(t)
        t.start()

    # Monitor thread states
    while any(t.is_alive() for t in threads):
        alive_threads = [t.name for t in threads if t.is_alive()]
        logging.info(f"Pending threads: {', '.join(alive_threads)}")
        time.sleep(1)

    logging.info("All threads ran successfully")


def thread_timeout_example():

    def long_running_task():
        logging.info("Long running task strted")
        time.sleep(10)
        logging.info("Complted long running task")

    thread = threading.Thread(target=long_running_task,name="LongTask")
    thread.start()

    timeout = 3
    logging.info(f"Waiting for thread {timeout=} seconds")
    thread.join(timeout)

    if thread.is_alive():
        logging.info(f"Thread is still running after {timeout=} seconds continue other work")
    else:
        logging.info("Thread completed within timeout")

def progress_task():
    
    class ProgressTask:
        
        def __init__(self) -> None:
            self.progress = 0
            self.running = False

        def run(self):
            self.running = True

            for i in range(1,11):
                time.sleep(0.5)
                self.progress = i * 10
            self.running = False

        def get_progress(self):
            return self.progress

    task = ProgressTask()
    thread = threading.Thread(target=task.run, name="ProgressTask")
    thread.start()

    while thread.is_alive():
        logging.info(f"Progress : {task.get_progress()} %")
        time.sleep(1)

    thread.join()
    logging.info(f"Final progress: {task.get_progress()}%")
    logging.info("Task completed")


def main():
    # check_thread_status(10)
    # monitor_multiple_thread()
    # thread_timeout_example()
    progress_task()
    ...


if __name__ == "__main__":
    main()
