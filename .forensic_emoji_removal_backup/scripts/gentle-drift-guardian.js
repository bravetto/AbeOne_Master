#!/usr/bin/env node
/**
 * GENTLE DRIFT GUARDIAN
 * 
 * Always-on, non-blocking drift protection
 * Runs on every chat interaction - informative, helpful, fun
 * Makes work better by guiding, not blocking
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + Abë (530 Hz) - Gentle & Helpful
 */

const fs = require('fs');
const path = require('path');

class GentleDriftGuardian {
  constructor() {
    this.workspaceRoot = this.findWorkspaceRoot();
    this.currentDir = process.cwd();
    this.messages = [];
    this.helpfulTips = [];
  }

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
      if (parent === current) break;
      current = parent;
      depth++;
    }

    return process.cwd();
  }

  check() {
    // Quick, lightweight checks - non-blocking
    this.checkCurrentDirectory();
    this.checkProjectStatus();
    this.generateHelpfulTips();

    return {
      status: this.messages.length === 0 ? 'ok' : 'info',
      messages: this.messages,
      tips: this.helpfulTips,
      currentProject: this.getCurrentProject()
    };
  }

  checkCurrentDirectory() {
    const statusPath = path.join(this.currentDir, 'PROJECT_STATUS.md');
    const boundaryPath = path.join(this.currentDir, '.project-boundary');

    // Check if we're in a project directory
    if (!fs.existsSync(statusPath) && !fs.existsSync(boundaryPath)) {
      // Not in a project directory - that's OK, just inform
      if (fs.existsSync(path.join(this.workspaceRoot, 'PROJECT_MASTER_INDEX.md'))) {
        this.messages.push({
          type: 'info',
          emoji: '📁',
          message: 'Working in workspace root',
          tip: 'Navigate to a project directory for project-specific context'
        });
      }
      return;
    }

    // Read status if available
    if (fs.existsSync(statusPath)) {
      const statusContent = fs.readFileSync(statusPath, 'utf8');
      
      // Quick status check - check for ACTIVE first, then LEGACY
      if (statusContent.includes('**Status**: ✅ **ACTIVE') || 
          statusContent.includes('Status**: ✅ **ACTIVE') ||
          statusContent.match(/Status[:\s*]+✅[:\s*]+ACTIVE/i)) {
        this.messages.push({
          type: 'success',
          emoji: '✨',
          message: 'You\'re in an active project!',
          tip: 'Perfect place to work'
        });
      } else if (statusContent.includes('**Status**: ⚠️ **LEGACY') ||
                 statusContent.includes('Status**: ⚠️ **LEGACY') ||
                 statusContent.match(/Status[:\s*]+⚠️[:\s*]+LEGACY/i)) {
        this.messages.push({
          type: 'gentle-warning',
          emoji: '💡',
          message: 'You\'re in a legacy directory',
          tip: this.findActiveDirectory(statusContent),
          action: 'Consider switching to the active directory for current work'
        });
      }
    }
  }

  checkProjectStatus() {
    const boundaryPath = path.join(this.currentDir, '.project-boundary');
    
    if (fs.existsSync(boundaryPath)) {
      try {
        const boundary = JSON.parse(fs.readFileSync(boundaryPath, 'utf8'));
        
        if (boundary.status === 'ACTIVE') {
          // All good - maybe add a helpful tip
          if (boundary.relatedProjects && boundary.relatedProjects.length > 0) {
            this.helpfulTips.push({
              emoji: '🔗',
              tip: `Related projects: ${boundary.relatedProjects.join(', ')}`
            });
          }
        }
      } catch (err) {
        // Silent fail - don't block
      }
    }
  }

  findActiveDirectory(statusContent) {
    const activeMatch = statusContent.match(/- \*\*Active Directory\*\*: `([^`]+)`/);
    if (activeMatch) {
      return `Active directory: ${activeMatch[1]}`;
    }
    return 'Check PROJECT_MASTER_INDEX.md for active directory';
  }

  getCurrentProject() {
    const projectName = path.basename(this.currentDir);
    const boundaryPath = path.join(this.currentDir, '.project-boundary');
    
    if (fs.existsSync(boundaryPath)) {
      try {
        const boundary = JSON.parse(fs.readFileSync(boundaryPath, 'utf8'));
        return {
          name: boundary.projectName || projectName,
          status: boundary.status || 'unknown',
          version: boundary.version || 'unknown'
        };
      } catch (err) {
        // Silent fail
      }
    }

    return {
      name: projectName,
      status: 'unknown',
      version: 'unknown'
    };
  }

  generateHelpfulTips() {
    // Add helpful, fun tips that make work easier
    const tips = [
      {
        emoji: '🎯',
        tip: 'Run `node scripts/validate-project-boundaries.js` anytime to check boundaries'
      },
      {
        emoji: '📚',
        tip: 'Check PROJECT_STATUS.md in any directory for project context'
      },
      {
        emoji: '🔍',
        tip: 'Use `node scripts/enhanced-import-validator.js` to check imports'
      }
    ];

    // Add tips based on current context
    const project = this.getCurrentProject();
    if (project.status === 'ACTIVE') {
      tips.push({
        emoji: '🚀',
        tip: `Working in ${project.name} - active project, perfect for development!`
      });
    }

    this.helpfulTips.push(...tips);
  }

  formatOutput() {
    const result = this.check();
    
    if ((!result.messages || result.messages.length === 0) && 
        (!result.helpfulTips || result.helpfulTips.length === 0)) {
      return '✨ All good! Happy coding!';
    }

    let output = '\n🛡️  Gentle Drift Guardian\n';
    output += '='.repeat(50) + '\n\n';

    // Show current project info
    if (result.currentProject) {
      output += `📦 Current Project: ${result.currentProject.name}\n`;
      output += `   Status: ${result.currentProject.status}\n`;
      if (result.currentProject.version && result.currentProject.version !== 'unknown') {
        output += `   Version: ${result.currentProject.version}\n`;
      }
      output += '\n';
    }

    // Show messages (informative, not blocking)
    if (result.messages && result.messages.length > 0) {
      result.messages.forEach(msg => {
        output += `${msg.emoji || '💡'} ${msg.message}\n`;
        if (msg.tip) {
          output += `   💡 ${msg.tip}\n`;
        }
        if (msg.action) {
          output += `   ✨ ${msg.action}\n`;
        }
        output += '\n';
      });
    }

    // Show helpful tips
    if (result.helpfulTips && result.helpfulTips.length > 0) {
      output += '💡 Helpful Tips:\n';
      result.helpfulTips.forEach(tip => {
        output += `   ${tip.emoji || '💡'} ${tip.tip}\n`;
      });
      output += '\n';
    }

    output += '='.repeat(50) + '\n';
    output += '✨ Keep coding! This is just friendly guidance.\n\n';

    return output;
  }
}

// Run if called directly
if (require.main === module) {
  const guardian = new GentleDriftGuardian();
  console.log(guardian.formatOutput());
}

module.exports = GentleDriftGuardian;

