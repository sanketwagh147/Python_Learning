# Threading Basics

A comprehensive guide to fundamental threading concepts in Python.

## 📚 Contents

1. **[Thread Naming & Identification](1_thread_naming_and_identification.md)**
   - How to name and identify threads
   - Using `threading.current_thread()`
   - Listing active threads
   - Thread IDs and identification

2. **[Thread States](2_thread_states.md)**
   - Understanding thread lifecycle
   - Using `is_alive()` to check thread state
   - Monitoring thread execution
   - Thread timeouts

3. **[Daemon vs Non-Daemon Threads](3_daemon_vs_non_daemon_threads.md)**
   - Differences between daemon and non-daemon threads
   - When to use each type
   - Program exit behavior
   - Background services pattern

4. **[Thread Synchronization: Locks](4_thread_synchronization_locks.md)**
   - Understanding race conditions
   - Using `threading.Lock()`
   - Critical sections
   - Preventing deadlocks

5. **[Thread-Safe Operations](5_thread_safe_operations_and_race_conditions.md)**
   - Atomic vs non-atomic operations
   - Common race condition patterns
   - Thread-safe data structures
   - Best practices for shared state

6. **[Exception Handling](6_exception_handling_in_threads.md)**
   - How exceptions work in threads
   - Catching and propagating exceptions
   - Error communication between threads
   - Global exception hooks

## 🚀 Quick Start

Start with [Thread Naming & Identification](1_thread_naming_and_identification.md) if you're new to threading, or jump to any topic based on your needs.

## 📋 Prerequisites

- Basic Python knowledge
- Understanding of functions and classes
- Familiarity with the `threading` module basics

## 💡 Learning Path

For beginners, we recommend this order:

1. Thread Naming & Identification → Understand how to work with thread objects
2. Thread States → Learn the lifecycle and monitoring
3. Daemon vs Non-Daemon → Understand thread types and program behavior
4. Thread Synchronization → Learn to prevent race conditions
5. Thread-Safe Operations → Understand what's safe and what's not
6. Exception Handling → Handle errors properly in threads

## 🎯 Key Takeaways

- **Thread naming** helps with debugging and monitoring
- **Thread states** help track execution and completion
- **Daemon threads** don't block program exit
- **Locks** prevent race conditions and data corruption
- **Not all operations are thread-safe** - know which are atomic
- **Exceptions in threads** don't propagate to main thread automatically

## 🔗 Related Topics

After mastering these basics, explore:
- Thread pools (`concurrent.futures`)
- Advanced synchronization (Semaphores, Events, Conditions)
- Thread-local storage
- Multiprocessing vs Threading
- Async/await and asyncio

## 📖 Additional Resources

- [Python threading documentation](https://docs.python.org/3/library/threading.html)
- [concurrent.futures documentation](https://docs.python.org/3/library/concurrent.futures.html)
- Global Interpreter Lock (GIL) considerations

---

**Note**: All examples in this guide are tested with Python 3.8+. Some features (like `threading.excepthook`) are only available in Python 3.8 and later.
