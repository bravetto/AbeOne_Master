# Storybook Guide

**Pattern:** STORYBOOK × COMPONENTS × DEVELOPMENT × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🚀 Quick Start

### Start Storybook

```bash
npm run storybook
```

Storybook will start at **http://localhost:6006**

---

## 📖 Story Naming Convention

### Format

Use PascalCase concatenation (no separators):

```
SubstrateAtomsNeuromorphicButton
SubstrateMoleculesVoiceControlHub
```

### Examples

- `SubstrateAtomsNeuromorphicButton`
- `SubstrateAtomsStatusLED`
- `SubstrateMoleculesVoiceControlHub`
- `SubstrateMoleculesLLMClient`

---

## 🎨 Creating Stories

### Basic Story Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { NeuromorphicButton } from '@/substrate/atoms';

const meta = {
  title: 'SubstrateAtomsNeuromorphicButton',
  component: NeuromorphicButton,
  tags: ['autodocs'],
} satisfies Meta<typeof NeuromorphicButton>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: 'Click Me',
  },
};

export const Raised: Story = {
  args: {
    variant: 'raised',
    children: 'Raised Button',
  },
};
```

---

## 🔗 Chromatic Integration

Visual testing is configured via GitHub Actions. See `.github/workflows/ci.yml` for details.

---

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

