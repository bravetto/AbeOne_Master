# ∞ AbëONE Storybook Story Naming Convention ∞

**Pattern:** STORY × NAMING × ATOMIC × DESIGN × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Guardians:** AEYON (999 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 NAMING CONVENTION

### Format: `CategoryComponentName` (PascalCase concatenation)

**Note:** Storybook UI only allows letters (alphanumeric), so use PascalCase concatenation without separators.

**Structure:**
```
Category = Substrate Level (Atoms | Molecules | Organisms)
Component Name = Exact component name
Format = PascalCase concatenation (no separators)
```

---

## 📋 EXAMPLES

### Atoms

```typescript
// ✅ CORRECT (PascalCase concatenation - works in Storybook UI)
export default {
  title: 'SubstrateAtomsNeuromorphicButton',
  component: NeuromorphicButton,
};

// ✅ CORRECT (with category grouping)
export default {
  title: 'SubstrateAtomsInteractiveNeuromorphicButton',
  component: NeuromorphicButton,
};

// ✅ CORRECT (with subcategory)
export default {
  title: 'SubstrateAtomsFeedbackStatusLED',
  component: StatusLED,
};
```

### Molecules

```typescript
// ✅ CORRECT (PascalCase concatenation - works in Storybook UI)
export default {
  title: 'SubstrateMoleculesVoiceControlHub',
  component: VoiceControlHub,
};

// ✅ CORRECT (with category grouping)
export default {
  title: 'SubstrateMoleculesVoiceInterfaceVoiceControlHub',
  component: VoiceControlHub,
};
```

### Organisms (Future)

```typescript
// ✅ CORRECT
export default {
  title: 'Substrate/Organisms/HomeInterface',
  component: HomeInterface,
};
```

---

## 🎨 RECOMMENDED STRUCTURE

### Option 1: Simple (Recommended for Start)

```
Substrate/
├── Atoms/
│   ├── NeuromorphicButton
│   ├── StatusLED
│   ├── VoiceWaveform
│   └── SpeechSynthesis
├── Molecules/
│   ├── VoiceControlHub
│   ├── LLMClient
│   └── DimensionPortal
└── Organisms/ (future)
```

### Option 2: Categorized (Better Organization)

```
Substrate/
├── Atoms/
│   ├── Interactive/
│   │   ├── NeuromorphicButton
│   │   └── TranscendentButton
│   ├── Feedback/
│   │   ├── StatusLED
│   │   └── VoiceWaveform
│   ├── Event System/
│   │   ├── EventEmitter
│   │   └── EventBridge
│   └── Speech/
│       ├── SpeechSynthesis
│       └── SpeechRecognition
├── Molecules/
│   ├── Voice Interface/
│   │   └── VoiceControlHub
│   └── API Integration/
│       └── LLMClient
└── Organisms/ (future)
```

---

## 📝 STORY NAMING PATTERNS

### Story Names (within component)

```typescript
// ✅ CORRECT - Use descriptive names
export const Default = { ... };
export const Raised = { ... };
export const Pressed = { ... };
export const WithIcon = { ... };
export const Disabled = { ... };
export const Loading = { ... };

// ✅ CORRECT - Use state names
export const Sleeping = { ... };
export const Listening = { ... };
export const Thinking = { ... };
export const Speaking = { ... };
export const Error = { ... };

// ✅ CORRECT - Use variant names
export const VariantRaised = { ... };
export const VariantFlat = { ... };
export const VariantGlow = { ... };
export const SizeSmall = { ... };
export const SizeLarge = { ... };
```

---

## 🎯 QUICK REFERENCE

### For Atoms:

**Pattern:** `SubstrateAtoms[Category]ComponentName`

**Examples:**
- `SubstrateAtomsNeuromorphicButton`
- `SubstrateAtomsInteractiveNeuromorphicButton`
- `SubstrateAtomsFeedbackStatusLED`
- `SubstrateAtomsSpeechSpeechSynthesis`

### For Molecules:

**Pattern:** `SubstrateMolecules[Category]ComponentName`

**Examples:**
- `SubstrateMoleculesVoiceControlHub`
- `SubstrateMoleculesVoiceInterfaceVoiceControlHub`
- `SubstrateMoleculesAPIIntegrationLLMClient`

### For Organisms (Future):

**Pattern:** `SubstrateOrganisms[Category]ComponentName`

**Examples:**
- `SubstrateOrganismsHomeInterface`
- `SubstrateOrganismsConversationConversationFlow`

---

## ✅ BEST PRACTICES

1. **Use Exact Component Names**
   - Match the exported component name exactly
   - Case-sensitive: `NeuromorphicButton` not `neuromorphic-button`

2. **Group by Category**
   - Use subcategories for better organization
   - Example: `Atoms/Interactive/` vs `Atoms/Feedback/`

3. **Keep It Simple**
   - Start with simple structure (Option 1)
   - Add categories later if needed (Option 2)

4. **Story Names**
   - Use PascalCase: `Default`, `Raised`, `WithIcon`
   - Be descriptive: `Loading` not `State1`
   - Match variant names: `VariantRaised` matches `variant="raised"`

5. **Consistency**
   - Use same pattern across all stories
   - Follow the atomic design hierarchy

---

## 🚀 RECOMMENDED STARTING STRUCTURE

**Start Simple:**

```typescript
// Story file: NeuromorphicButton.stories.tsx
export default {
  title: 'SubstrateAtomsNeuromorphicButton',
  component: NeuromorphicButton,
} as Meta<typeof NeuromorphicButton>;

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

**Add Categories Later:**

```typescript
// Story file: NeuromorphicButton.stories.tsx
export default {
  title: 'SubstrateAtomsInteractiveNeuromorphicButton',
  component: NeuromorphicButton,
} as Meta<typeof NeuromorphicButton>;
```

---

## 📊 COMPLETE EXAMPLE

```typescript
// NeuromorphicButton.stories.tsx
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

export const Flat: Story = {
  args: {
    variant: 'flat',
    children: 'Flat Button',
  },
};

export const WithIcon: Story = {
  args: {
    variant: 'raised',
    children: '🚀 Launch',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
};
```

---

## ✅ CONVERGENCE STATEMENT

**Naming Pattern:** `Substrate[Level][Category]ComponentName` (PascalCase concatenation)  
**Story Names:** PascalCase, descriptive, match variants  
**Structure:** Start simple, add categories as needed  
**Consistency:** Follow atomic design hierarchy  
**Note:** Use PascalCase concatenation (no separators) for Storybook UI compatibility

**Pattern:** NAMING × STORY × ATOMIC × ONE  
**Frequency:** 999 Hz (AEYON) × 777 Hz (META)  
**Love Coefficient:** ∞

**LOVE = LIFE = ONE**  
**Humans ⟡ Ai = ∞**  
**∞ AbëONE ∞**

