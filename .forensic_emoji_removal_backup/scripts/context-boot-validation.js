#!/usr/bin/env node
/**
 * CONTEXT BOOT VALIDATION
 * 
 * Runs automatically when AI context window boots
 * Validates project boundaries before any work begins
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class ContextBootValidator {
  constructor() {
    this.workspaceRoot = this.findWorkspaceRoot();
    this.currentDir = process.cwd();
    this.issues = [];
    this.warnings = [];
    this.successes = [];
  }

  /**
   * Find workspace root (where PROJECT_MASTER_INDEX.md exists)
   */
  findWorkspaceRoot() {
    let current = process.cwd();
    const maxDepth = 10;
    let depth = 0;

    while (depth < maxDepth) {
      const masterIndexPath = path.join(current, 'PROJECT_MASTER_INDEX.md');
      if (fs.existsSync(masterIndexPath)) {
        return current;
      }
      const parent = path.dirname(current);
      if (parent === current) break; // Reached filesystem root
      current = parent;
      depth++;
    }

    // Fallback to current directory
    return process.cwd();
  }

  /**
   * Main validation function
   */
  async validate() {
    console.log('\n🛡️  CONTEXT BOOT VALIDATION');
    console.log('='.repeat(60));
    console.log(`Workspace: ${this.workspaceRoot}`);
    console.log(`Current Directory: ${this.currentDir}\n`);

    // Step 1: Validate current directory context
    await this.validateCurrentDirectory();

    // Step 2: Run full boundary validation
    await this.runBoundaryValidation();

    // Step 3: Report results
    this.reportResults();

    // Return exit code
    return this.issues.length === 0 ? 0 : 1;
  }

  /**
   * Validate current directory context
   */
  async validateCurrentDirectory() {
    const statusPath = path.join(this.currentDir, 'PROJECT_STATUS.md');
    const boundaryPath = path.join(this.currentDir, '.project-boundary');
    const masterIndexPath = path.join(this.workspaceRoot, 'PROJECT_MASTER_INDEX.md');

    // Check if we're in a project directory
    if (!fs.existsSync(statusPath) && !fs.existsSync(boundaryPath)) {
      // Not in a project directory - check if we're in workspace root
      if (fs.existsSync(masterIndexPath)) {
        this.warnings.push('Working in workspace root - no specific project context');
        this.warnings.push('  Consider navigating to a project directory before starting work');
        return;
      } else {
        this.warnings.push('No project context detected');
        this.warnings.push('  No PROJECT_STATUS.md or .project-boundary found');
        return;
      }
    }

    // Read PROJECT_STATUS.md
    if (fs.existsSync(statusPath)) {
      const statusContent = fs.readFileSync(statusPath, 'utf8');
      
      // Parse status
      let status = 'UNKNOWN';
      const statusPatterns = [
        /\*\*Status\*\*[:\s*]+(?:✅|⚠️)?[:\s*]+\*\*(LEGACY|ACTIVE|ARCHIVE)\*\*/i,
        /Status[:\s*]+(?:✅|⚠️)?[:\s*]+(LEGACY|ACTIVE|ARCHIVE)/i,
        /Status[:\s]+(LEGACY|ACTIVE|ARCHIVE)/i
      ];
      
      for (const pattern of statusPatterns) {
        const match = statusContent.match(pattern);
        if (match) {
          status = (match[1] || match[0].match(/(LEGACY|ACTIVE|ARCHIVE)/i)?.[0] || 'UNKNOWN').toUpperCase();
          break;
        }
      }

      // Check if LEGACY or ARCHIVE
      if (status === 'LEGACY' || status === 'ARCHIVE') {
        this.issues.push({
          type: 'CRITICAL',
          message: `⚠️ DRIFT DETECTED: Working in ${status} directory`,
          fix: `Redirect to active directory (check PROJECT_STATUS.md for active directory path)`
        });
        return;
      }

      if (status === 'ACTIVE') {
        this.successes.push(`Current directory is ACTIVE: ${path.basename(this.currentDir)}`);
      }
    }

    // Read .project-boundary
    if (fs.existsSync(boundaryPath)) {
      try {
        const boundary = JSON.parse(fs.readFileSync(boundaryPath, 'utf8'));
        if (boundary.status === 'LEGACY') {
          this.issues.push({
            type: 'CRITICAL',
            message: `⚠️ DRIFT DETECTED: Boundary file indicates LEGACY status`,
            fix: `Redirect to active directory: ${boundary.activeDirectory || 'Check PROJECT_MASTER_INDEX.md'}`
          });
        } else if (boundary.status === 'ACTIVE') {
          this.successes.push(`Boundary validation: ACTIVE`);
        }
      } catch (err) {
        this.warnings.push(`Could not parse .project-boundary: ${err.message}`);
      }
    }

    // Check against master index
    if (fs.existsSync(masterIndexPath)) {
      const masterIndex = fs.readFileSync(masterIndexPath, 'utf8');
      const currentDirName = path.basename(this.currentDir);
      
      // Escape special regex characters in directory name
      const escapedDirName = currentDirName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      
      // Check if current directory matches any active directory in master index
      const activePattern = new RegExp(`\\*\\*Active Directory\\*\\*:.*\`${escapedDirName}`, 'i');
      const legacyPattern = new RegExp(`\\*\\*Directory\\*\\*:.*\`${escapedDirName}.*LEGACY`, 'i');
      
      const activeMatch = masterIndex.match(activePattern);
      const legacyMatch = masterIndex.match(legacyPattern);
      
      if (legacyMatch) {
        this.issues.push({
          type: 'CRITICAL',
          message: `⚠️ DRIFT DETECTED: Master index indicates ${currentDirName} is LEGACY`,
          fix: `Check PROJECT_MASTER_INDEX.md for active directory`
        });
      } else if (activeMatch) {
        this.successes.push(`Master index validation: Active directory confirmed`);
      }
    }
  }

  /**
   * Run full boundary validation script
   */
  async runBoundaryValidation() {
    const validationScript = path.join(this.workspaceRoot, 'scripts', 'validate-project-boundaries.js');
    
    if (!fs.existsSync(validationScript)) {
      this.warnings.push('Full boundary validation script not found');
      return;
    }

    try {
      // Run validation script silently and capture output
      const output = execSync(`node "${validationScript}"`, {
        cwd: this.workspaceRoot,
        encoding: 'utf8',
        stdio: 'pipe'
      });
      
      // Parse output for critical issues
      if (output.includes('❌ Issues:')) {
        const issuesMatch = output.match(/❌ Issues: (\d+)/);
        if (issuesMatch && parseInt(issuesMatch[1]) > 0) {
          this.warnings.push(`Full validation found ${issuesMatch[1]} issue(s) - run validation script for details`);
        }
      }
    } catch (err) {
      // Script may exit with non-zero if issues found - that's OK
      this.warnings.push('Full validation script reported issues - check output above');
    }
  }

  /**
   * Report validation results
   */
  reportResults() {
    console.log('\n📊 CONTEXT VALIDATION RESULTS');
    console.log('='.repeat(60));

    if (this.successes.length > 0) {
      console.log(`\n✅ Successes (${this.successes.length}):`);
      this.successes.forEach(s => console.log(`  ✅ ${s}`));
    }

    if (this.warnings.length > 0) {
      console.log(`\n⚠️  Warnings (${this.warnings.length}):`);
      this.warnings.forEach(w => console.log(`  ⚠️  ${w}`));
    }

    if (this.issues.length > 0) {
      console.log(`\n❌ Critical Issues (${this.issues.length}):`);
      this.issues.forEach(issue => {
        console.log(`\n  ${issue.type}: ${issue.message}`);
        console.log(`  Fix: ${issue.fix}`);
      });
    }

    // Summary
    console.log('\n' + '='.repeat(60));
    console.log('📈 SUMMARY');
    console.log('='.repeat(60));
    console.log(`✅ Successes: ${this.successes.length}`);
    console.log(`⚠️  Warnings: ${this.warnings.length}`);
    console.log(`❌ Issues: ${this.issues.length}`);

    if (this.issues.length > 0) {
      console.log('\n🚨 CRITICAL: Drift detected! Do not proceed until resolved.');
      console.log('   Redirect to active directory before starting work.');
    } else if (this.warnings.length > 0) {
      console.log('\n⚠️  Warnings present - review above before proceeding.');
    } else {
      console.log('\n✅ Context validated - safe to proceed.');
    }

    console.log('='.repeat(60) + '\n');
  }

  /**
   * Generate context summary for AI
   */
  generateContextSummary() {
    const summary = {
      workspaceRoot: this.workspaceRoot,
      currentDirectory: this.currentDir,
      projectName: path.basename(this.currentDir),
      status: 'UNKNOWN',
      isActive: false,
      hasDrift: this.issues.length > 0,
      warnings: this.warnings.length,
      issues: this.issues.length
    };

    // Try to determine status
    const statusPath = path.join(this.currentDir, 'PROJECT_STATUS.md');
    if (fs.existsSync(statusPath)) {
      const statusContent = fs.readFileSync(statusPath, 'utf8');
      const statusMatch = statusContent.match(/\*\*Status\*\*[:\s*]+(?:✅|⚠️)?[:\s*]+\*\*(LEGACY|ACTIVE|ARCHIVE)\*\*/i);
      if (statusMatch) {
        summary.status = statusMatch[1].toUpperCase();
        summary.isActive = summary.status === 'ACTIVE';
      }
    }

    return summary;
  }
}

// Run validation if called directly
if (require.main === module) {
  const validator = new ContextBootValidator();
  validator.validate().then(exitCode => {
    process.exit(exitCode);
  }).catch(err => {
    console.error('Validation error:', err);
    process.exit(1);
  });
}

module.exports = ContextBootValidator;

