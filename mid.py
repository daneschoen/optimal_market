import csv
import sys
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

def output_trades(trades, path):
    with open(path, 'w', newline='') as csvfile:
        fieldnames = ['Party', 'Counterparty', 'Direction', 'Product', 'Quantity', 'Rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for trade in trades:
            writer.writerow(trade)

def match_trades(orders):
    product_orders = defaultdict(lambda: {'Buy': [], 'Sell': []})
    for order in orders:
        product_orders[order['Product']][order['Direction']].append(order)

    trades = []

    for product, groups in product_orders.items():
        buyers = deque(sorted(groups['Buy'], key=lambda x: x['Price'], reverse=True))
        sellers = deque(sorted(groups['Sell'], key=lambda x: x['Price']))

        total_buy_qty = sum(b['Quantity'] for b in buyers)
        total_sell_qty = sum(s['Quantity'] for s in sellers)

        if total_buy_qty == 0 or total_sell_qty == 0:
            continue

        matched_qty = min(total_buy_qty, total_sell_qty)

        total_buy_value = sum(b['Quantity'] * b['Price'] for b in buyers)
        total_sell_value = sum(s['Quantity'] * s['Price'] for s in sellers)

        rate = (total_buy_value + total_sell_value) / (total_buy_qty + total_sell_qty)
        rate = round(rate, 2)

        while matched_qty > 0 and buyers and sellers:
            buyer = buyers[0]
            seller = sellers[0]

            trade_qty = min(buyer['Quantity'], seller['Quantity'], matched_qty)

            trades.append({
                'Party': seller['Party'],
                'Counterparty': buyer['Party'],
                'Direction': 'Sell',
                'Product': product,
                'Quantity': trade_qty,
                'Rate': rate
            })

            buyer['Quantity'] -= trade_qty
            seller['Quantity'] -= trade_qty
            matched_qty -= trade_qty

            if buyer['Quantity'] == 0:
                buyers.popleft()
            if seller['Quantity'] == 0:
                sellers.popleft()

    return trades

if __name__ == '__main__':
    ''' To run:
    python mid.py orders.csv --output mid_results.csv
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('--output', default='mid_results.csv')
    args = parser.parse_args()

    orders = get_orders(args.input_csv)
    trades = match_trades(orders)
    output_trades(trades, args.output)
