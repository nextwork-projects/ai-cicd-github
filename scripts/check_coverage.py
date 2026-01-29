import subprocess
import sys
import json

def get_coverage_percentage():
    """Run pytest with coverage and return the percentage."""
    result = subprocess.run(
        ['pytest', '--cov=src', '--cov-report=json', '-q'],
        capture_output=True,
        text=True
    )

    try:
        with open('coverage.json', 'r') as f:
            data = json.load(f)
            return data['totals']['percent_covered']
    except (FileNotFoundError, KeyError):
        return 0.0


def main():
    """Check coverage and exit with appropriate code."""
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 80.0

    coverage = get_coverage_percentage()
    print(f"Current coverage: {coverage:.1f}%")
    print(f"Threshold: {threshold:.1f}%")

    if coverage >= threshold:
        print(f"Coverage is sufficient ({coverage:.1f}% >= {threshold:.1f}%)")
        print("Skipping test generation.")
        sys.exit(0)
    else:
        print(f"Coverage below threshold ({coverage:.1f}% < {threshold:.1f}%)")
        print("Test generation needed.")
        sys.exit(1)


if __name__ == '__main__':
    main()
