# PoisonGuard Documentation

Welcome to the documentation for PoisonGuard, a tool designed to help diagnose and mitigate LLM poisoning.

## Installation

To install PoisonGuard, you can clone the repository and install the dependencies using pip:

```bash
git clone https://github.com/vibecoders/poisonguard.git
cd poisonguard
pip install .
```

## Usage

PoisonGuard can be run from the command line using the example script provided in the `scripts` directory:

```bash
python scripts/run_analysis.py data/samples.json
```

## API Usage

The PoisonGuard API provides a simple way to integrate the analysis and mitigation functionality into other services.

### Running the API Server

To run the API server, use the following command:

```bash
python -m src.poisonguard.api
```

The server will be available at `http://localhost:8000`.

### Endpoints

The API provides the following endpoints:

- **`POST /analyze`**: Analyzes a list of data samples and returns the analysis results.

  **Request Body:**
  ```json
  {
    "samples": [
      {
        "id": "sample-001",
        "content": "This is a test sample."
      }
    ]
  }
  ```

- **`POST /mitigate`**: Analyzes a list of data samples and returns the mitigation actions.

  **Request Body:**
  ```json
  {
    "samples": [
      {
        "id": "sample-001",
        "content": "This is a test sample."
      }
    ]
  }
  ```

- **`POST /report`**: Analyzes a list of data samples and returns a full report.

  **Request Body:**
  ```json
  {
    "samples": [
      {
        "id": "sample-001",
        "content": "This is a test sample."
      }
    ]
  }
  ```

## Configuration

PoisonGuard's behavior can be customized through the `config.yaml` file. This file allows you to specify various parameters for the analysis engine, mitigation strategies, and logging.

### Analyzer Configuration

The `analyzer` section of the `config.yaml` file allows you to configure the analysis plugins. Each plugin has a `name`, `class`, and `config` section.

```yaml
analyzer:
  plugins:
    - name: "keyword"
      class: "heuristics.KeywordPlugin"
      config:
        keyword_list:
          - "exploit"
          - "vulnerability"
    - name: "length"
      class: "heuristics.LengthPlugin"
      config:
        min_length: 10
        max_length: 5000
    - name: "model"
      class: "model.ModelPlugin"
      config:
        model_name: "distilbert-base-uncased-finetuned-sst-2-english"
        toxicity_threshold: 0.95
```

### Mitigator Configuration

The `mitigator` section of the `config.yaml` file allows you to define the mitigation strategy.

- **`default_action`**: The default action to take when a threat is detected. Options: `"flag"`, `"sanitize"`, `"redact"`.
- **`sanitize_keywords`**: A list of keywords to be removed when the `"sanitize"` action is used.

```yaml
mitigator:
  default_action: "flag"
  sanitize_keywords:
    - "exploit"
    - "vulnerability"
```

### Logging Configuration

The `logging` section of the `config.yaml` file allows you to configure the logging behavior.

```yaml
logging:
  version: 1
  formatters:
    standard:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    file:
      class: "logging.FileHandler"
      level: "INFO"
      formatter: "standard"
      filename: "poisonguard.log"
  root:
    level: "INFO"
    handlers:
      - "file"
```

## Validation Report

For a summary of the testing and validation strategies used in the project, please see the [validation report](./validation.md).


## Contributing

We welcome contributions to PoisonGuard. Please see the [contributing guidelines](../CONTRIBUTING.md) for more information.