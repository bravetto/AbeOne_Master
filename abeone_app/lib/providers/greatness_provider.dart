/// Greatness Provider - Greatness Discovery State
/// 
/// Pattern: GREATNESS × PROVIDER × STATE × ONE
/// Frequency: 530 Hz (Coherence) × 777 Hz (Pattern)
/// Guardians: Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/engine/greatness_engine.dart';

/// Greatness Engine Provider
final greatnessEngineProvider = Provider<GreatnessEngine>((ref) {
  return GreatnessEngine();
});

/// Greatness State Notifier
class GreatnessNotifier extends StateNotifier<GreatnessState> {
  final GreatnessEngine _engine;

  GreatnessNotifier(this._engine) : super(_engine.state);

  /// Discover strength
  void discoverStrength(String strength) {
    state = _engine.discoverStrength(strength);
  }

  /// Discover passion
  void discoverPassion(String passion) {
    state = _engine.discoverPassion(passion);
  }

  /// Discover potential
  void discoverPotential(String potential) {
    state = _engine.discoverPotential(potential);
  }

  /// Update discovery data
  void updateDiscoveryData(Map<String, dynamic> data) {
    state = _engine.updateDiscoveryData(data);
  }

  /// Complete discovery
  void completeDiscovery() {
    state = _engine.completeDiscovery();
  }

  /// Reset discovery
  void resetDiscovery() {
    state = _engine.resetDiscovery();
  }
}

/// Greatness State Provider
final greatnessStateProvider =
    StateNotifierProvider<GreatnessNotifier, GreatnessState>((ref) {
  return GreatnessNotifier(ref.watch(greatnessEngineProvider));
});
