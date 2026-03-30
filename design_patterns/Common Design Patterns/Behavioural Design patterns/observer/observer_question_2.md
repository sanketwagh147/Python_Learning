# Observer Pattern — Question 2 (Medium)

## Problem: Event-Driven Stock Trading System

A stock market publishes price changes. Multiple trading algorithms subscribe to specific stocks and react to price movements.

### Requirements

#### Subject
```python
class StockMarket:
    def subscribe(self, stock_symbol: str, observer: StockObserver): ...
    def unsubscribe(self, stock_symbol: str, observer: StockObserver): ...
    def update_price(self, stock_symbol: str, price: float): ...
```

#### Observers
```python
class StockObserver(ABC):
    def on_price_change(self, symbol: str, old_price: float, new_price: float): ...
```

Concrete:
- `AlertObserver(threshold_percent)`: alerts when price changes by more than threshold%
- `LoggingObserver`: logs every price change to a list
- `AutoTrader(buy_below, sell_above)`: automatically buys/sells when conditions met

### Expected Usage

```python
market = StockMarket()
alert = AlertObserver(threshold_percent=5)
trader = AutoTrader(buy_below=150, sell_above=200)
logger = LoggingObserver()

market.subscribe("AAPL", alert)
market.subscribe("AAPL", trader)
market.subscribe("GOOGL", logger)

market.update_price("AAPL", 155.0)   # initial
market.update_price("AAPL", 145.0)   # -6.5% → alert triggers, trader buys
# → [ALERT] AAPL dropped 6.5% ($155.00 → $145.00)
# → [TRADE] BUY AAPL at $145.00 (below $150 threshold)

market.update_price("AAPL", 210.0)   # trader sells
# → [ALERT] AAPL rose 44.8% ($145.00 → $210.00)
# → [TRADE] SELL AAPL at $210.00 (above $200 threshold)

market.update_price("GOOGL", 2800.0)
# → [LOG] GOOGL: $2800.00 at 2024-01-15T10:30:00
```

### Constraints

- Observers subscribe to **specific stocks** — not all events.
- `StockMarket` stores observers per stock symbol (dict[str, list]).
- Price change percentage = `(new - old) / old * 100`.
- `AutoTrader` tracks position (bought/sold) to avoid duplicate trades.

### Think About

- How is topic-based subscription different from "observe everything"?
- How does this compare to pub/sub systems like Redis Pub/Sub or Kafka?
