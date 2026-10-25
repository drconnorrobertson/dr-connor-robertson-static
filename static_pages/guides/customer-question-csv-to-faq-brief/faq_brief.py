"""Build an evidence-preserving FAQ brief from reviewed CSV and answer records.
No network access, model calls, semantic topic inference or publishing.
"""
import csv
import json
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

FIELDS = {'request_id', 'question', 'topic', 'answer_id'}

def normalize(text):
    return ' '.join(unicodedata.normalize('NFKC', text).casefold().split())

def build(csv_path, answer_path):
    answers = json.loads(Path(answer_path).read_text(encoding='utf-8'))
    if not isinstance(answers, dict):
        raise ValueError('Answer file must be an object keyed by answer ID')
    groups = defaultdict(list)
    seen = set()
    with Path(csv_path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or len(reader.fieldnames) != len(FIELDS) or set(reader.fieldnames) != FIELDS:
            raise ValueError('Expected exactly: request_id, question, topic, answer_id')
        for number, raw in enumerate(reader, 2):
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError(f'Row {number}: wrong field count')
            row = {key: value.strip() for key, value in raw.items()}
            if not all(row.values()):
                raise ValueError(f'Row {number}: required value is blank')
            if row['request_id'] in seen:
                raise ValueError(f'Row {number}: duplicate request ID')
            seen.add(row['request_id'])
            answer = answers.get(row['answer_id'])
            if not isinstance(answer, dict) or not all(answer.get(key) for key in ['text', 'source', 'version']):
                raise ValueError(f'Row {number}: answer requires text, source and version')
            groups[row['topic']].append(row)
    result = []
    for topic, rows in sorted(groups.items()):
        variants = defaultdict(list)
        for row in rows:
            variants[normalize(row['question'])].append(row['request_id'])
        result.append({
            'topic': topic,
            'observed_request_rows': len(rows),
            'source_request_ids': [row['request_id'] for row in rows],
            'wording_variants': [
                {'normalized_question': question, 'request_ids': ids}
                for question, ids in sorted(variants.items())
            ],
            'answer_records': {
                key: answers[key] for key in sorted({row['answer_id'] for row in rows})
            },
            'review_status': 'Draft evidence brief; human scope and publication review required'
        })
    return result

if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('Usage: python3 faq_brief.py requests.csv answers.json output.json')
    result = build(sys.argv[1], sys.argv[2])
    Path(sys.argv[3]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared {len(result)} topic briefs; no pages published')
