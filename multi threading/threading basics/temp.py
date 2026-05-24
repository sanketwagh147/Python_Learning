import threading
import time


def foo(secs):
    current_thread = threading.current_thread()
    print(f"{current_thread.name=} : {current_thread.ident}")
    time.sleep(secs)
    print(f"{current_thread.name} Finished")


def multithread_foo():

    t1 = threading.Thread(target=foo, name="T1", args=[2])
    t2 = threading.Thread(target=foo, name="T2", args=[5])

    t1.start()
    t2.start()

    # Without join it will continue executing
    t1.join()
    print("Waiting")

    # t2.join()


if __name__ == "__main__":
    multithread_foo()
    print("Main finished")
