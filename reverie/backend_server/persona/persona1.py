"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: persona.py
Description: Defines the Persona class that powers the agents in Reverie. 

Note (May 1, 2023) -- this is effectively GenerativeAgent class. Persona was
the term we used internally back in 2022, taking from our Social Simulacra 
paper.
"""
import math
import sys
import datetime
import random
sys.path.append('../')
from global_methods import *

from persona.memory_structures.spatial_memory import *
from persona.memory_structures.associative_memory import *
from persona.memory_structures.scratch import *

from persona.cognitive_modules.perceive import *
from persona.cognitive_modules.retrieve import *
from persona.cognitive_modules.plan import *
from persona.cognitive_modules.reflect import *
from persona.cognitive_modules.execute import *
from persona.cognitive_modules.converse import *


class Persona:
    def __init__(self, name, role):
            self.name = name
            self.role = role
            self.current_investments = {}  # Dictionary to store current investments
            self.market_knowledge = {}     # Dictionary to store market knowledge
            self.risk_tolerance = 0.5      # Default risk tolerance
            self.cash_reserves = 100000    # Example initial cash reserves
            self.transaction_history = []  # List to store transaction history
            
            # Initialize market knowledge and investments
            self.initialize_market_knowledge()
            self.initialize_investments(folder_mem_saved)
            
            
    def initialize_market_knowledge(self):
        """
        Initialize market knowledge with baseline information.
        """
        # Example: Initialize with static data
        # In a real scenario, this might involve fetching data from a financial data API
        self.market_knowledge = {
            'StockA': {'current_price': 100, 'sentiment': 0.6, 'is_undervalued': True},
            'StockB': {'current_price': 150, 'sentiment': 0.4, 'is_undervalued': False}
            # ... other initial market data ...
        }

    def initialize_investments(self, folder_mem_saved):
        """
        Initialize or load the persona's investment portfolio.
        """
        if folder_mem_saved:
            # Load investments from saved memory
            # This would involve reading from a file or database
            # Example: Read JSON file and update current_investments
            try:
                with open(f"{folder_mem_saved}/investments.json", 'r') as file:
                    self.current_investments = json.load(file)
            except IOError:
                print("Saved investments file not found. Initializing new investments.")
                self.current_investments = {}
        else:
            # Initialize new investments
            self.current_investments = {
                # Example initial investment structure
                # 'StockA': {'quantity': 10, 'purchase_price': 100, 'current_price': 100},
                # 'StockB': {'quantity': 5, 'purchase_price': 150, 'current_price': 150}
            }



    def manage_portfolio(self):
            """
            Manage the persona's investment portfolio.
            """
            # Rebalance logic
            for stock, info in self.current_investments.items():
                if info['should_rebalance']:
                    self.rebalance_stock(stock, info)

            # Simple buying/selling logic based on a predefined strategy
            for stock, market_info in self.market_knowledge.items():
                if self.should_buy(stock, market_info):
                    self.buy_stock(stock, market_info)
                elif self.should_sell(stock, market_info):
                    self.sell_stock(stock, market_info)

    def rebalance_stock(self, stock, info):
        """
        Rebalance a specific stock in the portfolio.

        :param stock: str - Stock symbol.
        :param info: dict - Information about the stock in the portfolio.
        """
        desired_allocation = info['desired_allocation']
        current_allocation = self.calculate_current_allocation(stock)

        if current_allocation < desired_allocation:
            # Buy more of the stock to reach the desired allocation
            amount_to_buy = self.calculate_amount_to_buy(stock, desired_allocation, current_allocation)
            self.buy_stock(stock, amount_to_buy)
        elif current_allocation > desired_allocation:
            # Sell some of the stock to reduce to the desired allocation
            amount_to_sell = self.calculate_amount_to_sell(stock, desired_allocation, current_allocation)
            self.sell_stock(stock, amount_to_sell)
            
    def calculate_current_allocation(self, stock):
        """
        Calculate the current allocation of a stock in the portfolio.

        :param stock: str - Stock symbol.
        :return: float - The current allocation percentage of the stock.
        """
        total_portfolio_value = sum([info['quantity'] * info['current_price'] for info in self.current_investments.values()])
        stock_value = self.current_investments[stock]['quantity'] * self.current_investments[stock]['current_price']
        
        return stock_value / total_portfolio_value if total_portfolio_value > 0 else 0
    
    def calculate_amount_to_buy(self, stock, desired_allocation, current_allocation):
        """
        Calculate the amount of a stock to buy to reach the desired allocation.

        :param stock: str - Stock symbol.
        :param desired_allocation: float - The desired allocation percentage.
        :param current_allocation: float - The current allocation percentage.
        :return: float - The amount of stock to buy.
        """
        total_portfolio_value = sum([info['quantity'] * info['current_price'] for info in self.current_investments.values()])
        desired_stock_value = desired_allocation * total_portfolio_value
        current_stock_value = current_allocation * total_portfolio_value

        amount_to_buy_value = desired_stock_value - current_stock_value
        return amount_to_buy_value / self.current_investments[stock]['current_price']

    def calculate_amount_to_sell(self, stock, desired_allocation, current_allocation):
        """
        Calculate the amount of a stock to sell to reach the desired allocation.

        :param stock: str - Stock symbol.
        :param desired_allocation: float - The desired allocation percentage.
        :param current_allocation: float - The current allocation percentage.
        :return: float - The amount of stock to sell.
        """
        total_portfolio_value = sum([info['quantity'] * info['current_price'] for info in self.current_investments.values()])
        desired_stock_value = desired_allocation * total_portfolio_value
        current_stock_value = current_allocation * total_portfolio_value

        amount_to_sell_value = current_stock_value - desired_stock_value
        return amount_to_sell_value / self.current_investments[stock]['current_price']



    def should_buy(self, stock, market_info):
        """
        Determine whether to buy a stock.

        :param stock: str - Stock symbol.
        :param market_info: dict - Market information about the stock.
        :return: bool - True if the stock should be bought, else False.
        """
        # Simple decision-making logic to buy stock
        # Example: Buy if the market sentiment is positive and the stock is undervalued
        return market_info['sentiment'] > 0.5 and market_info['is_undervalued']

    def should_sell(self, stock, market_info):
        """
        Determine whether to sell a stock.

        :param stock: str - Stock symbol.
        :param market_info: dict - Market information about the stock.
        :return: bool - True if the stock should be sold, else False.
        """
        # Simple decision-making logic to sell stock
        # Example: Sell if the stock is overvalued or if the market sentiment is negative
        return market_info['sentiment'] < 0.5 or market_info['is_overvalued']

    def buy_stock(self, stock, amount):
        """
        Buy a stock.

        :param stock: str - The stock symbol.
        :param amount: float - The amount of the stock to buy.
        """
        # Check if the stock is already in the portfolio
        if stock in self.current_investments:
            self.current_investments[stock]['quantity'] += amount
        else:
            # If not, add the stock to the portfolio
            self.current_investments[stock] = {'quantity': amount, 'purchase_price': self.market_knowledge[stock]['current_price']}
        
        # Deduct the cost of purchase from the cash reserves (assuming cash reserves are being tracked)
        # self.cash_reserves -= amount * self.market_knowledge[stock]['current_price']


    def sell_stock(self, stock, amount):
        """
        Sell a stock.

        :param stock: str - The stock symbol.
        :param amount: float - The amount of the stock to sell.
        """
        if stock in self.current_investments and self.current_investments[stock]['quantity'] >= amount:
            self.current_investments[stock]['quantity'] -= amount
            
            # Add the revenue from the sale to the cash reserves
            # self.cash_reserves += amount * self.market_knowledge[stock]['current_price']

            # Remove the stock from the portfolio if the quantity reaches zero
            if self.current_investments[stock]['quantity'] == 0:
                del self.current_investments[stock]
        else:
            # Handle the case where the stock is not in the portfolio or not enough quantity is available to sell
            # This could be logging an error, raising an exception, etc.
            pass


    def evaluate_performance(self):
        """
        Evaluate the performance of the persona's investments.
        """
        total_return = 0
        for stock, info in self.current_investments.items():
            # Calculate returns for each stock
            stock_return = (info['current_price'] - info['purchase_price']) / info['purchase_price']
            total_return += stock_return

        return total_return / len(self.current_investments)


    def assess_risk(self):
        """
        Assess the risk of the current investment portfolio.
        """
        portfolio_risk = 0
        for stock, info in self.current_investments.items():
            # Assume 'risk_score' is part of info
            portfolio_risk += info['risk_score']

        average_risk = portfolio_risk / len(self.current_investments)
        return average_risk

        

    def conduct_market_research(self):
        """
        Conduct market research to update market knowledge.
        """
        # This is a placeholder for market research logic
        # In a real-world scenario, this would involve analyzing market data, reports, etc.
        new_market_info = {}  # Assume this is obtained from research
        self.market_knowledge.update(new_market_info)


