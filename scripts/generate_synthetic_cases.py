import csv
from pathlib import Path


CASES = [
    ('base', 'RPC timeout while connecting to endpoint', 'RPC endpoint'),
    ('base-sepolia', 'execution reverted during deployment', 'Foundry'),
    ('base-sepolia', 'bridge deposit pending', 'bridge'),
]


def main():
    output = Path(__file__).parents[1] / 'data_samples' / 'synthetic_cases.csv'
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['network', 'error_message', 'tool_used'])
        writer.writerows(CASES)
    print(output)


if __name__ == '__main__':
    main()
