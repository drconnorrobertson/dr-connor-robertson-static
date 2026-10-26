"""Local illustrative agenda arithmetic; does not schedule or assess meetings."""
import csv
import json
import re
import sys


def calculate(rows, available):
    if type(available) is not int or available <= 0:
        raise ValueError('Available minutes must be a positive integer')
    seen = set()
    total = 0
    for row in rows:
        item = row['item_id'].strip()
        minutes = row['minutes'].strip()
        if not item or item in seen:
            raise ValueError('Item IDs must be present and unique')
        if not re.fullmatch(r'[0-9]+', minutes) or int(minutes) <= 0:
            raise ValueError('Each allocation must be a positive integer')
        seen.add(item)
        total += int(minutes)
    if not seen:
        raise ValueError('No agenda items')
    return {'item_count': len(seen), 'available_minutes': available,
            'allocated_minutes': total, 'unallocated_minutes': max(available-total, 0),
            'overrun_minutes': max(total-available, 0)}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python3 agenda_minutes.py fictional-agenda.csv 45')
    with open(sys.argv[1], newline='', encoding='utf-8') as source:
        result = calculate(csv.DictReader(source), int(sys.argv[2]))
    print(json.dumps(result, indent=2))
