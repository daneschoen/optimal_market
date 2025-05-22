# Optimal Market Algorithm
Algorithm for matching buy and sell orders of any products using bidirectional queue.

Given a list of buy and sell orders in a trading system, optimal algorithm takes in orders, which matches as many buyers to sellers by
creating trades between party pairs. Each trade must be executed at the mid-market rate, which is defined as the quantity-weighted average of input prices within a given
product. 

Profit and loss (P&L) for a given trade to be:

**P&L<sub>buyer</sub>** = Quantity × (Price<sub>buyer</sub> − Rate)  
**P&L<sub>seller</sub>** = Quantity × (Rate − Price<sub>seller</sub>)


Algorithm is also adjusted to allow for limits, specifying how much net amount they are able to buy and sell.
