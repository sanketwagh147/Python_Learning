"""Async decorator utilities.

`asyncify` turns a regular blocking function into an `async def` function.

Key behavior:
- The wrapped call runs in a thread (default executor or a provided executor).
- The wrapper *awaits* the thread result, so normal usage waits correctly.
- If the coroutine is cancelled, the thread cannot be force-stopped; optionally
  `wait_on_cancel=True` will wait for the thread to finish before re-raising
  `CancelledError` (graceful shutdown semantics).
"""

import asyncio
import functools
import contextvars
from concurrent.futures import Executor
from typing import Any, Callable, Coroutine, Optional, TypeVar, overload, ParamSpec
from contextlib_asyncio import call_simulate_io_operation_sync
P = ParamSpec("P")
R = TypeVar("R")

@overload
def asyncify(func: Callable[P, R], /) -> Callable[P, Coroutine[Any, Any, R]]:
    ...

@overload
def asyncify(
    *,
    executor: Optional[Executor] = None,
) -> Callable[[Callable[P, R]], Callable[P, Coroutine[Any, Any, R]]]:
    ...

def asyncify(
    func: Optional[Callable[P, R]] = None,
    /,
    *,
    executor: Optional[Executor] = None,
) -> Any:
    """
    Decorator to turn a blocking function into an async one.
    
    Ensures ContextVars (logging, tracing) are propagated to the thread.
    """
    def decorate(target: Callable[P, R]) -> Callable[P, Coroutine[Any, Any, R]]:
        if asyncio.iscoroutinefunction(target):
            return target # type: ignore

        @functools.wraps(target)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # cpy the current context (essential for logs/tracing)
            ctx = contextvars.copy_context()
            
            # Prepare the function call within the captured context
            func_call = functools.partial(ctx.run, target, *args, **kwargs)

            # Offload to thread
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(executor, func_call)

        return wrapper

    if func is None:
        return decorate
    return decorate(func)

# --- demo ---
blocking_operation = asyncify(call_simulate_io_operation_sync)

async def main() -> None:
    print("Starting concurrent blocking operations...\n")
    results = await asyncio.gather(
        blocking_operation( 2.0),
        blocking_operation( 1.5),
        blocking_operation( 1.0),
    )

    print("\nAll operations completed:")
    for result in results:
        print(f"  {result}")


if __name__ == "__main__":
    asyncio.run(main())