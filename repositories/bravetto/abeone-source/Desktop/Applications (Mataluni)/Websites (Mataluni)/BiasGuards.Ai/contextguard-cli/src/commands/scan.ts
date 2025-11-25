/**
 * ContextGuard Scan Command
 * Comprehensive project scanning with BiasGuard
 */

import { glob } from 'glob';
import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';
import { BiasGuardValidator, ValidationResult } from '../core/validator.js';

interface ScanOptions {
  path?: string;
  framework?: string;
  fix?: boolean;
  report?: boolean;
}

interface ScanResults {
  totalFiles: number;
  totalIssues: number;
  averageScore: number;
  frameworkContamination: number;
  missionCompliant: boolean;
  topIssues: string[];
  fileResults: Array<{
    file: string;
    result: ValidationResult;
  }>;
}

const FILE_PATTERNS = [
  '**/*.{js,ts,jsx,tsx,vue,svelte}',
  '**/*.{html,css,scss,sass,less}',
  '**/*.{json,md,yml,yaml}'
];

const IGNORE_PATTERNS = [
  'node_modules/**',
  'dist/**',
  'build/**',
  '.git/**',
  'coverage/**',
  '**/*.min.js',
  '**/*.bundle.js'
];

export async function scanProject(options: ScanOptions): Promise<ScanResults> {
  const scanPath = options.path || '.';
  const configPath = path.join(scanPath, '.biasguard.json');
  
  // Load configuration
  let config: any = {};
  if (await fs.pathExists(configPath)) {
    config = await fs.readJson(configPath);
  }
  
  const targetFramework = options.framework || config.framework;
  
  // Find files to scan
  const files: string[] = [];
  
  for (const pattern of FILE_PATTERNS) {
    const matches = await glob(pattern, {
      cwd: scanPath,
      ignore: IGNORE_PATTERNS,
      absolute: true
    });
    files.push(...matches);
  }
  
  // Remove duplicates
  const uniqueFiles = [...new Set(files)];
  
  console.log(chalk.cyan(`\n Scanning ${uniqueFiles.length} files...`));
  
  // Scan each file
  const fileResults: Array<{ file: string; result: ValidationResult }> = [];
  let totalIssues = 0;
  let totalScore = 0;
  let frameworkContamination = 0;
  let missionCompliantFiles = 0;
  const allIssues: string[] = [];
  
  for (const file of uniqueFiles) {
    try {
      const content = await fs.readFile(file, 'utf-8');
      const result = BiasGuardValidator.validateFile(file, content, targetFramework);
      
      fileResults.push({ file: path.relative(scanPath, file), result });
      
      totalIssues += result.issues.length;
      totalScore += result.score;
      
      if (result.issues.some(issue => issue.includes('contamination'))) {
        frameworkContamination++;
      }
      
      if (result.missionCompliant !== false) {
        missionCompliantFiles++;
      }
      
      allIssues.push(...result.issues);
      
    } catch (error) {
      // Skip files that can't be read
      console.log(chalk.yellow(`  Skipping ${file}: ${error}`));
    }
  }
  
  const averageScore = uniqueFiles.length > 0 ? Math.round(totalScore / uniqueFiles.length) : 0;
  const missionCompliant = missionCompliantFiles === uniqueFiles.length;
  
  // Count issue frequency for top issues
  const issueCount: Record<string, number> = {};
  allIssues.forEach(issue => {
    const key = issue.replace(/^[]\s*/, ''); // Remove emoji prefix
    issueCount[key] = (issueCount[key] || 0) + 1;
  });
  
  const topIssues = Object.entries(issueCount)
    .sort(([,a], [,b]) => b - a)
    .map(([issue, count]) => `${issue} (${count} files)`)
    .slice(0, 10);
  
  const results: ScanResults = {
    totalFiles: uniqueFiles.length,
    totalIssues,
    averageScore,
    frameworkContamination,
    missionCompliant,
    topIssues,
    fileResults
  };
  
  // Auto-fix if requested
  if (options.fix) {
    await autoFixIssues(fileResults, scanPath);
  }
  
  // Generate report if requested
  if (options.report) {
    await generateReport(results, scanPath, config);
  }
  
  // Update config with scan results
  if (await fs.pathExists(configPath)) {
    config.lastScan = new Date().toISOString();
    config.lastScanResults = {
      totalFiles: results.totalFiles,
      totalIssues: results.totalIssues,
      averageScore: results.averageScore,
      missionCompliant: results.missionCompliant
    };
    await fs.writeJson(configPath, config, { spaces: 2 });
  }
  
  return results;
}

async function autoFixIssues(
  fileResults: Array<{ file: string; result: ValidationResult }>,
  basePath: string
): Promise<void> {
  console.log(chalk.cyan('\n Auto-fixing issues...'));
  
  let fixedFiles = 0;
  
  for (const { file, result } of fileResults) {
    if (result.issues.length === 0) continue;
    
    const filePath = path.join(basePath, file);
    let content = await fs.readFile(filePath, 'utf-8');
    let modified = false;
    
    // Simple auto-fixes
    const fixes = [
      // Fix common JAHmere Webb fact errors
      { from: 'July 28, 2025', to: 'August 25, 2025' },
      { from: '$25,000', to: '$26,500' },
      { from: '$27,000', to: '$26,500' },
      { from: '10%', to: '15%' },
      { from: '20%', to: '15%' },
      
      // Fix common Svelte 5 patterns
      { from: 'on:click=', to: 'onclick=' },
      { from: 'on:input=', to: 'oninput=' },
    ];
    
    for (const fix of fixes) {
      if (content.includes(fix.from)) {
        content = content.replace(new RegExp(fix.from, 'g'), fix.to);
        modified = true;
      }
    }
    
    if (modified) {
      await fs.writeFile(filePath, content);
      fixedFiles++;
      console.log(chalk.green(` Fixed: ${file}`));
    }
  }
  
  console.log(chalk.green(` Auto-fixed ${fixedFiles} files`));
}

async function generateReport(
  results: ScanResults,
  basePath: string,
  config: any
): Promise<void> {
  const reportPath = path.join(basePath, 'biasguard-report.json');
  
  const report = {
    generatedAt: new Date().toISOString(),
    projectConfig: config,
    summary: {
      totalFiles: results.totalFiles,
      totalIssues: results.totalIssues,
      averageScore: results.averageScore,
      frameworkContamination: results.frameworkContamination,
      missionCompliant: results.missionCompliant
    },
    topIssues: results.topIssues,
    fileResults: results.fileResults.map(({ file, result }) => ({
      file,
      score: result.score,
      valid: result.valid,
      issues: result.issues,
      framework: result.framework,
      missionCompliant: result.missionCompliant
    })),
    jahmereWebbMission: {
      courtDate: 'August 25, 2025',
      crisisAmount: '$26,500',
      revenueToJustice: '15%',
      missionStatus: results.missionCompliant ? 'COMPLIANT' : 'NEEDS_ATTENTION'
    }
  };
  
  await fs.writeJson(reportPath, report, { spaces: 2 });
  
  console.log(chalk.green(` Report generated: ${reportPath}`));
}
