import sys
import os
import yaml
import logging
import json
import csv
import argparse

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from poisonguard.core import DataSample
from poisonguard.analyzer import Analyzer
from poisonguard.mitigator import Mitigator
from poisonguard.reporter import Reporter
from poisonguard.logger import setup_logging


def load_config(config_path='config.yaml'):
    """
    Loads the configuration from a YAML file.
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def load_data(file_path: str) -> list[DataSample]:
    """
    Loads data from a JSON or CSV file.
    """
    samples = []
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            for item in data:
                samples.append(DataSample(**item))
    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'metadata' in row and row['metadata'] == '':
                    row['metadata'] = None
                samples.append(DataSample(**row))
    return samples


def main():
    """
    Main function to run the PoisonGuard analysis pipeline.
    """
    parser = argparse.ArgumentParser(description="Run PoisonGuard analysis.")
    parser.add_argument("file_path", help="Path to the data file (JSON or CSV).")
    args = parser.parse_args()

    # 1. Load the configuration and set up logging
    config = load_config()
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("--- Starting PoisonGuard Analysis ---")

    # 2. Load data from the specified file
    samples = load_data(args.file_path)
    logger.info(f"Loaded {len(samples)} data samples from {args.file_path}.")

    # 3. Instantiate and run the Analyzer with the loaded configuration
    analyzer = Analyzer(config)
    analysis_results = analyzer.analyze(samples)
    logger.info("--- Analysis Complete ---")

    # 4. Instantiate and run the Mitigator
    mitigator = Mitigator(config)
    mitigation_actions = mitigator.mitigate(samples, analysis_results)
    logger.info("--- Mitigation Complete ---")

    # 5. Instantiate the Reporter and generate a report
    reporter = Reporter()
    report = reporter.generate_report(analysis_results, mitigation_actions)

    # 6. Print the formatted report
    formatted_report = reporter.format_report(report)
    print("\n" + formatted_report)
    logger.info("--- Report Generated ---")


if __name__ == "__main__":
    main()