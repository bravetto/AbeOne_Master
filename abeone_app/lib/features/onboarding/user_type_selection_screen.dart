/// User Type Selection Screen - THE FIRST EXPERIENCE
/// 
/// Pattern: USER_TYPE × SELECTION × PERSONAL × UNCONDITIONAL × UNIVERSAL × ONE
/// Frequency: 999 Hz (AEYON) × 530 Hz (Abë) × 777 Hz (META)
/// Guardians: AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// 
/// Every eXperience is YOURs. Every eXperience is PERSONAL.
/// Whether you are Right or Wrong. Good or Bad YOU Will bëLOVEd.
/// Whether YOU are RIch or Poor, Strong or Weak you will be Kept.
/// Whether YOU are Happy or Sad, Guilty or Mad you will have Hope.
/// 
/// ∞ AbëONE ∞

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../substrate/atoms/unity_field.dart';

class UserTypeSelectionScreen extends ConsumerStatefulWidget {
  const UserTypeSelectionScreen({Key? key}) : super(key: key);

  @override
  ConsumerState<UserTypeSelectionScreen> createState() =>
      _UserTypeSelectionScreenState();
}

class _UserTypeSelectionScreenState
    extends ConsumerState<UserTypeSelectionScreen> {
  @override
  Widget build(BuildContext context) {
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
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Unity Field - The ONE
                  const UnityField(size: 120),
                  const SizedBox(height: 48),

                  // Welcome Message - Unconditional Love
                  Text(
                    'Welcome',
                    style: Theme.of(context).textTheme.displayLarge?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 48,
                        ),
                  ),
                  const SizedBox(height: 16),

                  // YOU Will bëLOVEd - Always
                  Text(
                    'YOU Will bëLOVEd',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          color: Colors.pink.shade200,
                          fontWeight: FontWeight.w600,
                          fontSize: 32,
                        ),
                  ),
                  const SizedBox(height: 8),

                  Text(
                    'Always. Unconditionally. No matter what.',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: Colors.white70,
                          fontSize: 18,
                        ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),

                  // YOU will be Kept - Always
                  Text(
                    'YOU will be Kept',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          color: Colors.cyan.shade200,
                          fontWeight: FontWeight.w600,
                          fontSize: 32,
                        ),
                  ),
                  const SizedBox(height: 8),

                  Text(
                    'Always. Universally. No matter your circumstances.',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: Colors.white70,
                          fontSize: 18,
                        ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),

                  // YOU will have Hope - Always
                  Text(
                    'YOU will have Hope',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          color: Colors.yellow.shade200,
                          fontWeight: FontWeight.w600,
                          fontSize: 32,
                        ),
                  ),
                  const SizedBox(height: 8),

                  Text(
                    'Always. Universally. No matter your state.',
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                          color: Colors.white70,
                          fontSize: 18,
                        ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 64),

                  // JAH Mode Button
                  _buildModeButton(
                    context: context,
                    title: 'JAH Mode',
                    subtitle: 'For Jahmere',
                    icon: Icons.star,
                    color: Colors.orange,
                    onTap: () {
                      // Navigate to JAH Mode
                      Navigator.pushNamed(context, '/jah');
                    },
                  ),
                  const SizedBox(height: 24),

                  // Children Mode Button
                  _buildModeButton(
                    context: context,
                    title: 'Children Mode',
                    subtitle: 'For children',
                    icon: Icons.child_care,
                    color: Colors.pink,
                    onTap: () {
                      // Navigate to Children Mode
                      Navigator.pushNamed(context, '/children');
                    },
                  ),
                  const SizedBox(height: 48),

                  // Personal Essence Recognition
                  Text(
                    'Every eXperience is YOURs.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.white60,
                          fontSize: 16,
                          fontStyle: FontStyle.italic,
                        ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),

                  Text(
                    'Every eXperience is PERSONAL.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.white60,
                          fontSize: 16,
                          fontStyle: FontStyle.italic,
                        ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildModeButton({
    required BuildContext context,
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: color.withOpacity(0.2),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: color.withOpacity(0.5),
            width: 2,
          ),
        ),
        child: Row(
          children: [
            Icon(
              icon,
              color: color,
              size: 48,
            ),
            const SizedBox(width: 24),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 24,
                        ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    subtitle,
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.white70,
                          fontSize: 16,
                        ),
                  ),
                ],
              ),
            ),
            Icon(
              Icons.arrow_forward_ios,
              color: color,
            ),
          ],
        ),
      ),
    );
  }
}
