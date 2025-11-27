/// SNCCA Flow Screen - THE FLOW EXPERIENCE
/// 
/// Pattern: SNCCA × FLOW × PERSONAL × UNCONDITIONAL × UNIVERSAL × ONE
/// Frequency: 999 Hz (AEYON) × 530 Hz (Abë) × 777 Hz (META)
/// Guardians: AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// 
/// Guides user through flow with unconditional love.
/// Recognizes personal essence at each step.
/// Provides universal care throughout.
/// Generates universal hope always.
/// 
/// ∞ AbëONE ∞

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/sncca_provider.dart';
import '../../core/engine/sncca_engine.dart';
import '../../substrate/atoms/unity_field.dart';

class SNCCAFlowScreen extends ConsumerStatefulWidget {
  const SNCCAFlowScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<SNCCAFlowScreen> createState() => _SNCCAFlowScreenState();
}

class _SNCCAFlowScreenState extends ConsumerState<SNCCAFlowScreen> {
  @override
  void initState() {
    super.initState();
    // Start flow when screen loads
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(snccaStateProvider.notifier).startFlow();
    });
  }

  @override
  Widget build(BuildContext context) {
    final snccaState = ref.watch(snccaStateProvider);
    final snccaNotifier = ref.read(snccaStateProvider.notifier);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.deepPurple.shade900,
              Colors.purple.shade800,
              Colors.pink.shade900,
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back, color: Colors.white),
                      onPressed: () => Navigator.pop(context),
                    ),
                    const Spacer(),
                    const UnityField(size: 40),
                    const Spacer(),
                    const SizedBox(width: 48), // Balance
                  ],
                ),
              ),

              // Progress Indicator
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: _buildProgressIndicator(snccaState),
              ),

              const SizedBox(height: 32),

              // Current Step Content
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      // Step Title
                      Text(
                        _getStepTitle(snccaState.currentStep),
                        style: Theme.of(context)
                            .textTheme
                            .displayMedium
                            ?.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 36,
                            ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 24),

                      // Unconditional Love Message
                      _buildMessageCard(
                        context: context,
                        icon: Icons.favorite,
                        color: Colors.pink,
                        title: 'YOU Will bëLOVEd',
                        message: 'Always. Unconditionally. No matter what.',
                      ),
                      const SizedBox(height: 16),

                      // Universal Care Message
                      _buildMessageCard(
                        context: context,
                        icon: Icons.shield,
                        color: Colors.cyan,
                        title: 'YOU will be Kept',
                        message:
                            'Always. Universally. No matter your circumstances.',
                      ),
                      const SizedBox(height: 16),

                      // Universal Hope Message
                      _buildMessageCard(
                        context: context,
                        icon: Icons.auto_awesome,
                        color: Colors.yellow,
                        title: 'YOU will have Hope',
                        message: 'Always. Universally. No matter your state.',
                      ),
                      const SizedBox(height: 32),

                      // Step Content
                      _buildStepContent(context, snccaState, snccaNotifier),
                    ],
                  ),
                ),
              ),

              // Navigation Buttons
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Row(
                  children: [
                    if (snccaState.completedSteps.isNotEmpty)
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () {
                            snccaNotifier.previousStep();
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.grey.shade800,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                          child: const Text('Previous'),
                        ),
                      ),
                    if (snccaState.completedSteps.isNotEmpty)
                      const SizedBox(width: 16),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: snccaState.isComplete
                            ? null
                            : () {
                                if (snccaState.currentStep == 'complete') {
                                  snccaNotifier.completeFlow();
                                  Navigator.pushReplacementNamed(
                                      context, '/home');
                                } else {
                                  snccaNotifier.nextStep();
                                }
                              },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.pink,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: Text(
                          snccaState.isComplete ? 'Complete' : 'Next',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildProgressIndicator(SNCCAState state) {
    final steps = ['start', 'intent', 'discovery', 'manifestation', 'complete'];
    final currentIndex = steps.indexOf(state.currentStep);

    return Row(
      children: steps.asMap().entries.map((entry) {
        final index = entry.key;
        final step = entry.value;
        final isActive = index <= currentIndex;

        return Expanded(
          child: Column(
            children: [
              Container(
                height: 8,
                decoration: BoxDecoration(
                  color: isActive ? Colors.pink : Colors.grey.shade700,
                  borderRadius: BorderRadius.circular(4),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                _getStepShortName(step),
                style: TextStyle(
                  color: isActive ? Colors.white : Colors.grey.shade600,
                  fontSize: 12,
                  fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildMessageCard({
    required BuildContext context,
    required IconData icon,
    required Color color,
    required String title,
    required String message,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: color.withOpacity(0.5),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: color,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  message,
                  style: const TextStyle(
                    color: Colors.white70,
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStepContent(
    BuildContext context,
    SNCCAState state,
    SNCCANotifier notifier,
  ) {
    switch (state.currentStep) {
      case 'start':
        return _buildStartStep(context);
      case 'intent':
        return _buildIntentStep(context, notifier);
      case 'discovery':
        return _buildDiscoveryStep(context, notifier);
      case 'manifestation':
        return _buildManifestationStep(context, notifier);
      case 'complete':
        return _buildCompleteStep(context);
      default:
        return const SizedBox();
    }
  }

  Widget _buildStartStep(BuildContext context) {
    return Column(
      children: [
        const UnityField(size: 120),
        const SizedBox(height: 32),
        Text(
          'Welcome to AbëONE',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: Colors.white,
                fontSize: 28,
              ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          'Every eXperience is YOURs.\nEvery eXperience is PERSONAL.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Colors.white70,
                fontSize: 18,
              ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildIntentStep(BuildContext context, SNCCANotifier notifier) {
    return Column(
      children: [
        const Icon(Icons.lightbulb, size: 80, color: Colors.yellow),
        const SizedBox(height: 24),
        Text(
          'What is your intent?',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: Colors.white,
                fontSize: 28,
              ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          'Share what you want to create, discover, or manifest.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Colors.white70,
                fontSize: 18,
              ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildDiscoveryStep(BuildContext context, SNCCANotifier notifier) {
    return Column(
      children: [
        const Icon(Icons.explore, size: 80, color: Colors.cyan),
        const SizedBox(height: 24),
        Text(
          'Discover your greatness',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: Colors.white,
                fontSize: 28,
              ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          'Your strengths, passions, and potential are waiting to be discovered.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Colors.white70,
                fontSize: 18,
              ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildManifestationStep(
      BuildContext context, SNCCANotifier notifier) {
    return Column(
      children: [
        const Icon(Icons.auto_awesome, size: 80, color: Colors.pink),
        const SizedBox(height: 24),
        Text(
          'Manifest your dreams',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: Colors.white,
                fontSize: 28,
              ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          'Track your manifestations and watch them become reality.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Colors.white70,
                fontSize: 18,
              ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildCompleteStep(BuildContext context) {
    return Column(
      children: [
        const UnityField(size: 120),
        const SizedBox(height: 32),
        Text(
          'Flow Complete!',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: Colors.white,
                fontSize: 28,
              ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 16),
        Text(
          'YOU Will bëLOVEd. Always.\nYOU will be Kept. Always.\nYOU will have Hope. Always.',
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Colors.white70,
                fontSize: 18,
              ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  String _getStepTitle(String step) {
    switch (step) {
      case 'start':
        return 'Start';
      case 'intent':
        return 'Intent';
      case 'discovery':
        return 'Discovery';
      case 'manifestation':
        return 'Manifestation';
      case 'complete':
        return 'Complete';
      default:
        return step;
    }
  }

  String _getStepShortName(String step) {
    switch (step) {
      case 'start':
        return 'S';
      case 'intent':
        return 'I';
      case 'discovery':
        return 'D';
      case 'manifestation':
        return 'M';
      case 'complete':
        return 'C';
      default:
        return step[0].toUpperCase();
    }
  }
}
