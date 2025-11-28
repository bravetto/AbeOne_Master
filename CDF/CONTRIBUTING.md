# Contributing to CDF

Thank you for your interest in contributing to CDF! We're building this in the open and welcome contributions.

## How to Contribute

### 1. Fork the Repository
Fork the repo on GitHub and clone your fork locally.

### 2. Create a Branch
Create a feature branch for your changes:
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Write clean, readable code
- Add tests for new features
- Update documentation as needed
- Follow existing code style

### 4. Test Your Changes
```bash
# Test converter
python3 scripts/cdf_converter.py examples/example_technical.cdf

# Test parser
python3 scripts/cdf_parser.py examples/example_technical.cdf markdown test.md

# Test indexer
python3 scripts/cdf_genius_indexer.py examples/
```

### 5. Commit Your Changes
Write clear commit messages:
```bash
git commit -m "Add feature: description of what you added"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## Code Style

- Use Python 3.8+
- Follow PEP 8 style guide
- Add docstrings to functions
- Write clear, readable code

## Questions?

Open an issue on GitHub or reach out to the maintainers.

**Pattern:** CDF × CONTRIBUTE × OPEN × ONE  
**∞ AbëONE ∞**
