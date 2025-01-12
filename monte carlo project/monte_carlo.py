import numpy as np
import os
import math
os.environ['TCL_LIBRARY'] = "C:/Users/birsa/AppData/Local/Programs/Python/Python313/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Users/birsa/AppData/Local/Programs/Python/Python313/tcl/tk8.6"   
import matplotlib.pyplot as plt
import yfinance as yf

def download_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    if ('Close', stock_symbol) not in stock_data.columns:
        raise ValueError("Column 'Close' not found in the downloaded data.")
    return stock_data[('Close', stock_symbol)]


def calculate_market_parameters(stock_prices):
    # Calculating the log-returns
    log_returns = []
    for i in range(1, len(stock_prices)):
        if stock_prices[i - 1] > 0:  # Check to avoid division by zero
            log_return = math.log(stock_prices[i] / stock_prices[i - 1])
            log_returns.append(log_return)
    
    # Calculating the mean of log-returns
    num_returns = len(log_returns)
    if num_returns == 0:
        raise ValueError("Not enough data to calculate returns.")
    mean_log_return = sum(log_returns) / num_returns
    
    # Calculating the standard deviation
    variance = sum((r - mean_log_return)**2 for r in log_returns) / num_returns
    standard_deviation = math.sqrt(variance)
    
    # Converting to annualized values
    annualized_volatility = standard_deviation * math.sqrt(252)  # 252 trading days in a year
    annualized_return = mean_log_return * 252
    
    return annualized_return, annualized_volatility


import random

def simulate_future_stock_prices(initial_price, annualized_return, annualized_volatility, time_horizon, time_steps, num_simulations):
    """
    Simulates future stock prices using geometric Brownian motion.

    Parameters:  
    - initial_price: The initial stock price.
    - annualized_return: The annualized rate of return of the stock (μ).
    - annualized_volatility: The annualized volatility of the stock (σ).
    - time_horizon: The time horizon for the simulation (in years).
    - time_steps: The number of time steps in the simulation.
    - num_simulations: The number of independent simulations.

    Returns:
    - A list of the final stock prices for each simulation.
    """

    # Delta time (∆t) - The time interval for each step of the simulation
    delta_time = time_horizon / time_steps
    
    # List to store the final prices from each simulation
    final_prices = []
    
    for simulation_index in range(num_simulations):
        stock_price = initial_price  # Initializing the price with the initial price
        
        # Simulation for each time step
        for step in range(time_steps):
            # Generate a random variable from a standard normal distribution N(0, 1)
            z = random.gauss(0, 1)
            
            # Drift (µ - 0.5 * σ²)∆t - The deterministic component
            # The drift reflects the general price trend based on average profitability and volatility adjustment.
            drift = (annualized_return - 0.5 * annualized_volatility**2) * delta_time
            
            # Diffusion (σ√∆t * z) - The stochastic component
            # Diffusion adds random variability based on volatility and normal distribution.
            diffusion = annualized_volatility * math.sqrt(delta_time) * z
            
            # Geometric Brownian motion:
            # S(t+∆t) = S(t) * exp(drift + diffusion)
            # This is the solution to the stochastic differential equation:
            # dS(t) = µS(t)dt + σS(t)dW(t), where W(t) is a Wiener process.
            stock_price *= math.exp(drift + diffusion)
        
        # We add the final price of the current simulation to the results list
        final_prices.append(stock_price)
    
    return final_prices


def calculate_call_option_price(simulated_prices, strike_price, risk_free_rate, time_to_maturity):
    total_payoffs = 0
    num_simulations = len(simulated_prices)
    for final_price in simulated_prices:
        payoff = max(final_price - strike_price, 0)
        total_payoffs += payoff
    average_payoff = total_payoffs / num_simulations
    discounted_price = np.exp(-risk_free_rate * time_to_maturity) * average_payoff
    return discounted_price

def hoeffding_trial_count(tolerance, min_payoff, max_payoff, confidence_level):
    return np.ceil((np.log(2 / confidence_level) * (max_payoff - min_payoff)**2) / (2 * tolerance**2))

def main():
    stock_symbol = 'JNJ'
    data_start_date = '2020-01-01'
    data_end_date = '2021-01-01'
    stock_prices = download_stock_data(stock_symbol, data_start_date, data_end_date)
    initial_price = stock_prices.iloc[-1]
    print(f"Initial stock price for {stock_symbol} at the end of the data period: ${initial_price:.2f}")
    
    strike_price = initial_price * 1.2 # to change
    maturity_time = 1
    risk_free_rate = 0.03
    annualized_return, annualized_volatility = calculate_market_parameters(stock_prices)
    
    tolerance = 1.00
    confidence_level = 0.05
    min_payoff = 0
    max_payoff_estimate = np.max(np.maximum(initial_price * np.exp(annualized_return + 3 * annualized_volatility) - strike_price, 0))
    
    num_simulations = int(hoeffding_trial_count(tolerance, min_payoff, max_payoff_estimate, confidence_level))
    print(f"Using {num_simulations} simulations to ensure estimation error within ${tolerance} with 95% confidence.")
    
    simulated_prices = simulate_future_stock_prices(initial_price, annualized_return, annualized_volatility, maturity_time, 252, num_simulations)
    estimated_call_price = calculate_call_option_price(simulated_prices, strike_price, risk_free_rate, maturity_time)
    
    print(f"Estimated call option price: ${estimated_call_price:.2f}")
    
    plt.figure(figsize=(10, 6))
    plt.hist(simulated_prices, bins=50, alpha=0.75)
    plt.axvline(x=strike_price, color='r', linestyle='--', label='Strike Price (K)')
    plt.title(f'End-of-Year Stock Price Distributions for {stock_symbol}')
    plt.xlabel('Stock Price at Expiry')
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
