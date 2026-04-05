import threading
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from statistics import mean
from time import perf_counter
from typing import Callable

from sqlalchemy import text

from common.db import session_scope

SQL_EXCHANGES = "select * from stic.exchanges;"
SQL_SYMBOLS = "select * from stic.symbols;"
PRICE_DAILY = "select * from stic.prices_daily pd  order by date desc limit 1;"
VERBOSE_THREAD_LOGS = False



def log_thread_info(func):
    """Decorator to print thread identity and row count for DB fetch functions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        rows = func(*args, **kwargs)
        if VERBOSE_THREAD_LOGS:
            print(
                f"[{func.__name__}] name={threading.current_thread().name} "
                f"id={threading.get_ident()} rows={len(rows)}"
            )
        return rows

    return wrapper


@log_thread_info
def fetch_exchanges() -> list[dict]:
    """Run the exchanges query inside a thread-local sync session."""
    with session_scope() as db_session:
        rows = db_session.execute(text(SQL_EXCHANGES)).mappings().all()
        return [dict(row) for row in rows]


@log_thread_info
def fetch_symbols() -> list[dict]:
    """Run the symbols query inside a thread-local sync session."""
    with session_scope() as db_session:
        rows = db_session.execute(text(SQL_SYMBOLS)).mappings().all()
        return [dict(row) for row in rows]


@log_thread_info
def fetch_price_daily() -> list[dict]:
    """Run the query inside a thread-local sync session."""
    with session_scope() as db_session:
        rows = db_session.execute(text(PRICE_DAILY)).mappings().all()
        return [dict(row) for row in rows]

def timed_task(task: Callable[[], list[dict]]) -> tuple[str, int, float]:
    """Return task name, row count, and task duration in seconds."""
    started = perf_counter()
    rows = task()
    duration = perf_counter() - started
    return task.__name__, len(rows), duration


def run_sequential() -> tuple[int, list[tuple[str, int, float]], float]:
    tasks = [fetch_exchanges, fetch_symbols, fetch_price_daily]
    started = perf_counter()
    per_task = [timed_task(task) for task in tasks]
    total = perf_counter() - started
    total_rows = sum(row_count for _, row_count, _ in per_task)
    return total_rows, per_task, total


def run_threaded() -> tuple[int, list[tuple[str, int, float]], float]:
    tasks = [fetch_exchanges, fetch_symbols, fetch_price_daily]
    started = perf_counter()

    with ThreadPoolExecutor(max_workers=3, thread_name_prefix="db-worker") as pool:
        futures = [pool.submit(timed_task, task) for task in tasks]
        per_task = [future.result() for future in futures]

    total = perf_counter() - started
    total_rows = sum(row_count for _, row_count, _ in per_task)
    return total_rows, per_task, total


def benchmark(runs: int = 5) -> None:
    threaded_totals: list[float] = []
    sequential_totals: list[float] = []

    print(f"Running benchmark for {runs} runs...")
    for run_number in range(1, runs + 1):
        seq_rows, seq_per_task, seq_total = run_sequential()
        th_rows, th_per_task, th_total = run_threaded()

        sequential_totals.append(seq_total)
        threaded_totals.append(th_total)

        print(f"\\nRun {run_number}")
        print(f"  sequential: {seq_total:.4f}s, rows={seq_rows}")
        for name, rows, duration in seq_per_task:
            print(f"    - {name}: {duration:.4f}s, rows={rows}")
        print(f"  threaded:   {th_total:.4f}s, rows={th_rows}")
        for name, rows, duration in th_per_task:
            print(f"    - {name}: {duration:.4f}s, rows={rows}")

    print("\nSummary")
    print(
        "  sequential total: "
        f"min={min(sequential_totals):.4f}s "
        f"avg={mean(sequential_totals):.4f}s "
        f"max={max(sequential_totals):.4f}s"
    )
    print(
        "  threaded total:   "
        f"min={min(threaded_totals):.4f}s "
        f"avg={mean(threaded_totals):.4f}s "
        f"max={max(threaded_totals):.4f}s"
    )


if __name__ == "__main__":
    benchmark(runs=5)