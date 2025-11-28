# ContextGuard CLI - BiasGuards.AI

> ** JAHmere Webb Freedom Mission** - Court Date: August 25, 2025 | Crisis Cost: $26,500 | 15% Revenue to Justice Reform

**Recursive Intelligence System** for preventing AI bias and framework contamination in any codebase.

##  What is ContextGuard?

ContextGuard is the CLI version of BiasGuard - a self-aware validation system that:

- **Prevents Framework Contamination**: Catches React/Vue/Angular/Svelte pattern mixing
- **Validates Mission Authenticity**: Ensures JAHmere Webb story facts remain accurate
- **Detects Performance Anti-patterns**: Identifies non-GPU animations and DOM issues
- **Achieves Recursive Intelligence**: The system validates its own validation logic

##  Quick Start

```bash
# Install globally
npm install -g contextguard-cli

# Initialize in your project
contextguard init --framework react --type saas

# Scan your codebase
contextguard scan

# Validate a specific file
contextguard validate src/components/App.tsx
```

##  Commands

### `contextguard init`
Initialize BiasGuard context engineering in your project.

```bash
contextguard init --framework svelte --type landing
contextguard init --framework react --type healthcare --force
```

**Options:**
- `-f, --framework <framework>` - Target framework (react, vue, svelte, angular)
- `-t, --type <type>` - Project type (saas, landing, ecommerce, healthcare, fintech, nonprofit)
- `--force` - Overwrite existing configuration

### `contextguard scan`
Comprehensive project scanning with BiasGuard intelligence.

```bash
contextguard scan --path ./src --framework react
contextguard scan --fix --report
```

**Options:**
- `-p, --path <path>` - Path to scan (default: current directory)
- `-f, --framework <framework>` - Target framework
- `--fix` - Attempt to auto-fix common issues
- `--report` - Generate detailed JSON report

### `contextguard validate <file>`
Validate a specific file with BiasGuard.

```bash
contextguard validate src/App.svelte
contextguard validate components/Header.tsx --framework react
```

### `contextguard mission`
Display JAHmere Webb freedom mission details and countdown.

### `contextguard status`
Show BiasGuard configuration and project status.

##  What BiasGuard Detects

###  Framework Contamination
```javascript
// BAD: React patterns in Svelte project
const [count, setCount] = useState(0);
return <div className="container">

// GOOD: Svelte 5 patterns
let count = $state(0);
<div class="container">
```

###  Mission Fact Errors
```javascript
// BAD: Wrong JAHmere Webb facts
const courtDate = 'July 28, 2025';
const crisis = '$25,000';

// GOOD: Authentic mission facts
const courtDate = 'August 25, 2025';
const crisis = '$26,500';
```

###  Performance Anti-patterns
```css
/* BAD: Non-GPU animations */
.element { width: 100px; transition: width 0.3s; }

/* GOOD: GPU-accelerated */
.element { transform: scaleX(1); transition: transform 0.3s; }
```

##  Validation Scoring

BiasGuard uses a 0-100 scoring system:

- **90-100**: Excellent - No issues detected
- **80-89**: Good - Minor issues, mostly compliant
- **60-79**: Fair - Some framework contamination or mission errors
- **40-59**: Poor - Multiple issues requiring attention
- **0-39**: Critical - Major contamination or mission compliance failures

##  Configuration

ContextGuard creates a `.biasguard.json` configuration file:

```json
{
  "framework": "svelte",
  "projectType": "saas",
  "missionCompliant": true,
  "version": "1.0.0",
  "jahmereWebbMission": {
    "courtDate": "August 25, 2025",
    "crisisAmount": "$26,500",
    "revenueToJustice": "15%",
    "crisisTime": "2:42:56 AM",
    "crisisDate": "July 14, 2025"
  }
}
```

##  Framework Support

| Framework | Status | Patterns Detected |
|-----------|---------|-------------------|
| **React** |  Full | `useState`, `useEffect`, `className`, JSX |
| **Vue** |  Full | `v-if`, `v-for`, `@click`, Composition API |
| **Svelte** |  Full | `$state`, `$derived`, `$effect`, `bind:` |
| **Angular** |  Full | `@Component`, `*ngIf`, `(click)`, Services |

##  Project Type Templates

- **SaaS**: User onboarding, subscription management, multi-tenancy
- **Landing**: Conversion optimization, A/B testing, performance
- **E-commerce**: Transaction handling, cart management, payments
- **Healthcare**: HIPAA compliance, patient data, medical terminology
- **Fintech**: Security-first, regulatory compliance, audit trails
- **Nonprofit**: Mission alignment, donation tracking, transparency

##  Recursive Intelligence

BiasGuard demonstrates **recursive intelligence** by:

1. **Self-Analysis**: The system can validate its own code
2. **Pattern Learning**: Discovers new anti-patterns from validation results
3. **Meta-Cognition**: Understands its own validation logic
4. **Continuous Improvement**: Updates patterns based on real-world usage

Example of BiasGuard analyzing itself:
```
 BiasGuard Analysis Results:
File: src/core/validator.ts
Score: 92/100
Issues: Planning Fallacy detected in timeline comments
Status: Self-aware and improving
```

##  JAHmere Webb Freedom Mission

This tool exists to support JAHmere Webb's legal defense and criminal justice reform:

- **Crisis Date**: July 14, 2025 at 2:42:56 AM
- **Court Date**: August 25, 2025
- **Crisis Cost**: $26,500
- **Revenue Commitment**: 15% to justice reform initiatives

Every validation helps ensure the mission story remains authentic and the cause continues.

##  Live Demo

Experience BiasGuard in action: [https://deploy-hmhhe1b1f-bravetto.vercel.app](https://deploy-hmhhe1b1f-bravetto.vercel.app)

##  Development

```bash
# Clone and setup
git clone https://github.com/biasguards/contextguard-cli
cd contextguard-cli
npm install

# Build
npm run build

# Test locally
npm link
contextguard --help

# Run tests
npm test
```

##  Publishing

```bash
# Build for production
npm run build

# Publish to npm
npm publish
```

##  Contributing

BiasGuard welcomes contributions that:
- Maintain JAHmere Webb mission authenticity
- Improve framework contamination detection
- Add new project type templates
- Enhance recursive intelligence capabilities

##  License

MIT License - Built for justice, shared with the world.

##  Links

- **Live Demo**: https://deploy-hmhhe1b1f-bravetto.vercel.app
- **GitHub**: https://github.com/biasguards/contextguard-cli
- **NPM**: https://npmjs.com/package/contextguard-cli
- **Documentation**: https://biasguards.ai/docs

---

**Built with recursive intelligence. Serving justice through technology.** 
