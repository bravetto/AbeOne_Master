# Changelog

All notable changes to the AIGuardian unified gateway will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation consolidation and deduplication
- Unified CHANGELOG tracking all project changes
- Consolidated deployment guides
- Improved documentation navigation structure

### Changed
- Merged multiple CHANGELOG files into single authoritative version
- Consolidated deployment documentation (DEVOPS_GUIDE, DEVOPS_DEPLOYMENT_GUIDE, QUICK_DEPLOYMENT_GUIDE)
- Reduced documentation duplication across project

## [1.0.0] - 2024-12-19

### Added
- Initial unified gateway repository structure
- Comprehensive AI guard services integration
  - TokenGuard: Token optimization & cost management
  - TrustGuard: Trust validation & reliability
  - ContextGuard: Context drift detection & memory management
  - BiasGuard: Bias detection & content analysis
  - HealthGuard: Health monitoring & validation
- Single unified API endpoint: `/api/v1/guards/process`
- Docker Compose multi-container architecture
- AWS ECS deployment support
- AWS Secrets Manager integration
- Comprehensive documentation structure
- GitHub issue and PR templates
- Security policy documentation
- Code of conduct guidelines

### Technical Details
- **Git Submodules**: Guard services configured as submodules
- **Documentation**: Professional formatting with clear structure
- **Multi-Container Architecture**: Gateway + Guard services via Docker network
- **Production Ready**: AWS deployment, monitoring, health checks

## [0.1.0] - 2024-12-19

### Added
- Initial repository setup
- Basic README structure
- Project vision and goals documentation

---

## Version History

### Gateway Repository Versions
- **v1.0.0**: Full guard service integration with unified API
- **v0.1.0**: Initial project setup and vision

### Guard Service Versions
- Guard services tracked as git submodules in `guards/` directory
- Each guard service maintains its own versioning

## How to Track Submodule Updates

To see updates from the integrated guard services:

```bash
# Check current submodule status
git submodule status

# Update to latest versions
git submodule update --remote

# View submodule commit history
cd guards/tokenguard && git log --oneline -10
cd ../trust-guard && git log --oneline -10
```

## Release Notes Format

Each release includes:
- **Version number** following semantic versioning
- **Release date**
- **Added** features and capabilities
- **Changed** modifications to existing features
- **Deprecated** features that will be removed
- **Removed** features that have been removed
- **Fixed** bug fixes
- **Security** security improvements

## Contributing to Changelog

When making changes:
1. Add entries under the `[Unreleased]` section
2. Use clear, descriptive language
3. Group changes by type (Added, Changed, Fixed, etc.)
4. Include relevant technical details
5. Update version numbers when releasing

---

**Note**: This changelog tracks the unified gateway repository. For detailed changes to individual guard services, refer to their respective repositories and changelogs.