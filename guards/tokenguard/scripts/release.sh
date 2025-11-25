#!/usr/bin/env bash
# Release automation script for TokenGuard microservice.
#
# This script helps with:
# - Version bumping
# - Changelog updates
# - Git tagging
# - Build validation
set -e

# Configuration
PROJECT_NAME="tokenguard-microservice"
MAIN_BRANCH="main"
PYPROJECT_FILE="pyproject.toml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if we're on main branch
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
        log_error "Must be on $MAIN_BRANCH branch. Currently on: $CURRENT_BRANCH"
        exit 1
    fi
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        log_error "Working directory is not clean. Please commit or stash changes."
        exit 1
    fi
    
    # Check if up to date with remote
    git fetch origin
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse origin/$MAIN_BRANCH)
    if [ "$LOCAL" != "$REMOTE" ]; then
        log_error "Local branch is not up to date with remote. Please pull latest changes."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

get_current_version() {
    grep '^version = ' $PYPROJECT_FILE | sed 's/version = "\(.*\)"/\1/'
}

bump_version() {
    local version_type=$1
    local current_version=$(get_current_version)
    
    log_info "Current version: $current_version"
    
    # Simple version bumping (assumes semantic versioning)
    IFS='.' read -ra VERSION_PARTS <<< "$current_version"
    MAJOR=${VERSION_PARTS[0]}
    MINOR=${VERSION_PARTS[1]}
    PATCH=${VERSION_PARTS[2]}
    
    case $version_type in
        major)
            MAJOR=$((MAJOR + 1))
            MINOR=0
            PATCH=0
            ;;
        minor)
            MINOR=$((MINOR + 1))
            PATCH=0
            ;;
        patch)
            PATCH=$((PATCH + 1))
            ;;
        *)
            log_error "Invalid version type: $version_type. Use: major, minor, or patch"
            exit 1
            ;;
    esac
    
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    log_info "New version: $NEW_VERSION"
    
    # Update pyproject.toml
    sed -i "s/^version = .*/version = \"$NEW_VERSION\"/" $PYPROJECT_FILE
    
    echo $NEW_VERSION
}

run_tests() {
    log_info "Running test suite..."
    
    # Run tests
    if ! make test; then
        log_error "Tests failed. Aborting release."
        exit 1
    fi
    
    # Run linting
    if ! make lint; then
        log_error "Linting failed. Aborting release."
        exit 1
    fi
    
    log_success "All tests passed"
}

update_changelog() {
    local version=$1
    local date=$(date +"%Y-%m-%d")
    
    log_info "Updating CHANGELOG.md..."
    
    # Replace [Unreleased] with version and date
    sed -i "s/## \[Unreleased\]/## [$version] - $date/" CHANGELOG.md
    
    # Add new Unreleased section
    sed -i "/## \[$version\] - $date/i ## [Unreleased]\n\n### Added\n\n### Changed\n\n### Fixed\n\n### Security\n" CHANGELOG.md
    
    log_success "CHANGELOG.md updated"
}

create_release_commit() {
    local version=$1
    
    log_info "Creating release commit..."
    
    git add $PYPROJECT_FILE CHANGELOG.md
    git commit -m "Release v$version

- Bump version to $version
- Update changelog
"
    
    log_success "Release commit created"
}

create_git_tag() {
    local version=$1
    
    log_info "Creating git tag..."
    
    git tag -a "v$version" -m "Release v$version"
    
    log_success "Git tag v$version created"
}

push_changes() {
    local version=$1
    
    log_info "Pushing changes to remote..."
    
    git push origin $MAIN_BRANCH
    git push origin "v$version"
    
    log_success "Changes pushed to remote"
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] VERSION_TYPE

Release automation script for $PROJECT_NAME

VERSION_TYPE:
    major    Bump major version (breaking changes)
    minor    Bump minor version (new features)
    patch    Bump patch version (bug fixes)

OPTIONS:
    -h, --help       Show this help message
    -n, --dry-run    Show what would be done without making changes
    --skip-tests     Skip running tests (not recommended)

Examples:
    $0 patch         # 1.0.0 -> 1.0.1
    $0 minor         # 1.0.1 -> 1.1.0
    $0 major         # 1.1.0 -> 2.0.0
    $0 --dry-run patch
EOF
}

main() {
    local version_type=""
    local dry_run=false
    local skip_tests=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -n|--dry-run)
                dry_run=true
                shift
                ;;
            --skip-tests)
                skip_tests=true
                shift
                ;;
            major|minor|patch)
                version_type=$1
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    if [ -z "$version_type" ]; then
        log_error "Version type is required"
        show_usage
        exit 1
    fi
    
    log_info "Starting release process for $PROJECT_NAME..."
    log_info "Version type: $version_type"
    if [ "$dry_run" = true ]; then
        log_warning "DRY RUN MODE - No changes will be made"
    fi
    
    # Run checks
    if [ "$dry_run" = false ]; then
        check_prerequisites
    fi
    
    # Get new version
    if [ "$dry_run" = true ]; then
        current_version=$(get_current_version)
        log_info "Would bump version from $current_version"
        exit 0
    fi
    
    new_version=$(bump_version $version_type)
    
    # Run tests
    if [ "$skip_tests" = false ]; then
        run_tests
    else
        log_warning "Skipping tests as requested"
    fi
    
    # Update changelog
    update_changelog $new_version
    
    # Create release commit
    create_release_commit $new_version
    
    # Create git tag
    create_git_tag $new_version
    
    # Push changes
    push_changes $new_version
    
    log_success "Release v$new_version completed successfully!"
    log_info "Next steps:"
    log_info "1. Check the GitHub release page"
    log_info "2. Update any deployment configurations"
    log_info "3. Monitor the deployment"
}

# Run main function
main "$@"