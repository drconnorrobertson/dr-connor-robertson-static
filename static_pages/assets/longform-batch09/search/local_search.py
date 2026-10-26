#!/usr/bin/env python3
"""Fictional local retrieval baseline. No network, model API or saved database."""
import argparse
import csv
import json
from pathlib import Path
import sqlite3

def search(path, query):
    path = Path(path)
    if path.stat().st_size > 2_000_000:
        raise ValueError('CSV exceeds the two-megabyte demonstration limit')
    if not query.strip() or len(query) > 300:
        raise ValueError('Query must contain 1 to 300 characters')
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ['doc_id', 'title', 'body']:
            raise ValueError('Expected CSV headers: doc_id,title,body')
        records = []
        identifiers = set()
        for row in reader:
            if len(records) >= 1000:
                raise ValueError('CSV exceeds the 1,000-record demonstration limit')
            if None in row or any(not isinstance(row.get(k), str) or not row[k].strip() for k in reader.fieldnames):
                raise ValueError('Each record needs three nonempty fields')
            values = tuple(row[k].strip() for k in reader.fieldnames)
            if values[0] in identifiers:
                raise ValueError('Duplicate document identifier: ' + values[0])
            identifiers.add(values[0])
            records.append(values)
    with sqlite3.connect(':memory:') as db:
        try:
            db.execute('CREATE VIRTUAL TABLE docs USING fts5(doc_id UNINDEXED, title, body)')
        except sqlite3.OperationalError as exc:
            raise ValueError('This demonstration requires SQLite with FTS5 support') from exc
        db.executemany('INSERT INTO docs(doc_id,title,body) VALUES (?,?,?)', records)
        phrase = '"' + query.strip().replace('"', '""') + '"'
        rows = db.execute('SELECT doc_id,title,body FROM docs WHERE docs MATCH ? ORDER BY bm25(docs),doc_id LIMIT 5', (phrase,)).fetchall()
    return [dict(zip(['doc_id', 'title', 'body'], row)) for row in rows]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file')
    parser.add_argument('query')
    args = parser.parse_args()
    try:
        result = search(args.csv_file, args.query)
    except (ValueError, OSError, csv.Error) as exc:
        parser.exit(2, 'Input error: ' + str(exc) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
