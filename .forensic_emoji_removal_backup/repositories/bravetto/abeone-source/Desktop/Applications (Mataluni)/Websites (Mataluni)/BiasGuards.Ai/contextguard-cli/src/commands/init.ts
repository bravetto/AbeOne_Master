/**
 * ContextGuard Init Command
 * Initialize BiasGuard context engineering in any project
 */

import inquirer from 'inquirer';
import fs from 'fs-extra';
import path from 'path';
import chalk from 'chalk';

interface InitOptions {
  framework?: string;
  type?: string;
  force?: boolean;
}

interface ProjectConfig {
  framework: string;
  projectType: string;
  missionCompliant: boolean;
  createdAt: string;
  version: string;
  jahmereWebbMission: {
    courtDate: string;
    crisisAmount: string;
    revenueToJustice: string;
    crisisTime: string;
    crisisDate: string;
  };
}

const FRAMEWORK_TEMPLATES = {
  react: {
    name: 'React',
    description: 'React with TypeScript, hooks, and modern patterns',
    devDependencies: ['@types/react', '@types/react-dom'],
    eslintRules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn'
    }
  },
  vue: {
    name: 'Vue',
    description: 'Vue 3 with Composition API and TypeScript',
    devDependencies: ['@vue/typescript'],
    eslintRules: {
      'vue/multi-word-component-names': 'error'
    }
  },
  svelte: {
    name: 'Svelte',
    description: 'Svelte 5 with Runes API and SvelteKit',
    devDependencies: ['@sveltejs/adapter-auto'],
    eslintRules: {
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }]
    }
  },
  angular: {
    name: 'Angular',
    description: 'Angular with TypeScript and strict mode',
    devDependencies: ['@angular/cli'],
    eslintRules: {
      '@angular-eslint/directive-selector': 'error'
    }
  }
};

const PROJECT_TYPES = {
  saas: 'SaaS Application',
  landing: 'Landing Page',
  ecommerce: 'E-commerce Site',
  healthcare: 'Healthcare Platform',
  fintech: 'Financial Technology',
  nonprofit: 'Non-profit Organization'
};

export async function initProject(options: InitOptions): Promise<void> {
  const configPath = path.join(process.cwd(), '.biasguard.json');
  const packagePath = path.join(process.cwd(), 'package.json');
  
  // Check if already initialized
  if (await fs.pathExists(configPath) && !options.force) {
    const { overwrite } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'overwrite',
        message: 'BiasGuard is already initialized. Overwrite configuration?',
        default: false
      }
    ]);
    
    if (!overwrite) {
      console.log(chalk.yellow('🔄 Initialization cancelled'));
      return;
    }
  }
  
  // Interactive setup if options not provided
  let framework = options.framework;
  let projectType = options.type;
  
  if (!framework) {
    const frameworkChoice = await inquirer.prompt([
      {
        type: 'list',
        name: 'framework',
        message: 'What framework are you using?',
        choices: Object.entries(FRAMEWORK_TEMPLATES).map(([key, config]) => ({
          name: `${config.name} - ${config.description}`,
          value: key
        }))
      }
    ]);
    framework = frameworkChoice.framework;
  }
  
  if (!projectType) {
    const typeChoice = await inquirer.prompt([
      {
        type: 'list',
        name: 'projectType',
        message: 'What type of project is this?',
        choices: Object.entries(PROJECT_TYPES).map(([key, name]) => ({
          name,
          value: key
        }))
      }
    ]);
    projectType = typeChoice.projectType;
  }
  
  // Create BiasGuard configuration
  const config: ProjectConfig = {
    framework: framework!,
    projectType: projectType!,
    missionCompliant: true,
    createdAt: new Date().toISOString(),
    version: '1.0.0',
    jahmereWebbMission: {
      courtDate: 'August 25, 2025',
      crisisAmount: '$26,500',
      revenueToJustice: '15%',
      crisisTime: '2:42:56 AM',
      crisisDate: 'July 14, 2025'
    }
  };
  
  await fs.writeJson(configPath, config, { spaces: 2 });
  
  // Create validation script template
  const validationScript = `/**
 * BiasGuard Validation Script
 * JAHmere Webb Freedom Mission - August 25, 2025
 * 
 * Auto-generated for ${FRAMEWORK_TEMPLATES[framework as keyof typeof FRAMEWORK_TEMPLATES].name} project
 */

import { BiasGuardValidator } from 'contextguard-cli';

export function validateCode(code: string) {
  return BiasGuardValidator.validate(code, '${framework}');
}

export function validateFile(filePath: string, content: string) {
  return BiasGuardValidator.validateFile(filePath, content, '${framework}');
}

// Mission-critical facts (DO NOT MODIFY)
export const JAHMERE_WEBB_FACTS = {
  courtDate: 'August 25, 2025',
  crisisAmount: '$26,500',
  revenueToJustice: '15%',
  crisisTime: '2:42:56 AM',
  crisisDate: 'July 14, 2025'
};
`;
  
  await fs.writeFile(
    path.join(process.cwd(), 'biasguard-validation.js'),
    validationScript
  );
  
  // Update package.json scripts if it exists
  if (await fs.pathExists(packagePath)) {
    try {
      const packageJson = await fs.readJson(packagePath);
      
      if (!packageJson.scripts) {
        packageJson.scripts = {};
      }
      
      packageJson.scripts['biasguard:scan'] = 'contextguard scan';
      packageJson.scripts['biasguard:validate'] = 'contextguard validate';
      
      // Add contextguard-cli as dev dependency
      if (!packageJson.devDependencies) {
        packageJson.devDependencies = {};
      }
      packageJson.devDependencies['contextguard-cli'] = '^1.0.0';
      
      await fs.writeJson(packagePath, packageJson, { spaces: 2 });
    } catch (error) {
      console.log(chalk.yellow('⚠️  Could not update package.json scripts'));
    }
  }
  
  // Create framework-specific templates
  await createFrameworkTemplates(framework!, projectType!);
  
  console.log(chalk.green('\n✅ BiasGuard Context Engineering Initialized!'));
  console.log(chalk.cyan('\n📁 Created Files:'));
  console.log(chalk.white('  • .biasguard.json - Configuration'));
  console.log(chalk.white('  • biasguard-validation.js - Validation utilities'));
  
  console.log(chalk.cyan('\n🎯 Mission Details:'));
  console.log(chalk.white('  • JAHmere Webb court date: August 25, 2025'));
  console.log(chalk.white('  • Crisis amount: $26,500'));
  console.log(chalk.white('  • Revenue to justice reform: 15%'));
}

async function createFrameworkTemplates(framework: string, projectType: string): Promise<void> {
  const templatesDir = path.join(process.cwd(), '.biasguard', 'templates');
  await fs.ensureDir(templatesDir);
  
  // Create framework-specific validation rules
  const rules = {
    [`${framework}-patterns.json`]: {
      goodPatterns: FRAMEWORK_TEMPLATES[framework as keyof typeof FRAMEWORK_TEMPLATES]?.devDependencies || [],
      badPatterns: Object.keys(FRAMEWORK_TEMPLATES)
        .filter(f => f !== framework)
        .map(f => FRAMEWORK_TEMPLATES[f as keyof typeof FRAMEWORK_TEMPLATES].name),
      eslintRules: FRAMEWORK_TEMPLATES[framework as keyof typeof FRAMEWORK_TEMPLATES]?.eslintRules || {}
    },
    
    [`${projectType}-context.json`]: {
      projectType,
      missionAlignment: true,
      performanceTargets: {
        lighthouse: 98,
        accessibility: 100,
        seo: 95
      },
      businessMetrics: {
        conversionRate: 'TBD',
        userRetention: 'TBD',
        revenueToJustice: '15%'
      }
    }
  };
  
  for (const [filename, content] of Object.entries(rules)) {
    await fs.writeJson(path.join(templatesDir, filename), content, { spaces: 2 });
  }
}
