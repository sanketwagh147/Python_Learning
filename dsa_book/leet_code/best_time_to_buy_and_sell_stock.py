"""
Leet code 121
"""

from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        # Track the lowest price
        min_price = float("inf")  # buy_price
        max_profit = 0

        for price in prices:

            # update min price if lower
            if price < min_price:
                min_price = price

            profit = price - min_price

            # update max price if higher
            if profit > max_profit:
                max_profit = profit

        return max_profit

    def maxProfit_brute(self, prices: List[int]) -> int:
        """Brute force"""
        max_profit = 0
        num_days = len(prices)

        for i in range(num_days):

            for j in range(i + 1, num_days):
                profit = prices[j] - prices[i]

                if profit > max_profit:
                    max_profit = profit

        return max_profit


if __name__ == "__main__":
    # prices = [7, 1, 5, 3, 6, 4]
    # s = Solution()
    # s.maxProfit(prices)

    prices = [2, 1, 4]
    s = Solution()
    s.maxProfit(prices)
