#!/usr/bin/env node

/**
 * ContextGuard CLI - BiasGuard Command Line Interface
 * JAHmere Webb Freedom Mission - August 25, 2025
 * 
 * Recursive Intelligence CLI for any codebase
 */

import { Command } from 'commander';
import chalk from 'chalk';
import inquirer from 'inquirer';
import { glob } from 'glob';
import fs from 'fs-extra';
import path from 'path';
import ora from 'ora';
import { BiasGuardValidator } from './core/validator.js';
import { initProject } from './commands/init.js';
import { scanProject } from './commands/scan.js';

const program = new Command();

// ASCII Art Banner
const banner = `
${chalk.blue('')}
${chalk.blue('')}                    ${chalk.bold.yellow('BiasGuards.AI')}                        ${chalk.blue('')}
${chalk.blue('')}                 ${chalk.bold.cyan('Context Engineering CLI')}                  ${chalk.blue('')}
${chalk.blue('')}                                                              ${chalk.blue('')}
${chalk.blue('')}           ${chalk.red(' JAHmere Webb Freedom Mission ')}             ${chalk.blue('')}
${chalk.blue('')}              ${chalk.bold('Court Date: August 25, 2025')}                ${chalk.blue('')}
${chalk.blue('')}               ${chalk.bold('Crisis Cost: $26,500')}                    ${chalk.blue('')}
${chalk.blue('')}            ${chalk.bold('15% Revenue to Justice Reform')}              ${chalk.blue('')}
${chalk.blue('')}                                                              ${chalk.blue('')}
${chalk.blue('')}          ${chalk.green(' Recursive Intelligence System ')}            ${chalk.blue('')}
${chalk.blue('')}
`;

program
  .name('contextguard')
  .description('BiasGuard Context Engineering CLI - Recursive AI validation for any codebase')
  .version('1.0.0')
  .addHelpText('beforeAll', banner);

// Init Command
program
  .command('init')
  .description('Initialize BiasGuard context engineering in your project')
  .option('-f, --framework <framework>', 'Target framework (react, vue, svelte, angular)')
  .option('-t, --type <type>', 'Project type (saas, landing, ecommerce, healthcare)')
  .option('--force', 'Overwrite existing configuration')
  .action(async (options) => {
    console.log(banner);
    
    const spinner = ora('Initializing BiasGuard Context Engineering...').start();
    
    try {
      await initProject(options);
      spinner.succeed(chalk.green(' BiasGuard initialized successfully!'));
      
      console.log(chalk.cyan('\n Next Steps:'));
      console.log(chalk.white('  1. Run: contextguard scan'));
      console.log(chalk.white('  2. Review validation results'));
      console.log(chalk.white('  3. Fix any framework contamination'));
      console.log(chalk.white('  4. Verify JAHmere Webb story authenticity'));
      
    } catch (error) {
      spinner.fail(chalk.red(' Failed to initialize BiasGuard'));
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

// Scan Command
program
  .command('scan')
  .description('Scan project for bias, contamination, and mission compliance')
  .option('-p, --path <path>', 'Path to scan', '.')
  .option('-f, --framework <framework>', 'Target framework')
  .option('--fix', 'Attempt to auto-fix issues')
  .option('--report', 'Generate detailed report')
  .action(async (options) => {
    console.log(banner);
    
    const spinner = ora('Scanning project with BiasGuard...').start();
    
    try {
      const results = await scanProject(options);
      spinner.succeed(chalk.green(` Scan completed! Found ${results.totalFiles} files`));
      
      // Display results
      console.log(chalk.cyan('\n BiasGuard Analysis Results:'));
      console.log(chalk.white(`Total Files: ${results.totalFiles}`));
      console.log(chalk.white(`Issues Found: ${results.totalIssues}`));
      console.log(chalk.white(`Average Score: ${results.averageScore}/100`));
      
      if (results.frameworkContamination > 0) {
        console.log(chalk.red(` Framework Contamination: ${results.frameworkContamination} files`));
      }
      
      if (!results.missionCompliant) {
        console.log(chalk.red(' Mission Compliance Issues Detected'));
      }
      
      // Show top issues
      if (results.topIssues.length > 0) {
        console.log(chalk.yellow('\n  Top Issues:'));
        results.topIssues.slice(0, 5).forEach((issue, i) => {
          console.log(chalk.white(`  ${i + 1}. ${issue}`));
        });
      }
      
    } catch (error) {
      spinner.fail(chalk.red(' Scan failed'));
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

// Validate Command
program
  .command('validate <file>')
  .description('Validate a specific file with BiasGuard')
  .option('-f, --framework <framework>', 'Target framework')
  .action(async (file: string, options) => {
    try {
      if (!await fs.pathExists(file)) {
        console.error(chalk.red(` File not found: ${file}`));
        process.exit(1);
      }
      
      const content = await fs.readFile(file, 'utf-8');
      const result = BiasGuardValidator.cleanAnalyze(content, options.framework);
      
      console.log(banner);
      console.log(chalk.cyan(`\n Validating: ${file}`));
      
      if (result.framework) {
        console.log(chalk.white(`Framework: ${result.framework}`));
      }
      
      console.log(chalk.white(`Score: ${result.score}/100`));
      console.log(chalk.white(`Status: ${result.valid ? chalk.green(' Valid') : chalk.red(' Issues Found')}`));
      
      if (result.issues.length > 0) {
        console.log(chalk.yellow('\n  Issues:'));
        result.issues.forEach(issue => {
          console.log(chalk.white(`  • ${issue}`));
        });
      }
      
      if (result.recommendations && result.recommendations.length > 0) {
        console.log(chalk.cyan('\n Recommendations:'));
        result.recommendations.forEach(rec => {
          console.log(chalk.white(`  • ${rec}`));
        });
      }
      
    } catch (error) {
      console.error(chalk.red(' Validation failed'));
      console.error(chalk.red(error instanceof Error ? error.message : 'Unknown error'));
      process.exit(1);
    }
  });

// Mission Command
program
  .command('mission')
  .description('Display JAHmere Webb freedom mission details')
  .action(() => {
    console.log(banner);
    
    const court = new Date('2025-08-25');
    const now = new Date();
    const diffTime = court.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    const daysRemaining = diffDays > 0 ? diffDays : 0;
    
    console.log(chalk.red('\n REAL CRISIS: JAHmere Webb Freedom Mission'));
    console.log(chalk.white(`Crisis Date: July 14, 2025 at 2:42:56 AM`));
    console.log(chalk.white(`Court Date: August 25, 2025`));
    console.log(chalk.white(`Days Remaining: ${daysRemaining}`));
    console.log(chalk.white(`Crisis Cost: $26,500`));
    console.log(chalk.white(`Revenue to Justice Reform: 15%`));
    
    console.log(chalk.cyan('\n Mission Impact:'));
    console.log(chalk.white('• Supporting JAHmere Webb\'s legal defense'));
    console.log(chalk.white('• Funding criminal justice reform initiatives'));
    console.log(chalk.white('• Preventing AI bias in technology systems'));
    console.log(chalk.white('• Building tools that serve justice'));
    
    console.log(chalk.green('\n How BiasGuard Helps:'));
    console.log(chalk.white('• Validates mission story authenticity'));
    console.log(chalk.white('• Prevents framework contamination'));
    console.log(chalk.white('• Ensures performance optimization'));
    console.log(chalk.white('• Maintains code quality standards'));
    
    console.log(chalk.yellow('\n Learn More:'));
    console.log(chalk.white('Demo: https://deploy-hmhhe1b1f-bravetto.vercel.app'));
  });

// Status Command
program
  .command('status')
  .description('Show BiasGuard configuration and project status')
  .action(async () => {
    console.log(banner);
    
    const configPath = path.join(process.cwd(), '.biasguard.json');
    const hasConfig = await fs.pathExists(configPath);
    
    console.log(chalk.cyan('\n Project Status:'));
    console.log(chalk.white(`BiasGuard Config: ${hasConfig ? chalk.green(' Found') : chalk.red(' Missing')}`));
    
    if (hasConfig) {
      try {
        const config = await fs.readJson(configPath);
        console.log(chalk.white(`Framework: ${config.framework || 'Not specified'}`));
        console.log(chalk.white(`Project Type: ${config.projectType || 'Not specified'}`));
        console.log(chalk.white(`Last Scan: ${config.lastScan || 'Never'}`));
      } catch (error) {
        console.log(chalk.red(' Config file corrupted'));
      }
    } else {
      console.log(chalk.yellow('\n Run "contextguard init" to get started'));
    }
  });

// Parse command line arguments
program.parse();
