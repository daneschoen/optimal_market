import csv
import argparse
from collections import defaultdict, deque

def get_orders(path):
    orders = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['Quantity'] = int(row['Quantity'])
            row['Price'] = float(row['Price'])
            orders.append(row)
    return orders

def get_limits(path):
    limits = defaultdict(lambda: {'Buy': float('inf'), 'Sell': float('inf')})
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            direction = row['Direction']
            party = row['Party']
            limits[party][direction] = int(row['Net Limit'])
    return limits

def out_trades(trades, path):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['Party', 'Counterparty', 'Direction', 'Product', 'Quantity', 'Rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for trade in trades:
            writer.writerow(trade)

def match_trade_limits(orders, limits):
    trades = []
    product_orders = defaultdict(lambda: {'Buy': [], 'Sell': []})

    remaining_limits = {p: {'Buy': l['Buy'], 'Sell': l['Sell']} for p, l in limits.items()}

    for order in orders:
        product_orders[order['Product']][order['Direction']].append(order)

    for product, groups in product_orders.items():
        buyers = deque(sorted(groups['Buy'], key=lambda x: x['Price'], reverse=True))
        sellers = deque(sorted(groups['Sell'], key=lambda x: x['Price']))

        total_buy_qty = sum(b['Quantity'] for b in buyers)
        total_sell_qty = sum(s['Quantity'] for s in sellers)

        if total_buy_qty == 0 or total_sell_qty == 0:
            continue

        total_buy_value = sum(b['Quantity'] * b['Price'] for b in buyers)
        total_sell_value = sum(s['Quantity'] * s['Price'] for s in sellers)
        rate = round((total_buy_value + total_sell_value) / (total_buy_qty + total_sell_qty), 2)

        while buyers and sellers:
            buyer = buyers[0]
            seller = sellers[0]

            buyer_party = buyer['Party']
            seller_party = seller['Party']

            max_buyer_limit = remaining_limits.get(buyer_party, {}).get('Buy', 0)
            max_seller_limit = remaining_limits.get(seller_party, {}).get('Sell', 0)

            max_trade_qty = min(buyer['Quantity'], seller['Quantity'], max_buyer_limit, max_seller_limit)
            if max_trade_qty <= 0:
                break

            trades.append({
                'Party': seller_party,
                'Counterparty': buyer_party,
                'Direction': 'Sell',
                'Product': product,
                'Quantity': max_trade_qty,
                'Rate': rate
            })

            buyer['Quantity'] -= max_trade_qty
            seller['Quantity'] -= max_trade_qty
            remaining_limits[buyer_party]['Buy'] -= max_trade_qty
            remaining_limits[seller_party]['Sell'] -= max_trade_qty

            if buyer['Quantity'] == 0:
                buyers.popleft()
            if seller['Quantity'] == 0:
                sellers.popleft()

    return trades

if __name__ == '__main__':
    """
    Example usage:
    python limits.py orders.csv limits.csv --output limit_results.csv
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('orders_csv')
    parser.add_argument('limits_csv')
    parser.add_argument('--output', default='limit_results.csv')
    args = parser.parse_args()

    orders = get_orders(args.orders_csv)
    limits = get_limits(args.limits_csv)
    trades = match_trades_limits(orders, limits)
    out_trades(trades, args.output)
