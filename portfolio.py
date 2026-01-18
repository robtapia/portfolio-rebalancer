from dataclasses import dataclass
from random import random, seed

# Use seed to obtain repeatable results from Stock.get_current_price, for debugging 
# seed(1)

@dataclass(frozen=True)
class Stock:
    ticker: str

    def get_current_price(self) -> float:
        return 10*random()

    def __str__(self):
        return self.ticker
    

# @dataclass
class Portfolio:
    """
    This class receives stocks both owned and allocated, as dictionaries, where
    the keys are Stock objects, and the values are floats, the amount of shares for stocks_owned
    and the fraction of the portfolio (between 0 and 1) for stock_allocation.
    """
    stocks_owned: dict[Stock, float]
    stock_allocation: dict[Stock, float]

    def __init__(self, stocks_owned: dict[Stock, float], stock_allocation: dict[Stock, float]):
        if sum(stocks_owned.values()) <= 0:
            raise Exception("Can't create a portfolio without any shares!")
        if sum(stock_allocation.values()) != 1:
            raise Exception("Can't create a portfolio without a valid allocation!")

        self.stocks_owned = stocks_owned
        self.stock_allocation = stock_allocation

    def rebalance_portfolio(self) -> dict[Stock, float]:
        """
        Checks stocks_owned and stock_allocation to calculate which stocks to sell and
        to buy to fit allocation.

        :returns: A dictionary, where the key is a Stock object, and the value
            is a float. A positive number indicates the stock must be bought, and a negative one indicates 
            it should be sold, in both cases the amount to trade is the value of the float.
        """
        current_allocation = {}
        total_value = 0
        rebalance = {}

        # We create a list that contains all relevant stocks, specifically, to avoid problems if any stock
        # is owned but has no allocation, or vice versa. Then we convert it to a set to avoid repetitions
        total_stocks = set(list(self.stock_allocation.keys())+list(self.stocks_owned.keys()))

        # We iterate over all relevant stocks, calculating both the current price of the stock, and the total
        # value the portfolio holds in this stock.
        # Also, while we iterate, we calculate the total value of the portfolio in all stocks
        for stock in total_stocks:
            current_price = stock.get_current_price()
            current_value = current_price * self.stocks_owned[stock] if stock in self.stocks_owned else 0
            current_allocation[stock] = {
                "current_price": current_price,
                "current_value": current_value,
                # "current_allocation": 0
            }
            total_value += current_value
            print(f"{str(stock)}: {current_allocation[stock]}")
            print(f"total_value current: {total_value}")

        # We iterate over the dictionary we previously built, which now contains 
        # the value of each stock held in the portfolio.
        for stock in current_allocation.keys():
            # We calculate which percentage of the portfolio is in every specific stock
            current_allocation[stock]["current_allocation"] = (current_allocation[stock]["current_value"] / total_value)
            
            # We calculate the difference between how much of the portfolio should be in each stock
            # and how much actually is in said stock.
            # We use minus the current value of the stock for the cases when the stock has no allocation
            # and then overwrite the value for the cases where the stock has an allocation
            delta_allocation = -current_allocation[stock]["current_allocation"]
            if stock in self.stock_allocation:
                delta_allocation = self.stock_allocation[stock] - current_allocation[stock]["current_allocation"]
            
            # After calculting which percentage of the stock should be bought or sold,
            # we convert this percentage into a number of shares
            # (Here we use floats, which have a higher precision than what could probably be bought or sold,
            # though it is possible to round the numbers later)
            delta_units = (delta_allocation * total_value) / current_allocation[stock]["current_price"]
            # changes.append((stock, delta_units,))
            rebalance[stock] = delta_units

        return rebalance
