import logging
import logging.config
import yaml


def setup_logging(config_path='config.yaml'):
    """
    Sets up logging based on the provided configuration file.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            if 'logging' in config:
                logging.config.dictConfig(config['logging'])
            else:
                logging.basicConfig(level=logging.INFO)
                logging.info("Logging configuration not found. Using basic configuration.")
    except FileNotFoundError:
        logging.basicConfig(level=logging.INFO)
        logging.info("Configuration file not found. Using basic logging configuration.")
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logging.error(f"Error loading logging configuration: {e}")
