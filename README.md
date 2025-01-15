# Monte Carlo Simulation for Option Pricing

## Overview
This project implements a Monte Carlo simulation to estimate the price of a European call option based on the Geometric Brownian Motion (GBM) model. The goal is to simulate the future price movements of a stock and determine the fair value of the option, providing insights into the associated risks and potential returns.

---

## What is a Monte Carlo Simulation for Stock Prices?
Monte Carlo simulation is a probabilistic technique used to generate a large number of possible scenarios for the evolution of a system. In this context, the system being simulated is the stock price, which follows a random, stochastic process.

- **Main objective**: To estimate the price of an option by analyzing the probable distribution of future stock prices.

---

## Financial Context of the Project
- A **European call option** gives the holder the right (but not the obligation) to purchase a stock at a predetermined price (called the strike price) at a specified future date.
- The **value of the option** depends on the expected future price of the stock relative to the strike price. If the stock price at maturity exceeds the strike price, the option has a positive payoff; otherwise, it expires worthless.

---

## Key Components of the Model

### 1. Stock Price Simulation:
- The future price of the stock is simulated using the GBM model, which incorporates both the drift (expected return) and volatility (random fluctuations) of the stock.
- The process is repeated thousands of times to account for a wide range of possible price paths.

### 2. Option Payoff Calculation:
- The payoff of the option for each simulated scenario is computed as the difference between the final stock price and the strike price (if positive).

### 3. Discounting to Present Value:
- The average expected payoff is discounted using the risk-free interest rate to obtain the present value of the option.

---

## Practical Applications
This type of simulation is widely used in financial engineering for:
- **Risk assessment and pricing of financial derivatives**.
- **Portfolio optimization** by analyzing potential outcomes under different market conditions.
- **Stress-testing strategies** to evaluate how extreme market movements affect the value of options.


## Contents
- [Project Setup](#project-setup)
- [Mathematical Model](#mathematical-model)
  - [Geometric Brownian Motion (GBM)](#geometric-brownian-motion-gbm)
  - [Monte Carlo Simulation](#monte-carlo-simulation)
  - [Discounting to Present Value](#discounting-to-present-value)
- [Implementation Details](#implementation-details)
- [Evaluation and Results](#evaluation-and-results)
- [Additional Resources](#additional-resources)



---

## Project Setup

### Dependencies
- Python 3.x
- NumPy
- Matplotlib
- yFinance

### Installation
To install necessary libraries, run:
```bash
pip install numpy matplotlib yfinance
```
## Environmental Variables

To configure the system for matplotlib, set the necessary environment variables:

### For Terminal:
```bash
# Set TCL and TK paths for matplotlib
export TCL_LIBRARY="<path_to_tcl>"
export TK_LIBRARY="<path_to_tk>"
```
### For Python:
```python
import os
os.environ['TCL_LIBRARY'] = "<path_to_tcl>"
os.environ['TK_LIBRARY'] = "<path_to_tk>"
```





# Mathematical Model

## Geometric Brownian Motion (GBM)
The project uses GBM to model the stock prices' dynamics under a stochastic process defined by:

The differential equation for GBM is:

$$
dS_t = \mu S_t \, dt + \sigma S_t \, dW_t
$$

### **Variable Definitions**

$$
\begin{aligned}
dS_t & : \text{ The change in stock price at time } t, \\
\mu & : \text{ The annualized return (drift)}, \\
\sigma & : \text{ The annualized volatility (measure of risk)}, \\
S_t & : \text{ The stock price at time } t, \\
dW_t & : \text{ The increment of a Wiener process (random market fluctuation)}.
\end{aligned}
$$

---

## Intermediate Formulas

### **Logarithmic Returns**
The logarithmic return between two time points is given by:

$$
r_i = \ln\left(\frac{S_i}{S_{i-1}}\right)
$$

### **Variable Definitions**

$$
\begin{aligned}
S_i & : \text{ The stock price at time } i, \\
S_{i-1} & : \text{ The stock price at time } i - 1.
\end{aligned}
$$

---

### **Mean Log Return**
The mean log return over \(n\) returns is:

$$
\bar{r} = \frac{1}{n} \sum_{i=1}^{n} r_i
$$

---

### **Variance and Standard Deviation**
The variance of the log returns is:

$$
\sigma^2 = \frac{1}{n} \sum_{i=1}^{n} (r_i - \bar{r})^2
$$

The standard deviation (volatility) is:

$$
\sigma = \sqrt{\sigma^2}
$$

---

### **Annualization**
To annualize the returns and volatility:

$$
\mu_{\text{annualized}} = \bar{r} \times 252
$$

$$
\sigma_{\text{annualized}} = \sigma \times \sqrt{252}
$$

### **Variable Definitions**

$$
252 : \text{ The number of trading days in a year.}
$$

---

## Monte Carlo Simulation
The formula for stock price evolution at a time step \(\Delta t\) is:

$$
S(t + \Delta t) = S(t) \times e^{(\mu - 0.5 \sigma^2) \Delta t + \sigma \sqrt{\Delta t} \cdot z}
$$

### **Variable Definitions**

$$
\begin{aligned}
S(t) & : \text{ The stock price at time } t, \\
\mu & : \text{ The annualized return (drift)}, \\
\sigma & : \text{ The annualized volatility}, \\
\Delta t & : \text{ The time step}, \\
z & : \text{ A random variable sampled from a standard normal distribution } (z \sim N(0, 1)).
\end{aligned}
$$

---

## Discounting to Present Value
The formula for present value is:

$$
PV = e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]
$$

### **Variable Definitions**

$$
\begin{aligned}
PV & : \text{ The present value (option price)}, \\
r & : \text{ The risk-free interest rate}, \\
T & : \text{ The time to maturity (in years)}, \\
S_T & : \text{ The stock price at maturity}, \\
K & : \text{ The strike price}, \\
\mathbb{E}[\max(S_T - K, 0)] & : \text{ The expected value (mean payoff at maturity)}.
\end{aligned}
$$










## Implementation Details

### Data Acquisition
Stock data is fetched using yFinance, focusing on historical closing prices to calculate the necessary parameters for simulation.

### Simulation Execution
The project iterates over numerous simulated paths to average out the randomness and provides an estimate of the option's price.

### Visualization
Results are visualized using histograms to represent the distribution of simulated end-of-year stock prices, and the strike price is marked for reference.

---

## Evaluation and Results

### Accuracy and Confidence
The number of simulations is determined using Hoeffding’s inequality to ensure that the estimated option price falls within a tolerable error range with a confidence level of 95%.

![JNJ](image.png)


### Additional Resources
- **Monte Carlo Simulation for Finance**: [https://en.wikipedia.org/wiki/Monte_Carlo_method](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- **Geometric Brownian Motion**: [https://en.wikipedia.org/wiki/Geometric_Brownian_motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion)
- **Option Pricing Theory**: [https://www.investopedia.com/terms/o/option-pricing-theory.asp](https://www.investopedia.com/terms/o/option-pricing-theory.asp)
- **QuantPy**: [https://www.youtube.com/watch?v=6-dhdMDiYWQ&list=PLqpCwow11-OqqfELduCMcRI6wcnoM3GAZ&index=1](https://www.youtube.com/watch?v=6-dhdMDiYWQ&list=PLqpCwow11-OqqfELduCMcRI6wcnoM3GAZ&index=1)
- **QuantPy Github**: [https://github.com/TheQuantPy/youtube-tutorials/blob/8e64e19629cee840928b51baf4660e5c777e87e7/2020/001%20Oct-Dec/2020-11-24%20Value%20at%20Risk%20(VaR)%20Explained!.ipynb](https://github.com/TheQuantPy/youtube-tutorials/blob/8e64e19629cee840928b51baf4660e5c777e87e7/2020/001%20Oct-Dec/2020-11-24%20Value%20at%20Risk%20(VaR)%20Explained!.ipynb)
