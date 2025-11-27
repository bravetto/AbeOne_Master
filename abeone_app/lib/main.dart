import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'features/unity/unity_screen.dart';
import 'features/unity/materialization_screen.dart';
import 'features/thanksgiving/thanksgiving_video_screen.dart';
import 'features/thanksgiving/manifestation_interface.dart';
import 'features/onboarding/user_type_selection_screen.dart';
import 'features/onboarding/sncca_flow_screen.dart';
import 'features/home/home_screen.dart';

/// AbëONE App - Main Entry Point
/// 
/// Pattern: APP × UNITY × LOVE × JOY × MATERIALIZATION × ONE
/// Frequency: 999 Hz (AEYON) × 530 Hz (Heart Truth) × 777 Hz (META)
/// Guardians: AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
void main() {
  runApp(
    const ProviderScope(
      child: AbeOneApp(),
    ),
  );
}

class AbeOneApp extends StatelessWidget {
  const AbeOneApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AbëONE',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.orange,
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.orange,
          brightness: Brightness.light,
        ),
      ),
      home: const UserTypeSelectionScreen(), // THE FIRST EXPERIENCE - PERSONAL, UNCONDITIONAL, UNIVERSAL
      routes: {
        // '/' route removed - home property handles default route
        '/sncca': (context) => const SNCCAFlowScreen(),
        '/jah': (context) => const SNCCAFlowScreen(), // JAH Mode → SNCCA Flow
        '/children': (context) => const SNCCAFlowScreen(), // Children Mode → SNCCA Flow
        '/home': (context) => const HomeScreen(),
        '/unity': (context) => const UnityScreen(),
        '/materialization': (context) => const MaterializationScreen(),
        '/thanksgiving': (context) => const ThanksgivingVideoScreen(),
        '/manifest': (context) => const ManifestationInterface(),
      },
    );
  }
}

