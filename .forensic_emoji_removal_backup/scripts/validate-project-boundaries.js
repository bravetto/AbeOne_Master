#!/usr/bin/env node
/**
 * Project Boundary Validation Script
 * 
 * Validates project boundaries and detects drift/bleed
 * Run: node scripts/validate-project-boundaries.js
 */

const fs = require('fs');
const path = require('path');

// GLOBAL_IGNORES: Unified ignore pattern for all traversals
const GLOBAL_IGNORES = [
  'node_modules',
  '.git',
  'dist',
  'build',
  '.next',
  'out',
  '.vscode',
  '.idea',
  '__pycache__',
  '.DS_Store',
  'Thumbs.db'
];

class ProjectBoundaryValidator {
  constructor() {
    this.workspaceRoot = path.resolve(__dirname, '..');
    this.issues = [];
    this.warnings = [];
    this.successes = [];
  }

  /**
   * Main validation function
   */
  async validate() {
    console.log('🛡️  PROJECT BOUNDARY VALIDATION');
    console.log('='.repeat(60));
    console.log(`Workspace: ${this.workspaceRoot}\n`);

    // Step 1: Check master index exists
    await this.validateMasterIndex();

    // Step 2: Validate all project directories
    await this.validateProjectDirectories();

    // Step 3: Check for drift
    await this.detectDrift();

    // Step 4: Check for bleed
    await this.detectBleed();

    // Step 5: Report results
    this.reportResults();
  }

  /**
   * Validate master index exists and is valid
   */
  async validateMasterIndex() {
    const masterIndexPath = path.join(this.workspaceRoot, 'PROJECT_MASTER_INDEX.md');
    
    if (!fs.existsSync(masterIndexPath)) {
      this.issues.push({
        type: 'CRITICAL',
        message: 'PROJECT_MASTER_INDEX.md not found',
        fix: 'Create PROJECT_MASTER_INDEX.md in workspace root'
      });
      return;
    }

    this.successes.push('Master index found');
    
    // Read and parse master index
    const content = fs.readFileSync(masterIndexPath, 'utf8');
    
    // Check for active projects
    if (!content.includes('ACTIVE')) {
      this.warnings.push('Master index may not have active projects listed');
    }
  }

  /**
   * Validate all project directories
   */
  async validateProjectDirectories() {
    const projects = [
      { name: 'AiGuardian Chrome Extension', dir: 'AiGuardian-Chrome-Ext-orbital', expectedStatus: 'ACTIVE' },
      { name: 'AI Guardians Chrome Extension (Legacy)', dir: '_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext', expectedStatus: 'ARCHIVED', isArchived: true },
      { name: 'AIGuards Backend', dir: 'AIGuards-Backend', expectedStatus: 'ACTIVE' },
      { name: 'Emergent OS', dir: 'EMERGENT_OS', expectedStatus: 'ACTIVE' }
    ];

    for (const project of projects) {
      await this.validateProject(project);
    }
  }

  /**
   * Validate a single project
   */
  async validateProject(project) {
    const projectPath = path.join(this.workspaceRoot, project.dir);
    
    if (!fs.existsSync(projectPath)) {
      this.warnings.push(`Project directory not found: ${project.dir}`);
      return;
    }

    // Check PROJECT_STATUS.md
    const statusPath = path.join(projectPath, 'PROJECT_STATUS.md');
    if (!fs.existsSync(statusPath)) {
      this.issues.push({
        type: 'HIGH',
        message: `PROJECT_STATUS.md missing in ${project.dir}`,
        fix: `Create PROJECT_STATUS.md in ${project.dir}/`
      });
      return;
    }

    const statusContent = fs.readFileSync(statusPath, 'utf8');
    
    // SUBSTRATE-REQUIRED: Validate markdown structure before parsing
    if (!statusContent || statusContent.trim().length === 0) {
      this.issues.push({
        type: 'HIGH',
        message: `PROJECT_STATUS.md is empty in ${project.dir}`,
        fix: `Add status information to ${project.dir}/PROJECT_STATUS.md`
      });
      return;
    }
    
    // Validate required sections exist
    const hasStatusSection = /Status/i.test(statusContent);
    if (!hasStatusSection) {
      this.issues.push({
        type: 'HIGH',
        message: `PROJECT_STATUS.md missing Status section in ${project.dir}`,
        fix: `Add status section to ${project.dir}/PROJECT_STATUS.md (format: **Status**: ✅ **ACTIVE**)`
      });
      return;
    }
    
    // Parse status from markdown - handles formats like:
    // **Status**: ✅ **ACTIVE**
    // Status: ACTIVE
    // **Status**: ⚠️ **LEGACY**
    let status = 'UNKNOWN';
    const statusPatterns = [
      /Status[:\s*]+(?:✅|⚠️)?[:\s*]+(?:LEGACY|ACTIVE|ARCHIVE)/i,
      /\*\*Status\*\*[:\s*]+(?:✅|⚠️)?[:\s*]+\*\*(LEGACY|ACTIVE|ARCHIVE)\*\*/i,
      /Status[:\s]+(LEGACY|ACTIVE|ARCHIVE)/i
    ];
    
    for (const pattern of statusPatterns) {
      const match = statusContent.match(pattern);
      if (match) {
        // Extract status from match (handle different capture groups)
        status = match[1] || match[0].match(/(LEGACY|ACTIVE|ARCHIVE)/i)?.[0] || 'UNKNOWN';
        status = status.toUpperCase();
        break;
      }
    }
    
    // SUBSTRATE-REQUIRED: If status still UNKNOWN after parsing, report error
    if (status === 'UNKNOWN') {
      this.warnings.push(`Could not parse status from ${statusPath}`);
      this.warnings.push(`Expected format: **Status**: ✅ **ACTIVE**`);
      this.warnings.push(`SUBSTRATE-REQUIRED: Invalid PROJECT_STATUS.md structure in ${project.dir}`);
      this.warnings.push(`Provide example and required sections.`);
    }

    // Check .project-boundary
    const boundaryPath = path.join(projectPath, '.project-boundary');
    if (!fs.existsSync(boundaryPath)) {
      this.issues.push({
        type: 'MEDIUM',
        message: `.project-boundary missing in ${project.dir}`,
        fix: `Create .project-boundary in ${project.dir}/`
      });
    } else {
      try {
        const boundary = JSON.parse(fs.readFileSync(boundaryPath, 'utf8'));
        if (boundary.status !== project.expectedStatus) {
          this.issues.push({
            type: 'HIGH',
            message: `Status mismatch in ${project.dir}: Expected ${project.expectedStatus}, Got ${boundary.status}`,
            fix: `Update .project-boundary status to ${project.expectedStatus}`
          });
        } else {
          this.successes.push(`${project.dir}: Status validated (${boundary.status})`);
        }
      } catch (err) {
        this.issues.push({
          type: 'MEDIUM',
          message: `Invalid .project-boundary JSON in ${project.dir}`,
          fix: `Fix JSON syntax in ${project.dir}/.project-boundary`
        });
      }
    }

    // Validate status matches expected (only warn if clearly different)
    if (status !== 'UNKNOWN' && status !== project.expectedStatus && !status.includes(project.expectedStatus)) {
      this.warnings.push(`${project.dir}: Status may not match expected (found: ${status}, expected: ${project.expectedStatus})`);
    }
  }

  /**
   * Detect drift (working in wrong directory)
   */
  async detectDrift() {
    // Check for modifications in legacy/archived directories
    const legacyDirs = ['_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext'];
    
    // Boundary system files that are expected to be modified during setup
    const boundaryFiles = ['PROJECT_STATUS.md', '.project-boundary'];
    
    for (const dir of legacyDirs) {
      const dirPath = path.join(this.workspaceRoot, dir);
      if (fs.existsSync(dirPath)) {
        // Check for recent modifications in code files (exclude boundary files)
        const checkForCodeModifications = (dirPath) => {
          const items = fs.readdirSync(dirPath);
          let hasRecentCodeChanges = false;
          let lastCodeModification = null;
          
          for (const item of items) {
            // Skip boundary files and hidden directories
            if (boundaryFiles.includes(item) || item.startsWith('.')) {
              continue;
            }
            
            const itemPath = path.join(dirPath, item);
            const stats = fs.statSync(itemPath);
            
            if (stats.isDirectory()) {
              // Recursively check subdirectories (limit depth to avoid performance issues)
              const subItems = fs.readdirSync(itemPath);
              for (const subItem of subItems) {
                if (boundaryFiles.includes(subItem)) continue;
                const subItemPath = path.join(itemPath, subItem);
                try {
                  const subStats = fs.statSync(subItemPath);
                  if (subStats.isFile()) {
                    const hoursSinceModified = (Date.now() - subStats.mtimeMs) / (1000 * 60 * 60);
                    if (hoursSinceModified < 24) {
                      hasRecentCodeChanges = true;
                      if (!lastCodeModification || subStats.mtimeMs > lastCodeModification.getTime()) {
                        lastCodeModification = new Date(subStats.mtimeMs);
                      }
                    }
                  }
                } catch (err) {
                  // Skip files we can't access
                }
              }
            } else {
              const hoursSinceModified = (Date.now() - stats.mtimeMs) / (1000 * 60 * 60);
              if (hoursSinceModified < 24) {
                hasRecentCodeChanges = true;
                if (!lastCodeModification || stats.mtimeMs > lastCodeModification.getTime()) {
                  lastCodeModification = new Date(stats.mtimeMs);
                }
              }
            }
          }
          
          return { hasRecentCodeChanges, lastCodeModification };
        };
        
        const { hasRecentCodeChanges, lastCodeModification } = checkForCodeModifications(dirPath);
        
        if (hasRecentCodeChanges) {
          this.warnings.push(`Recent code modifications detected in legacy directory: ${dir}`);
          this.warnings.push(`  Last code modification: ${lastCodeModification}`);
          this.warnings.push(`  Check if work should be in active directory instead`);
          this.warnings.push(`  Note: Boundary files (PROJECT_STATUS.md, .project-boundary) are excluded from this check`);
        }
      }
    }
  }

  /**
   * Detect bleed (code from one project leaking into another)
   */
  async detectBleed() {
    // Check for imports from legacy/archived directories
    const activeDir = path.join(this.workspaceRoot, 'AiGuardian-Chrome-Ext-orbital');
    if (fs.existsSync(activeDir)) {
      // Check for imports from archived legacy directory
      await this.checkImports(activeDir, '_ARCHIVE/legacy-projects/AI-Guardians-chrome-ext');
      // Also check old path in case of stale references
      await this.checkImports(activeDir, 'AI-Guardians-chrome-ext');
    }
  }

  /**
   * Check for imports from other projects
   */
  async checkImports(projectDir, otherProject) {
    const srcDir = path.join(projectDir, 'src');
    if (!fs.existsSync(srcDir)) return;

    const files = this.getAllFiles(srcDir, ['.js', '.ts', '.jsx', '.tsx']);
    
    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      
      // Check for imports from other project
      const importRegex = new RegExp(`['"]\\.\\./.*${otherProject}`, 'g');
      const matches = content.match(importRegex);
      
      if (matches) {
        this.warnings.push(`Potential bleed detected in ${path.relative(this.workspaceRoot, file)}`);
        this.warnings.push(`  Imports from ${otherProject}: ${matches.join(', ')}`);
        this.warnings.push(`  Verify this is intentional and documented`);
      }
    }
  }

  /**
   * Get all files with specific extensions
   */
  getAllFiles(dir, extensions) {
    let results = [];
    const list = fs.readdirSync(dir);
    
    for (const file of list) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      
      if (stat && stat.isDirectory()) {
        if (GLOBAL_IGNORES.includes(file)) continue;
        results = results.concat(this.getAllFiles(filePath, extensions));
      } else {
        const ext = path.extname(file);
        if (extensions.includes(ext)) {
          results.push(filePath);
        }
      }
    }
    
    return results;
  }

  /**
   * Report validation results
   */
  reportResults() {
    console.log('\n📊 VALIDATION RESULTS');
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
      console.log(`\n❌ Issues (${this.issues.length}):`);
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

    const totalChecks = this.successes.length + this.warnings.length + this.issues.length;
    const successRate = totalChecks > 0 ? (this.successes.length / totalChecks * 100).toFixed(1) : 0;
    
    console.log(`\n📊 Success Rate: ${successRate}%`);

    if (this.issues.length === 0 && this.warnings.length === 0) {
      console.log('\n🎉 ALL VALIDATIONS PASSED! Project boundaries are clear.');
    } else if (this.issues.length === 0) {
      console.log('\n✅ No critical issues. Review warnings above.');
    } else {
      console.log('\n⚠️  Issues detected. Review and fix above.');
      process.exit(1);
    }
  }
}

// Run validation
if (require.main === module) {
  const validator = new ProjectBoundaryValidator();
  validator.validate().catch(err => {
    console.error('Validation error:', err);
    process.exit(1);
  });
}

module.exports = ProjectBoundaryValidator;

