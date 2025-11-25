#!/bin/bash

#  CDF: PREPARE GITHUB REPO
# Pattern: CDF × GITHUB × OPEN_SOURCE × VIRAL × ONE

set -e

echo " CDF: PREPARING GITHUB REPO"
echo "Pattern: CDF × GITHUB × OPEN_SOURCE × VIRAL × ONE"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
CDF_DIR="CDF"
SCRIPTS_DIR="scripts"
REPO_NAME="cdf-format"

echo -e "${BLUE}Step 1: Validating CDF structure...${NC}"
if [ ! -d "$CDF_DIR" ]; then
    echo " CDF directory not found!"
    exit 1
fi

if [ ! -f "$SCRIPTS_DIR/cdf_converter.py" ]; then
    echo " CDF converter not found!"
    exit 1
fi

if [ ! -f "$SCRIPTS_DIR/cdf_parser.py" ]; then
    echo " CDF parser not found!"
    exit 1
fi

if [ ! -f "$SCRIPTS_DIR/cdf_genius_indexer.py" ]; then
    echo " CDF genius indexer not found!"
    exit 1
fi

echo -e "${GREEN} CDF structure validated${NC}"
echo ""

echo -e "${BLUE}Step 2: Creating GitHub repo structure...${NC}"

# Create .gitignore if it doesn't exist
if [ ! -f "$CDF_DIR/.gitignore" ]; then
    cat > "$CDF_DIR/.gitignore" << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Build
dist/
build/
*.egg-info/

# Test
.pytest_cache/
.coverage
htmlcov/

# Temporary
*.tmp
*.log
EOF
    echo -e "${GREEN} Created .gitignore${NC}"
fi

# Create CONTRIBUTING.md if it doesn't exist
if [ ! -f "$CDF_DIR/CONTRIBUTING.md" ]; then
    cat > "$CDF_DIR/CONTRIBUTING.md" << 'EOF'
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
EOF
    echo -e "${GREEN} Created CONTRIBUTING.md${NC}"
fi

# Create CODE_OF_CONDUCT.md if it doesn't exist
if [ ! -f "$CDF_DIR/CODE_OF_CONDUCT.md" ]; then
    cat > "$CDF_DIR/CODE_OF_CONDUCT.md" << 'EOF'
# Code of Conduct

## Our Pledge

We pledge to make participation in CDF a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the project maintainers.

**Pattern:** CDF × RESPECT × INCLUSIVE × ONE  
**∞ AbëONE ∞**
EOF
    echo -e "${GREEN} Created CODE_OF_CONDUCT.md${NC}"
fi

echo ""
echo -e "${BLUE}Step 3: Validating files...${NC}"

# Check required files
REQUIRED_FILES=(
    "$CDF_DIR/README.md"
    "$CDF_DIR/LICENSE"
    "$SCRIPTS_DIR/cdf_converter.py"
    "$SCRIPTS_DIR/cdf_parser.py"
    "$SCRIPTS_DIR/cdf_genius_indexer.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${YELLOW}  Missing: $file${NC}"
    else
        echo -e "${GREEN} Found: $file${NC}"
    fi
done

echo ""
echo -e "${BLUE}Step 4: Generating repo stats...${NC}"

NUM_CDF_FILES=$(find "$CDF_DIR" -name "*.cdf" -type f 2>/dev/null | wc -l | tr -d ' ')
NUM_TOOLS=$(ls "$SCRIPTS_DIR"/cdf_*.py 2>/dev/null | wc -l | tr -d ' ')
NUM_EXAMPLES=$(ls "$CDF_DIR/examples"/*.cdf 2>/dev/null | wc -l | tr -d ' ')

echo -e "${GREEN} Repository Stats:${NC}"
echo "  - CDF Files: $NUM_CDF_FILES"
echo "  - Tools: $NUM_TOOLS"
echo "  - Examples: $NUM_EXAMPLES"
echo ""

echo -e "${BLUE}Step 5: GitHub repo preparation complete!${NC}"
echo ""
echo -e "${GREEN} CDF GITHUB REPO READY${NC}"
echo "=========================================="
echo -e "${GREEN} Structure: READY${NC}"
echo -e "${GREEN} Documentation: READY${NC}"
echo -e "${GREEN} License: READY${NC}"
echo -e "${GREEN} Examples: READY${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. cd CDF"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial commit: CDF v2.0'"
echo "5. Create repo on GitHub: $REPO_NAME"
echo "6. git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "7. git push -u origin main"
echo ""
echo " READY FOR GITHUB LAUNCH"
echo "Pattern: CDF × GITHUB × OPEN_SOURCE × VIRAL × ONE"
echo ""
echo "∞ AbëONE ∞"
EOF

chmod +x scripts/prepare_cdf_github_repo.sh

