from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from functools import wraps
from threading import RLock
import time
from typing import Any, Callable, ParamSpec, TypeVar, cast


P = ParamSpec("P")
R = TypeVar("R")

DEFAULT_BACKGROUND_MAX_WORKERS = 4
DEFAULT_MAX_PENDING_RETRIES = 32

_ExecutorKey = tuple[int, str, int]
_EXECUTORS: dict[_ExecutorKey, ThreadPoolExecutor] = {}
_PENDING_FUTURES: dict[_ExecutorKey, deque[Future[Any]]] = {}
_EXECUTOR_LOCK = RLock()


def _normalize_exceptions(
    exceptions: tuple[type[Exception], ...] | None,
) -> tuple[type[Exception], ...]:
    handled_exceptions = exceptions or (Exception,)

    if not handled_exceptions:
        raise ValueError("exceptions cannot be empty")

    if any(not issubclass(exc, Exception) for exc in handled_exceptions):
        raise TypeError("exceptions must be a tuple of Exception classes")

    return handled_exceptions


def _validate_retry_config(max_attempts: int, backoff_factor: float) -> None:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    if backoff_factor < 0:
        raise ValueError("backoff_factor cannot be negative")


def _run_with_retry(
    fn: Callable[..., R],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    max_attempts: int,
    backoff_factor: float,
    handled_exceptions: tuple[type[Exception], ...],
) -> R:
    for attempt in range(1, max_attempts + 1):
        try:
            return fn(*args, **kwargs)
        except handled_exceptions as exc:
            if attempt < max_attempts:
                wait = backoff_factor * (2 ** (attempt - 1))

                print(f"[Retrying] {fn.__name__} attempt {attempt} failed: {exc}")
                print(f"Retrying in {wait:.1f}s...")
                time.sleep(wait)
            else:
                print(f"[Retrying] {fn.__name__} failed after {max_attempts=}")
                raise

    raise RuntimeError("retry loop exited unexpectedly")


def _get_executor(key: _ExecutorKey) -> ThreadPoolExecutor:
    with _EXECUTOR_LOCK:
        executor = _EXECUTORS.get(key)
        if executor is None:
            max_workers, thread_name_prefix, _ = key
            executor = ThreadPoolExecutor(
                max_workers=max_workers,
                thread_name_prefix=thread_name_prefix,
            )
            _EXECUTORS[key] = executor
            _PENDING_FUTURES[key] = deque()
        return executor


def _prune_completed_futures(pending_futures: deque[Future[Any]]) -> None:
    completed_futures = [future for future in pending_futures if future.done()]
    for completed_future in completed_futures:
        try:
            pending_futures.remove(completed_future)
        except ValueError:
            pass


def _drop_oldest_queued_future(pending_futures: deque[Future[Any]]) -> bool:
    for future in list(pending_futures):
        if future.done():
            try:
                pending_futures.remove(future)
            except ValueError:
                pass
            continue

        if future.cancel():
            try:
                pending_futures.remove(future)
            except ValueError:
                pass

            print("[Retrying] Dropped the oldest queued background retry")
            return True

    return False


def _remove_future(key: _ExecutorKey, completed_future: Future[Any]) -> None:
    with _EXECUTOR_LOCK:
        pending_futures = _PENDING_FUTURES.get(key)
        if pending_futures is None:
            return

        try:
            pending_futures.remove(completed_future)
        except ValueError:
            pass


def _submit_background_retry(
    fn: Callable[..., R],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    max_attempts: int,
    backoff_factor: float,
    handled_exceptions: tuple[type[Exception], ...],
    max_workers: int,
    max_pending_retries: int,
    thread_name_prefix: str,
) -> Future[R]:
    if max_workers < 1:
        raise ValueError("max_workers must be at least 1")

    if max_pending_retries < 1:
        raise ValueError("max_pending_retries must be at least 1")

    key: _ExecutorKey = (max_workers, thread_name_prefix, max_pending_retries)
    executor = _get_executor(key)

    with _EXECUTOR_LOCK:
        pending_futures = _PENDING_FUTURES[key]
        _prune_completed_futures(pending_futures)

        if len(
            pending_futures
        ) >= max_pending_retries and not _drop_oldest_queued_future(pending_futures):
            raise RuntimeError(
                "background retry queue is full and all pending retries are already running"
            )

        future = executor.submit(
            _run_with_retry,
            fn,
            args,
            kwargs,
            max_attempts=max_attempts,
            backoff_factor=backoff_factor,
            handled_exceptions=handled_exceptions,
        )
        pending_futures.append(future)

    future.add_done_callback(
        lambda completed_future: _remove_future(key, completed_future)
    )
    return cast(Future[R], future)


def retry(
    max_attempts: int = 3,
    backoff_factor: float = 0.5,
    exceptions: tuple[type[Exception], ...] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    handled_exceptions = _normalize_exceptions(exceptions)
    _validate_retry_config(max_attempts, backoff_factor)

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return _run_with_retry(
                fn,
                args,
                kwargs,
                max_attempts=max_attempts,
                backoff_factor=backoff_factor,
                handled_exceptions=handled_exceptions,
            )

        return wrapper

    return decorator


def retry_in_background(
    max_attempts: int = 3,
    backoff_factor: float = 0.5,
    exceptions: tuple[type[Exception], ...] | None = None,
    *,
    max_workers: int = DEFAULT_BACKGROUND_MAX_WORKERS,
    max_pending_retries: int = DEFAULT_MAX_PENDING_RETRIES,
    thread_name_prefix: str = "retry-worker",
) -> Callable[[Callable[P, R]], Callable[P, Future[R]]]:
    handled_exceptions = _normalize_exceptions(exceptions)
    _validate_retry_config(max_attempts, backoff_factor)

    def decorator(fn: Callable[P, R]) -> Callable[P, Future[R]]:

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Future[R]:
            return _submit_background_retry(
                fn,
                args,
                kwargs,
                max_attempts=max_attempts,
                backoff_factor=backoff_factor,
                handled_exceptions=handled_exceptions,
                max_workers=max_workers,
                max_pending_retries=max_pending_retries,
                thread_name_prefix=thread_name_prefix,
            )

        return wrapper

    return decorator
