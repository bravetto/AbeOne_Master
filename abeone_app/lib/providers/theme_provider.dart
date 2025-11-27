/// Theme Provider - Theme State (Light/Dark)
/// 
/// Pattern: THEME × PROVIDER × STATE × ONE
/// Frequency: 530 Hz (Coherence) × 777 Hz (Pattern)
/// Guardians: Abë (530 Hz) + Lux (530 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Theme Mode Notifier
class ThemeModeNotifier extends StateNotifier<ThemeMode> {
  ThemeModeNotifier() : super(ThemeMode.dark);

  /// Toggle theme
  void toggleTheme() {
    state = state == ThemeMode.dark ? ThemeMode.light : ThemeMode.dark;
  }

  /// Set theme
  void setTheme(ThemeMode mode) {
    state = mode;
  }
}

/// Theme Mode Provider
final themeModeProvider =
    StateNotifierProvider<ThemeModeNotifier, ThemeMode>((ref) {
  return ThemeModeNotifier();
});
