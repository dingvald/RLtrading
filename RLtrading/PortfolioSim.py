class Stock:
    shares = 0
    avg_price = 0

    def __init__(self, shares, price):
        self.shares = shares
        self.avg_price = price

    def buy(self, shares, price):
        self.shares += shares
        self.avg_price = (self.avg_price + shares*price) / self.shares
        
    def sell(self, shares, price):
        if self.shares - shares <= 0:
            self.avg_price = 0
            return
        self.avg_price = ((self.avg_price * self.shares) - (shares*price)) / (self.shares - shares)
        self.shares -= shares




class Portfolio:
    cash = 0.00
    positions = {}

    def buy(self, ticker, shares, price):
        if self.cash >= shares*price:
            if ticker in self.positions:
                self.positions[ticker].buy(shares, price)
            else:
                self.positions[ticker] = Stock(shares, price)
            self.cash -= shares*price
        else:
            print("Cannot purchase",ticker,"not enough cash!")

    def sell(self, ticker, shares, price):
        if ticker not in self.positions:
            return
        else:
            self.positions[ticker].sell(shares, price)
            self.cash += shares*price
            if self.positions[ticker].shares <= 0:
                self.positions.pop(ticker)

    def deposit_cash(self, amount):
        self.cash += amount

    def print_portfolio(self):
        print("Cash: $",self.cash)
        for key, value in self.positions.items():
            print(key, "Shares:", value.shares, "AVG Price: $", value.avg_price)
