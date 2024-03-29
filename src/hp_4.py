# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_dates = []
    for date_str in old_dates:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        new_date_str = datetime.strftime(date_obj, '%d %b %Y')
        new_dates.append(new_date_str)
    return new_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str):
        raise TypeError("Start date must be a string.")
    elif not isinstance(n, int):
        raise TypeError("Number of days must be an integer.")
    else:
        date_list = []
        for i in range(n):
            date_obj = datetime.strptime(start, '%Y-%m-%d') + timedelta(days=i)
            date_list.append(date_obj)

        return date_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    start_date_object = datetime.strptime(start_date, '%Y-%m-%d')
    date_seq = [start_date_object + timedelta(days=i) for i in range(len(values))]
    res = list(zip(date_seq, values))
    return res


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    late_fees = defaultdict(float)

    with open(infile, 'r') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            patron_id = row['patron_id']
            date_returned = datetime.strptime(row['date_returned'], '%m/%d/%Y')
            date_due = datetime.strptime(row['date_due'], '%m/%d/%Y')
            late_days = max((date_returned - date_due).days, 0)
            late_fee = late_days * 0.25
            late_fees[patron_id] += late_fee
    
    with open(outfile, 'w') as csvfile:
        writer = DictWriter(csvfile, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        for patron_id, fee in late_fees.items():
            writer.writerow({
            'patron_id': patron_id,
            'late_fees': f'{fee:.2f}',
            })


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
