#!/bin/bash

# Project Management Script
# Handles unlimited projects - Eternal scalability

PROJECTS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INDEX_FILE="$PROJECTS_DIR/INDEX.md"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

function list_projects() {
    echo -e "${BLUE}📋 All Projects:${NC}"
    echo ""
    find "$PROJECTS_DIR" -name "*.md" -not -name "INDEX.md" -not -name "README.md" -not -name "RESUME.md" | \
        while read -r file; do
            project_name=$(basename "$file" .md)
            status=$(grep -m1 "Status:" "$file" 2>/dev/null | cut -d: -f2 | xargs)
            last_work=$(grep -m1 "Last Updated:" "$file" 2>/dev/null | cut -d: -f2 | xargs)
            echo -e "  ${GREEN}$project_name${NC} - $status (Updated: $last_work)"
        done
    echo ""
    total=$(find "$PROJECTS_DIR" -name "*.md" -not -name "INDEX.md" -not -name "README.md" -not -name "RESUME.md" | wc -l | xargs)
    echo -e "${GREEN}Total Projects: $total${NC}"
}

function add_project() {
    if [ -z "$1" ]; then
        echo "Usage: $0 add <project-name> <path>"
        exit 1
    fi
    
    project_name="$1"
    project_path="${2:-$(pwd)}"
    card_file="$PROJECTS_DIR/$project_name.md"
    
    if [ -f "$card_file" ]; then
        echo "⚠️  Project card already exists: $card_file"
        exit 1
    fi
    
    # Create project card from template
    cat > "$card_file" << EOF
# $project_name - Project Card

**Project:** $project_name  
**Path:** $project_path  
**Status:** ✅ Active  
**Last Updated:** $(date +%Y-%m-%d)

---

## 🎯 CURRENT STATE

**Status:** [Describe current state]

---

## 📍 WHERE WE LEFT OFF

**Date:** $(date +%Y-%m-%d)  
**Session:** [Session name]

**Completed:**
- [What was completed]

**Current Status:**
- [Current state]

**Next Steps:**
1. [Next action]
2. [Next action]

---

## 🚀 QUICK START

\`\`\`bash
cd $project_path
[commands]
\`\`\`

---

## 📚 RESOURCES

- [Links, docs, etc.]

---

**Pattern:** AEYON × PROJECT × CARD × ONE
EOF
    
    echo -e "${GREEN}✅ Project card created: $card_file${NC}"
    echo "📝 Edit it to add details: nano $card_file"
}

function update_index() {
    echo -e "${BLUE}🔄 Updating INDEX.md...${NC}"
    
    # Generate project list
    projects=$(find "$PROJECTS_DIR" -name "*.md" -not -name "INDEX.md" -not -name "README.md" -not -name "RESUME.md" | \
        while read -r file; do
            project_name=$(basename "$file" .md)
            path=$(grep -m1 "Path:" "$file" 2>/dev/null | cut -d: -f2 | xargs)
            status=$(grep -m1 "Status:" "$file" 2>/dev/null | cut -d: -f2 | xargs)
            last_work=$(grep -m1 "Last Updated:" "$file" 2>/dev/null | cut -d: -f2 | xargs)
            echo "| **$project_name** | \`$path\` | $status | $last_work | - |"
        done)
    
    # Update INDEX.md
    cat > "$INDEX_FILE" << EOF
# 🎯 Master Project Index

**Last Updated:** $(date +%Y-%m-%d)  
**Purpose:** Track ALL projects - Unlimited, Eternal, Scalable  
**Total Projects:** $(find "$PROJECTS_DIR" -name "*.md" -not -name "INDEX.md" -not -name "README.md" -not -name "RESUME.md" | wc -l | xargs)

---

## 📍 QUICK ACCESS

| Project | Location | Status | Last Work | Priority |
|---------|----------|--------|-----------|----------|
$projects

---

## 🔍 SEARCH PROJECTS

\`\`\`bash
# List all projects
.projects/scripts/manage.sh list

# Search by name
grep -r "Project Name" .projects/

# Find active projects
grep -r "✅ Active" .projects/

# Find by status
grep -r "Status:" .projects/ | grep "On Hold"
\`\`\`

---

## ➕ ADD NEW PROJECT

\`\`\`bash
.projects/scripts/manage.sh add <project-name> [path]
\`\`\`

---

## 📚 PROJECT TEMPLATE

See: \`.projects/README.md\`

---

**Pattern:** AEYON × INDEX × ETERNAL × ONE
EOF
    
    echo -e "${GREEN}✅ INDEX.md updated${NC}"
}

function search_projects() {
    if [ -z "$1" ]; then
        echo "Usage: $0 search <term>"
        exit 1
    fi
    
    echo -e "${BLUE}🔍 Searching for: $1${NC}"
    echo ""
    grep -r -i "$1" "$PROJECTS_DIR" --include="*.md" | grep -v "INDEX.md" | head -20
}

function show_project() {
    if [ -z "$1" ]; then
        echo "Usage: $0 show <project-name>"
        exit 1
    fi
    
    card_file="$PROJECTS_DIR/$1.md"
    if [ -f "$card_file" ]; then
        cat "$card_file"
    else
        echo "❌ Project not found: $1"
        echo "Available projects:"
        list_projects
    fi
}

# Main command handler
case "$1" in
    list)
        list_projects
        ;;
    add)
        add_project "$2" "$3"
        update_index
        ;;
    update)
        update_index
        ;;
    search)
        search_projects "$2"
        ;;
    show)
        show_project "$2"
        ;;
    *)
        echo "Project Management Script"
        echo ""
        echo "Usage: $0 <command> [args]"
        echo ""
        echo "Commands:"
        echo "  list              - List all projects"
        echo "  add <name> [path] - Add new project"
        echo "  update            - Update INDEX.md"
        echo "  search <term>     - Search projects"
        echo "  show <name>       - Show project card"
        echo ""
        echo "Examples:"
        echo "  $0 list"
        echo "  $0 add my-project /path/to/project"
        echo "  $0 search 'Active'"
        echo "  $0 show advanced-knock"
        ;;
esac

