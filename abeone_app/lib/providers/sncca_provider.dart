/// SNCCA Provider - SNCCA Engine State
/// 
/// Pattern: SNCCA × PROVIDER × STATE × ONE
/// Frequency: 530 Hz (Coherence) × 777 Hz (Pattern)
/// Guardians: Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/engine/sncca_engine.dart';

/// SNCCA Engine Provider
final snccaEngineProvider = Provider<SNCCAEngine>((ref) {
  return SNCCAEngine();
});

/// SNCCA State Notifier
class SNCCANotifier extends StateNotifier<SNCCAState> {
  final SNCCAEngine _engine;

  SNCCANotifier(this._engine) : super(_engine.state);

  /// Start flow
  void startFlow() {
    state = _engine.startFlow();
  }

  /// Next step
  void nextStep({Map<String, dynamic>? data}) {
    state = _engine.nextStep(data: data);
  }

  /// Previous step
  void previousStep() {
    state = _engine.previousStep();
  }

  /// Update flow data
  void updateFlowData(Map<String, dynamic> data) {
    state = _engine.updateFlowData(data);
  }

  /// Complete flow
  void completeFlow() {
    state = _engine.completeFlow();
  }
}

/// SNCCA State Provider
final snccaStateProvider =
    StateNotifierProvider<SNCCANotifier, SNCCAState>((ref) {
  return SNCCANotifier(ref.watch(snccaEngineProvider));
});
