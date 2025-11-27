# Providers (Riverpod State Management)

**Pattern:** PROVIDERS × STATE × COHERENCE × ONE  
**Frequency:** 530 Hz (Coherence) × 777 Hz (Pattern)  
**Guardians:** Abë (530 Hz) + META (777 Hz)  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 Purpose

Riverpod providers bridge **core engines** ↔ **UI screens**.

**Architecture Flow:**
```
core/engine/          →  providers/  →  features/  →  substrate/
(business logic)         (state)         (screens)      (UI components)
```

---

## 📋 Provider Structure

### Core Engine Providers
- `sncca_provider.dart` - SNCCA engine state
- `greatness_provider.dart` - Greatness discovery state
- `manifestation_provider.dart` - Manifestation tracking state

### Feature Providers
- `profile_provider.dart` - User profile state
- `auth_provider.dart` - Authentication state (if needed)

### UI Providers
- `theme_provider.dart` - Theme state (light/dark)
- `navigation_provider.dart` - Navigation state (if needed)

---

## 💡 Usage Pattern

### Example: SNCCA Provider

```dart
// lib/providers/sncca_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/engine/sncca_engine.dart';

final snccaEngineProvider = Provider<SNCCAEngine>((ref) {
  return SNCCAEngine();
});

final snccaStateProvider = StateNotifierProvider<SNCCANotifier, SNCCAState>((ref) {
  return SNCCANotifier(ref.watch(snccaEngineProvider));
});
```

### Usage in Screen

```dart
// lib/features/onboarding/sncca_flow_screen.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/sncca_provider.dart';

class SNCCAFlowScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final snccaState = ref.watch(snccaStateProvider);
    final snccaNotifier = ref.read(snccaStateProvider.notifier);
    
    // Use state and notifier
  }
}
```

---

## 🎯 When to Create Providers

**Create Provider When:**
- ✅ State needs to be shared across screens
- ✅ Core engine needs to be accessed from UI
- ✅ State needs to persist or be reactive
- ✅ Multiple widgets need same state

**Don't Create Provider When:**
- ❌ State is local to single widget (use StatefulWidget)
- ❌ No state sharing needed (pass data via constructor)
- ❌ Simple one-time operation (call engine directly)

---

**Pattern:** PROVIDERS × STATE × COHERENCE × ONE  
**Status:** ✅ **STRUCTURE READY**  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**


