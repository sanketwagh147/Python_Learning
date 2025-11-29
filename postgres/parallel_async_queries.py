"""
Parallel Async Queries Example
==============================

Problem: You have 4 heavy/slow queries that are INDEPENDENT of each other.
         Running them sequentially takes: T1 + T2 + T3 + T4 = total time
         
Solution: Run them in parallel using asyncio.gather()
          Total time = max(T1, T2, T3, T4)

IMPORTANT: AsyncSession is NOT thread-safe and should NOT be shared across tasks!
           Each parallel task MUST have its own session instance.

Author: Sanket Wagh
Date: November 2025
"""

import asyncio
import time
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Import your existing pool helper
from async_db_pool import AsyncDBPool, DBConfig


# =============================================================================
# WRONG WAY ❌ - Sharing session across parallel tasks
# =============================================================================
async def wrong_parallel_queries_shared_session():
    """
    ❌ WRONG: This shares a single session across multiple tasks.
    
    AsyncSession is NOT thread-safe / task-safe!
    This can cause:
    - Race conditions
    - Connection errors
    - Data corruption
    - Unexpected exceptions
    """
    async with AsyncDBPool.get_session() as session:  # Single shared session
        # DON'T DO THIS!
        results = await asyncio.gather(
            heavy_query_1(session),  # ❌ Shared session
            heavy_query_2(session),  # ❌ Shared session
            heavy_query_3(session),  # ❌ Shared session
            heavy_query_4(session),  # ❌ Shared session
        )
    return results


# =============================================================================
# CORRECT WAY ✅ - Each task gets its own session
# =============================================================================
async def correct_parallel_queries():
    """
    ✅ CORRECT: Each task creates its own session from the pool.
    
    This is safe because:
    - Each task has its own isolated session
    - The connection pool manages concurrent connections
    - No race conditions or shared state issues
    
    Time taken = max(query1_time, query2_time, query3_time, query4_time)
    Instead of = query1_time + query2_time + query3_time + query4_time
    """
    start = time.perf_counter()
    
    # Each function creates its own session internally
    results = await asyncio.gather(
        fetch_users_report(),      # ~2 seconds
        fetch_orders_summary(),    # ~3 seconds  
        fetch_inventory_stats(),   # ~1.5 seconds
        fetch_analytics_data(),    # ~2.5 seconds
    )
    
    elapsed = time.perf_counter() - start
    print(f"\n✅ Parallel execution completed in {elapsed:.2f} seconds")
    print(f"   (Sequential would take ~9 seconds)")
    
    users, orders, inventory, analytics = results
    return {
        "users": users,
        "orders": orders,
        "inventory": inventory,
        "analytics": analytics,
    }


# =============================================================================
# Individual Query Functions - Each with its OWN session
# =============================================================================

async def fetch_users_report() -> dict[str, Any]:
    """
    Heavy query 1: Fetch users report
    Simulates ~2 second query
    """
    async with AsyncDBPool.get_session() as session:  # ✅ Own session
        start = time.perf_counter()
        
        # Simulate heavy query with pg_sleep
        # Replace with your actual query
        result = await session.execute(
            text("SELECT pg_sleep(2), 'users_report' as report_type")
        )
        # Or your actual query:
        # result = await session.execute(
        #     text("""
        #         SELECT u.*, COUNT(o.id) as order_count
        #         FROM users u
        #         LEFT JOIN orders o ON u.id = o.user_id
        #         GROUP BY u.id
        #         -- Heavy aggregation...
        #     """)
        # )
        
        elapsed = time.perf_counter() - start
        print(f"  📊 Users report completed in {elapsed:.2f}s")
        
        return {"report": "users", "time": elapsed, "data": "..."}


async def fetch_orders_summary() -> dict[str, Any]:
    """
    Heavy query 2: Fetch orders summary
    Simulates ~3 second query (the slowest)
    """
    async with AsyncDBPool.get_session() as session:  # ✅ Own session
        start = time.perf_counter()
        
        result = await session.execute(
            text("SELECT pg_sleep(3), 'orders_summary' as report_type")
        )
        
        elapsed = time.perf_counter() - start
        print(f"  📦 Orders summary completed in {elapsed:.2f}s")
        
        return {"report": "orders", "time": elapsed, "data": "..."}


async def fetch_inventory_stats() -> dict[str, Any]:
    """
    Heavy query 3: Fetch inventory statistics
    Simulates ~1.5 second query (the fastest)
    """
    async with AsyncDBPool.get_session() as session:  # ✅ Own session
        start = time.perf_counter()
        
        result = await session.execute(
            text("SELECT pg_sleep(1.5), 'inventory_stats' as report_type")
        )
        
        elapsed = time.perf_counter() - start
        print(f"  📈 Inventory stats completed in {elapsed:.2f}s")
        
        return {"report": "inventory", "time": elapsed, "data": "..."}


async def fetch_analytics_data() -> dict[str, Any]:
    """
    Heavy query 4: Fetch analytics data
    Simulates ~2.5 second query
    """
    async with AsyncDBPool.get_session() as session:  # ✅ Own session
        start = time.perf_counter()
        
        result = await session.execute(
            text("SELECT pg_sleep(2.5), 'analytics' as report_type")
        )
        
        elapsed = time.perf_counter() - start
        print(f"  📉 Analytics data completed in {elapsed:.2f}s")
        
        return {"report": "analytics", "time": elapsed, "data": "..."}


# =============================================================================
# Alternative Pattern: Pass session maker, not session
# =============================================================================

async def parallel_with_session_factory():
    """
    Alternative pattern where you pass the session factory.
    Useful when you want to keep query functions more flexible.
    """
    # Get the session maker from pool
    if AsyncDBPool._maker is None:
        raise RuntimeError("Pool not initialized")
    
    session_maker = AsyncDBPool._maker
    
    async def query_with_own_session(query: str, label: str):
        """Helper that creates its own session"""
        async with session_maker() as session:
            result = await session.execute(text(query))
            return result.fetchall()
    
    results = await asyncio.gather(
        query_with_own_session("SELECT pg_sleep(1), 1", "query1"),
        query_with_own_session("SELECT pg_sleep(1), 2", "query2"),
        query_with_own_session("SELECT pg_sleep(1), 3", "query3"),
    )
    
    return results


# =============================================================================
# Sequential vs Parallel Comparison
# =============================================================================

async def sequential_queries():
    """
    ❌ SLOW: Sequential execution
    Total time = 2 + 3 + 1.5 + 2.5 = 9 seconds
    """
    start = time.perf_counter()
    
    users = await fetch_users_report()
    orders = await fetch_orders_summary()
    inventory = await fetch_inventory_stats()
    analytics = await fetch_analytics_data()
    
    elapsed = time.perf_counter() - start
    print(f"\n❌ Sequential execution completed in {elapsed:.2f} seconds")
    
    return {"users": users, "orders": orders, "inventory": inventory, "analytics": analytics}


# =============================================================================
# Main - Demo
# =============================================================================

async def main():
    """Run the demo comparing sequential vs parallel execution."""
    
    # Initialize the pool with your database config
    config = DBConfig(
        database_url="postgresql+asyncpg://user:password@localhost:5432/mydb",
        pool_size=5,      # Need enough connections for parallel queries!
        max_overflow=10,
    )
    await AsyncDBPool.init(config=config)
    
    try:
        print("=" * 60)
        print("PARALLEL ASYNC QUERIES DEMO")
        print("=" * 60)
        
        print("\n🔄 Running queries in PARALLEL...")
        parallel_result = await correct_parallel_queries()
        
        print("\n" + "-" * 60)
        
        print("\n⏳ Running queries SEQUENTIALLY...")
        sequential_result = await sequential_queries()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("""
        Query Times:
        - Users Report:    ~2.0s
        - Orders Summary:  ~3.0s (slowest)
        - Inventory Stats: ~1.5s
        - Analytics Data:  ~2.5s
        
        Sequential: 2 + 3 + 1.5 + 2.5 = ~9.0 seconds
        Parallel:   max(2, 3, 1.5, 2.5) = ~3.0 seconds
        
        Speedup: 3x faster! 🚀
        """)
        
    finally:
        await AsyncDBPool.dispose()


if __name__ == "__main__":
    asyncio.run(main())
