#!/usr/bin/env node
/**
 * ENHANCED IMPORT VALIDATOR
 * 
 * Validates imports across project boundaries
 * Detects: static imports, dynamic imports, require statements, dependencies
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz)
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

class EnhancedImportValidator {
  constructor(workspaceRoot) {
    this.workspaceRoot = workspaceRoot;
    this.issues = [];
    this.warnings = [];
    this.projects = this.loadProjects();
  }

  loadProjects() {
    const masterIndexPath = path.join(this.workspaceRoot, 'PROJECT_MASTER_INDEX.md');
    if (!fs.existsSync(masterIndexPath)) {
      return [];
    }

    const content = fs.readFileSync(masterIndexPath, 'utf8');
    const projects = [];

    // Parse active projects
    const activeMatch = content.match(/##  \*\*ACTIVE PROJECTS\*\*([\s\S]*?)## /);
    if (activeMatch) {
      const activeProjects = activeMatch[1].match(/- \*\*Active Directory\*\*: `([^`]+)`/g);
      if (activeProjects) {
        activeProjects.forEach(match => {
          const dir = match.match(/`([^`]+)`/)[1];
          projects.push({ dir, status: 'ACTIVE' });
        });
      }
    }

    // Parse legacy projects
    const legacyMatch = content.match(/##  \*\*LEGACY PROJECTS\*\*([\s\S]*?)(?:## |$)/);
    if (legacyMatch) {
      const legacyProjects = legacyMatch[1].match(/- \*\*Directory\*\*: `([^`]+)`/g);
      if (legacyProjects) {
        legacyProjects.forEach(match => {
          const dir = match.match(/`([^`]+)`/)[1];
          projects.push({ dir, status: 'LEGACY' });
        });
      }
    }

    return projects;
  }

  validate() {
    console.log(' ENHANCED IMPORT VALIDATION');
    console.log('='.repeat(60));
    console.log(`Workspace: ${this.workspaceRoot}\n`);

    // Validate each active project
    for (const project of this.projects) {
      if (project.status === 'ACTIVE') {
        this.validateProject(project);
      }
    }

    this.reportResults();
    return this.issues.length === 0 ? 0 : 1;
  }

  validateProject(project) {
    const projectPath = path.join(this.workspaceRoot, project.dir);
    if (!fs.existsSync(projectPath)) return;

    console.log(`Validating imports in ${project.dir}...`);

    // Check source files
    const srcPath = path.join(projectPath, 'src');
    if (fs.existsSync(srcPath)) {
      this.checkImports(srcPath, project);
    }

    // Check test files
    const testPath = path.join(projectPath, 'tests');
    if (fs.existsSync(testPath)) {
      this.checkImports(testPath, project);
    }

    // Check package.json dependencies
    const packageJsonPath = path.join(projectPath, 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      this.checkDependencies(packageJsonPath, project);
    }
  }

  checkImports(dir, project) {
    const files = this.getAllFiles(dir, ['.js', '.ts', '.jsx', '.tsx']);

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');
      const relativePath = path.relative(this.workspaceRoot, file);

      // Check static imports
      this.checkStaticImports(content, relativePath, project);

      // Check dynamic imports
      this.checkDynamicImports(content, relativePath, project);

      // Check require statements
      this.checkRequireStatements(content, relativePath, project);
    }
  }

  checkStaticImports(content, filePath, project) {
    // Match: import ... from '...' or import '...'
    const importRegex = /import\s+(?:.*\s+from\s+)?['"]([^'"]+)['"]/g;
    let match;

    while ((match = importRegex.exec(content)) !== null) {
      const importPath = match[1];
      this.validateImportPath(importPath, filePath, project, 'static import');
    }
  }

  checkDynamicImports(content, filePath, project) {
    // Match: import('...') or import(`...`)
    const dynamicRegex = /import\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
    let match;

    while ((match = dynamicRegex.exec(content)) !== null) {
      const importPath = match[1];
      this.validateImportPath(importPath, filePath, project, 'dynamic import');
    }
  }

  checkRequireStatements(content, filePath, project) {
    // Match: require('...') or require(`...`)
    const requireRegex = /require\s*\(\s*['"]([^'"]+)['"]\s*\)/g;
    let match;

    while ((match = requireRegex.exec(content)) !== null) {
      const importPath = match[1];
      this.validateImportPath(importPath, filePath, project, 'require');
    }
  }

  validateImportPath(importPath, filePath, project, importType) {
    // Skip node_modules and absolute paths
    if (importPath.startsWith('node_modules/') || 
        importPath.startsWith('/') ||
        !importPath.startsWith('.')) {
      return;
    }

    // Check if import crosses project boundaries
    const fileDir = path.dirname(filePath);
    const resolvedPath = path.resolve(this.workspaceRoot, fileDir, importPath);
    const relativeToWorkspace = path.relative(this.workspaceRoot, resolvedPath);

    // Check if import goes outside current project
    if (!relativeToWorkspace.startsWith(project.dir)) {
      // Check if it goes to another project
      for (const otherProject of this.projects) {
        if (otherProject.dir !== project.dir && 
            relativeToWorkspace.startsWith(otherProject.dir)) {
          
          if (otherProject.status === 'LEGACY') {
            this.issues.push({
              type: 'CRITICAL',
              message: ` BLEED DETECTED: ${filePath}`,
              details: `${importType} from legacy project: ${otherProject.dir}`,
              import: importPath,
              fix: `Remove import from ${otherProject.dir}. Use active project instead.`
            });
          } else {
            this.warnings.push({
              message: ` Cross-project import: ${filePath}`,
              details: `${importType} from ${otherProject.dir}`,
              import: importPath,
              note: 'Verify this is intentional and documented'
            });
          }
        }
      }
    }
  }

  checkDependencies(packageJsonPath, project) {
    try {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      const relativePath = path.relative(this.workspaceRoot, packageJsonPath);

      // Check repository URL
      if (packageJson.repository && packageJson.repository.url) {
        const repoUrl = packageJson.repository.url;
        // Check if repository URL references wrong project
        for (const otherProject of this.projects) {
          if (otherProject.dir !== project.dir && 
              repoUrl.includes(otherProject.dir.replace(/-/g, ''))) {
            this.warnings.push({
              message: ` Repository URL may reference wrong project: ${relativePath}`,
              details: `URL: ${repoUrl}`,
              note: 'Verify repository URL is correct'
            });
          }
        }
      }

      // Check dependencies for local file references
      const allDeps = {
        ...packageJson.dependencies,
        ...packageJson.devDependencies
      };

      for (const [depName, depVersion] of Object.entries(allDeps)) {
        if (typeof depVersion === 'string' && depVersion.startsWith('file:')) {
          const depPath = depVersion.replace('file:', '');
          const resolvedPath = path.resolve(path.dirname(packageJsonPath), depPath);
          const relativeToWorkspace = path.relative(this.workspaceRoot, resolvedPath);

          // Check if dependency points to another project
          for (const otherProject of this.projects) {
            if (otherProject.dir !== project.dir && 
                relativeToWorkspace.startsWith(otherProject.dir)) {
              this.warnings.push({
                message: ` Local dependency may cross project boundary: ${relativePath}`,
                details: `Dependency: ${depName} -> ${depPath}`,
                note: 'Verify this is intentional'
              });
            }
          }
        }
      }
    } catch (err) {
      this.warnings.push({
        message: `Could not parse package.json: ${packageJsonPath}`,
        details: err.message
      });
    }
  }

  getAllFiles(dir, extensions) {
    let results = [];
    if (!fs.existsSync(dir)) return results;

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

  reportResults() {
    console.log('\n IMPORT VALIDATION RESULTS');
    console.log('='.repeat(60));

    if (this.warnings.length > 0) {
      console.log(`\n  Warnings (${this.warnings.length}):`);
      this.warnings.forEach(w => {
        console.log(`\n  ${w.message}`);
        if (w.details) console.log(`  Details: ${w.details}`);
        if (w.note) console.log(`  Note: ${w.note}`);
      });
    }

    if (this.issues.length > 0) {
      console.log(`\n Critical Issues (${this.issues.length}):`);
      this.issues.forEach(issue => {
        console.log(`\n  ${issue.type}: ${issue.message}`);
        console.log(`  Details: ${issue.details}`);
        console.log(`  Import: ${issue.import}`);
        console.log(`  Fix: ${issue.fix}`);
      });
    }

    console.log('\n' + '='.repeat(60));
    console.log(' SUMMARY');
    console.log('='.repeat(60));
    console.log(`  Warnings: ${this.warnings.length}`);
    console.log(` Issues: ${this.issues.length}`);

    if (this.issues.length > 0) {
      console.log('\n CRITICAL: Import bleed detected! Fix issues above.');
    } else if (this.warnings.length > 0) {
      console.log('\n  Warnings present - review above.');
    } else {
      console.log('\n No import issues detected.');
    }

    console.log('='.repeat(60) + '\n');
  }
}

// Run validation if called directly
if (require.main === module) {
  const workspaceRoot = path.resolve(__dirname, '..');
  const validator = new EnhancedImportValidator(workspaceRoot);
  const exitCode = validator.validate();
  process.exit(exitCode);
}

module.exports = EnhancedImportValidator;

