# Git Submodule Cloning Guide

##  Important: Submodule Access Requirements

This repository uses Git submodules to include guard services. When cloning, you may encounter issues if you don't have access to all submodule repositories.

## Current Submodule Configuration

The repository includes the following submodules:

| Submodule | Repository | Owner | Access Required |
|-----------|-----------|-------|----------------|
| `guards/tokenguard` | `bravetto/tokenguard` | bravetto |  Required |
| `guards/trust-guard` | `bravetto/trust-guard` | bravetto |  Required |
| `guards/contextguard` | `jimmyjdejesus-cmyk/ContextGuard` | jimmyjdejesus-cmyk |  **May need access** |
| `guards/biasguard-backend` | `bravetto/biasguard-backend` | bravetto |  Required |
| `guards/healthguard` | `bravetto/health-guard-logic` | bravetto |  Required |

## Cloning Scenarios

### Scenario 1: Clone WITHOUT Submodules (Recommended for Users Without Access)

If you don't have access to all submodule repositories, clone without submodules:

```bash
# Clone the main repository only
git clone https://github.com/bravetto/AIGuards-Backend.git
cd AIGuards-Backend

# The guards/ directories will be empty
# You can still work with the gateway and other non-submodule code
```

**Note:** The `guards/` directories will be empty, but the gateway service will still work if you're using Docker Compose (which pulls pre-built images).

### Scenario 2: Clone WITH Submodules (Requires Access)

If you have access to all repositories, clone with submodules:

```bash
# Clone with all submodules
git clone --recursive https://github.com/bravetto/AIGuards-Backend.git
cd AIGuards-Backend
```

**If you get authentication errors:**
- Ensure you have access to all repositories listed above
- Use SSH authentication if HTTPS fails
- Contact repository maintainers for access if needed

### Scenario 3: Selective Submodule Initialization

If you only have access to some submodules:

```bash
# Clone without submodules first
git clone https://github.com/bravetto/AIGuards-Backend.git
cd AIGuards-Backend

# Initialize only the submodules you have access to
git submodule update --init guards/tokenguard
git submodule update --init guards/trust-guard
# Skip submodules you don't have access to
```

## Troubleshooting

### Error: "fatal: could not read Username"

This means you don't have access to a private submodule repository.

**Solution:**
1. Clone without `--recursive` flag
2. The gateway will still work using Docker images
3. Contact repository maintainers for access if you need the source code

### Error: "No submodule mapping found"

This indicates a stale submodule reference.

**Solution:**
```bash
# Sync submodule URLs
git submodule sync

# Update submodules
git submodule update --init --recursive
```

### Empty Submodule Directories After Clone

If `guards/` directories are empty after cloning, this is normal if you didn't use `--recursive`.

**Options:**
1. **Use Docker Compose** - The gateway will pull pre-built images, so empty directories won't affect functionality
2. **Initialize submodules** - Run `git submodule update --init --recursive` if you have access
3. **Skip submodules** - Work with the gateway code only

## Docker Compose Usage

**Good News:** If you're using Docker Compose, empty submodule directories won't prevent the system from running. The Docker images are built separately and pulled from container registries.

```bash
# Even with empty guards/ directories, this will work:
docker-compose up -d
```

## Requesting Access

If you need access to private submodules:

1. Check if the repository is public (try accessing the URL directly)
2. Contact the repository owner:
   - **bravetto repositories**: Contact Bravetto team
   - **jimmyjdejesus-cmyk/ContextGuard**: Contact repository owner
3. Fork the repository if you need to make changes

## Best Practices

1. **For Contributors:** Always clone with `--recursive` if you have access
2. **For Users:** Clone without `--recursive` and use Docker Compose
3. **For CI/CD:** Use `--recursive` with proper authentication setup
4. **Document Access:** Keep this guide updated when submodule permissions change

## Verifying Submodule Status

Check which submodules are initialized:

```bash
git submodule status
```

Expected output for fully initialized:
```
 c0f7a9f guards/biasguard-backend (heads/main)
 761a59a guards/contextguard (heads/feature/merge-contextguard-features)
 f05969a guards/healthguard (heads/dev)
 095b911 guards/tokenguard (heads/feature/migration)
 f27fd49 guards/trust-guard (heads/feature/internal-review-preparation)
```

If you see empty directories or errors, review the troubleshooting section above.

