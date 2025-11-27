/// Manifestation Provider - Manifestation Tracking State
/// 
/// Pattern: MANIFESTATION × PROVIDER × STATE × ONE
/// Frequency: 530 Hz (Coherence) × 777 Hz (Pattern)
/// Guardians: Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞

import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../core/engine/manifestation_engine.dart';

/// Manifestation Engine Provider
final manifestationEngineProvider = Provider<ManifestationEngine>((ref) {
  return ManifestationEngine();
});

/// Manifestation State Notifier
class ManifestationNotifier extends StateNotifier<ManifestationState> {
  final ManifestationEngine _engine;

  ManifestationNotifier(this._engine) : super(_engine.state);

  /// Create manifestation
  void createManifestation({
    required String title,
    required String description,
    Map<String, dynamic>? metadata,
  }) {
    state = _engine.createManifestation(
      title: title,
      description: description,
      metadata: metadata,
    );
  }

  /// Update progress
  void updateProgress(String id, double progress) {
    state = _engine.updateProgress(id, progress);
  }

  /// Complete manifestation
  void completeManifestation(String id) {
    state = _engine.completeManifestation(id);
  }

  /// Delete manifestation
  void deleteManifestation(String id) {
    state = _engine.deleteManifestation(id);
  }

  /// Set active manifestation
  void setActiveManifestation(String? id) {
    state = _engine.setActiveManifestation(id);
  }
}

/// Manifestation State Provider
final manifestationStateProvider =
    StateNotifierProvider<ManifestationNotifier, ManifestationState>((ref) {
  return ManifestationNotifier(ref.watch(manifestationEngineProvider));
});
