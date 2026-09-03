import csv
from pathlib import Path

from app.models import create_case
from app.triage import triage_case


def main():
    source = Path(__file__).parents[1] / 'data_samples' / 'support_cases.csv'
    with source.open(newline='', encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            payload = {key: value or None for key, value in row.items()}
            payload['triage'] = triage_case(payload)
            create_case(payload)
    print(f'Imported cases from {source}')


if __name__ == '__main__':
    main()
