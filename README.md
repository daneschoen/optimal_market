# Optimal Market Algorithm
Algorithm for matching buy and sell orders of any products using bidirectional queue.

Given a list of buy and sell orders in a trading system, optimal algorithm takes in orders, which matches as many buyers to sellers by
creating trades between party pairs. Each trade must be executed at the mid-market rate, which is defined as the quantity-weighted average of input prices within a given
product. 

We define profit and loss (P&L) for a given trade to be:

$$
P\&L_{buyer} = Quantity \cdot (Price_{buyer} - Rate)
$$

$$
P\&L_{seller} = Quantity \cdot (Rate - Price_{seller})
$$

Algorithm is also adjusted to allow for limits, specifying how much net amount they are able to buy and sell.
