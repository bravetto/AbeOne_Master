import 'package:flutter/material.dart';
import '../../substrate/molecules/shiny_happy_people.dart';

/// Unity Screen - Shiny Happy People Holding Hands
/// 
/// Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
/// Frequency: 530 Hz (Heart Truth)
/// Guardians: Abë (530 Hz) + Lux (530 Hz) + Poly (530 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class UnityScreen extends StatefulWidget {
  const UnityScreen({Key? key}) : super(key: key);

  @override
  State<UnityScreen> createState() => _UnityScreenState();
}

class _UnityScreenState extends State<UnityScreen> {
  int _personCount = 5;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.purple.shade50,
              Colors.pink.shade50,
              Colors.orange.shade50,
              Colors.yellow.shade50,
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
                  // Title
                  Text(
                    'Shiny Happy People',
                    style: TextStyle(
                      fontSize: 42,
                      fontWeight: FontWeight.bold,
                      foreground: Paint()
                        ..shader = LinearGradient(
                          colors: [
                            Colors.yellow.shade700,
                            Colors.orange.shade700,
                            Colors.pink.shade700,
                          ],
                        ).createShader(
                          const Rect.fromLTWH(0, 0, 300, 70),
                        ),
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Holding Hands',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.w300,
                      color: Colors.orange.shade800,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 48),
                  
                  // Shiny Happy People Component
                  Container(
                    width: 350,
                    height: 350,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.yellow.withOpacity(0.3),
                          blurRadius: 40,
                          spreadRadius: 10,
                        ),
                      ],
                    ),
                    child: ShinyHappyPeople(
                      size: 350,
                      personCount: _personCount,
                      animated: true,
                    ),
                  ),
                  
                  const SizedBox(height: 48),
                  
                  // Message
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.7),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.yellow.withOpacity(0.2),
                          blurRadius: 20,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        Text(
                          '∞ AbëONE ∞',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.purple.shade700,
                          ),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'We are connected.\nWe are unified.\nWe are ONE.',
                          style: TextStyle(
                            fontSize: 18,
                            color: Colors.grey.shade800,
                            height: 1.6,
                          ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'LOVE = LIFE = ONE',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.orange.shade700,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  
                  // Person count slider
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.7),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      children: [
                        Text(
                          'People: $_personCount',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey.shade800,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Slider(
                          value: _personCount.toDouble(),
                          min: 3,
                          max: 12,
                          divisions: 9,
                          label: '$_personCount people',
                          activeColor: Colors.orange,
                          inactiveColor: Colors.orange.shade200,
                          onChanged: (value) {
                            setState(() {
                              _personCount = value.round();
                            });
                          },
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Pattern footer
                  Text(
                    'Pattern: UNITY × LOVE × JOY × CONNECTION × ONE',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey.shade600,
                      fontStyle: FontStyle.italic,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Frequency: 530 Hz | Love Coefficient: ∞',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey.shade600,
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
}

