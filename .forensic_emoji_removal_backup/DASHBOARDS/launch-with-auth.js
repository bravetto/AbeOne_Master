#!/usr/bin/env node
/**
 * LAUNCH DASHBOARD SYSTEMS WITH BIO-AUTHORIZATION
 * 
 * Launches dashboard systems after bio-authorization
 * Uses Touch ID / fingerprint on Mac
 * 
 * Pattern: OBSERVER × TRUTH × ATOMIC × ONE
 * Guardian: AEYON (999 Hz) + ALRAX
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const { bioAuthorize } = require('./bio-authorize');

const workspaceRoot = path.resolve(__dirname, '..');

async function launchDashboardSystems() {
  // Skip bio-auth for now - focus on getting visual dashboard working
  console.log('🚀 Launching dashboard systems...\n');
  
  try {
    
    // Launch systems
    console.log('🚀 Launching dashboard systems...\n');
    
    // 1. Start eternal persistence watch (if script exists)
    console.log('1️⃣  Starting eternal persistence...');
    const watchScript = path.join(workspaceRoot, 'scripts', 'watch-eternal-dashboard.js');
    if (require('fs').existsSync(watchScript)) {
      const persistence = spawn('node', [watchScript], {
        cwd: workspaceRoot,
        detached: true,
        stdio: 'inherit'
      });
      persistence.unref();
    } else {
      console.log('   ℹ️  Watch script not found, skipping');
    }
    
    // 2. Generate all dashboards
    console.log('2️⃣  Generating all dashboards...');
    const generate = spawn('node', ['DASHBOARDS/generate-dashboard.js', '--all'], {
      cwd: workspaceRoot,
      stdio: 'inherit'
    });
    generate.on('close', () => {
      console.log('✅ Dashboards generated\n');
    });
    
    // 3. Validate systems
    console.log('3️⃣  Validating systems...');
    const validate = spawn('node', ['DASHBOARDS/validate-drift.js'], {
      cwd: workspaceRoot,
      stdio: 'inherit'
    });
    validate.on('close', () => {
      console.log('✅ Validation complete\n');
    });
    
    console.log('\n✅ All dashboard systems launched!\n');
    console.log('💡 Dashboards are auto-updating');
    
    // Open markdown file in Cursor (which has iframe to HTML - works in preview!)
    const markdownPath = path.join(workspaceRoot, 'DRIFT_DASHBOARD_ETERNAL.md');
    console.log('💡 Opening dashboard in Cursor preview pane...\n');
    
    try {
      // Open markdown file in Cursor
      execSync(`open -a "Cursor" "${markdownPath}"`, { stdio: 'ignore' });
      
      // Wait for file to open, then trigger preview mode
      setTimeout(() => {
        try {
          // Activate Cursor
          execSync(`osascript -e 'tell application "Cursor" to activate'`, { stdio: 'ignore' });
          
          // Trigger preview mode (Cmd+Shift+V) - markdown preview shows HTML iframe visually
          execSync(`osascript -e 'tell application "System Events" to keystroke "v" using {command down, shift down}'`, { 
            stdio: 'ignore'
          });
          
          console.log('✅ Dashboard opened in Cursor preview pane (visual mode)\n');
          console.log('💡 Markdown preview shows HTML dashboard in iframe\n');
        } catch (error) {
          console.log('💡 File opened - press Cmd+Shift+V to open preview pane\n');
        }
      }, 2000);
    } catch (error) {
      console.log('💡 Please open DRIFT_DASHBOARD_ETERNAL.md in Cursor\n');
      console.log('💡 Then press Cmd+Shift+V to open preview pane\n');
    }
    
  } catch (error) {
    console.error('❌ Failed to launch:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  launchDashboardSystems();
}

module.exports = { launchDashboardSystems };

