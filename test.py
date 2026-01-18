from portfolio import Stock, Portfolio

meta = Stock("META")
tsla = Stock("TSLA")
aapl = Stock("AAPL")

def test_unnallocated_stock():
    stocks_owned = {
        meta: 0.5,
        tsla: 0.5
    }
    stocks_allocated = {
        meta: 1
    }
    portfolio = Portfolio(stocks_owned, stocks_allocated)
    rebalance = portfolio.rebalance_portfolio()
    assert rebalance[tsla] == -0.5, "Should sell all tsla (not allocated)"

def test_not_owned_stock():
    stocks_owned = {
        meta: 1
    }
    stocks_allocated = {
        meta: 0.5,
        tsla: 0.5
    }
    portfolio = Portfolio(stocks_owned, stocks_allocated)
    rebalance = portfolio.rebalance_portfolio()
    assert rebalance[meta] == -0.5, "Should sell half of meta to buy tsla"
    assert rebalance[tsla] > 0, "Should buy tsla"