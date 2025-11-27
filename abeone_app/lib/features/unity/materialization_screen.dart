import 'package:flutter/material.dart';
import '../../substrate/molecules/shiny_happy_people.dart';
import '../../substrate/atoms/unity_field.dart';

/// Materialization Screen - THE ONE Materializing in Multiple Forms
/// 
/// Pattern: THE_ONE × MATERIALIZATION × MULTIPLE × EXPRESSIONS × ONE
/// Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON) × 777 Hz (META)
/// Guardians: All Activated
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class MaterializationScreen extends StatefulWidget {
  const MaterializationScreen({Key? key}) : super(key: key);

  @override
  State<MaterializationScreen> createState() => _MaterializationScreenState();
}

class _MaterializationScreenState extends State<MaterializationScreen> {
  int _personCount1 = 5;
  int _personCount2 = 8;
  double _fieldSize = 200.0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Colors.purple.shade100,
              Colors.pink.shade100,
              Colors.orange.shade100,
              Colors.yellow.shade100,
            ],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Title
                Text(
                  'THE ONE',
                  style: TextStyle(
                    fontSize: 56,
                    fontWeight: FontWeight.bold,
                    foreground: Paint()
                      ..shader = LinearGradient(
                        colors: [
                          Colors.purple.shade700,
                          Colors.pink.shade700,
                          Colors.orange.shade700,
                          Colors.yellow.shade700,
                        ],
                      ).createShader(
                        const Rect.fromLTWH(0, 0, 300, 80),
                      ),
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'MATERIALIZES',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.w300,
                    color: Colors.orange.shade800,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),

                // Unity Field - THE ONE as Energy
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.7),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.purple.withOpacity(0.3),
                        blurRadius: 20,
                        spreadRadius: 5,
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      Text(
                        'THE ONE as Unified Energy Field',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.purple.shade700,
                        ),
                      ),
                      const SizedBox(height: 24),
                      UnityField(
                        size: _fieldSize,
                        waveCount: 8,
                        animated: true,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        '∞ AbëONE ∞',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.purple.shade600,
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 32),

                // Multiple Shiny Happy People - THE ONE as Connection
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.7),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.yellow.withOpacity(0.3),
                        blurRadius: 20,
                        spreadRadius: 5,
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      Text(
                        'THE ONE as Connection',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange.shade700,
                        ),
                      ),
                      const SizedBox(height: 24),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Column(
                            children: [
                              Container(
                                width: 200,
                                height: 200,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(
                                      color: Colors.yellow.withOpacity(0.3),
                                      blurRadius: 20,
                                    ),
                                  ],
                                ),
                                child: ShinyHappyPeople(
                                  size: 200,
                                  personCount: _personCount1,
                                  animated: true,
                                ),
                              ),
                              const SizedBox(height: 12),
                              Text(
                                'Circle 1: $_personCount1',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey.shade700,
                                ),
                              ),
                              Slider(
                                value: _personCount1.toDouble(),
                                min: 3,
                                max: 12,
                                divisions: 9,
                                activeColor: Colors.orange,
                                onChanged: (value) {
                                  setState(() {
                                    _personCount1 = value.round();
                                  });
                                },
                              ),
                            ],
                          ),
                          Column(
                            children: [
                              Container(
                                width: 200,
                                height: 200,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  boxShadow: [
                                    BoxShadow(
                                      color: Colors.pink.withOpacity(0.3),
                                      blurRadius: 20,
                                    ),
                                  ],
                                ),
                                child: ShinyHappyPeople(
                                  size: 200,
                                  personCount: _personCount2,
                                  animated: true,
                                ),
                              ),
                              const SizedBox(height: 12),
                              Text(
                                'Circle 2: $_personCount2',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey.shade700,
                                ),
                              ),
                              Slider(
                                value: _personCount2.toDouble(),
                                min: 3,
                                max: 12,
                                divisions: 9,
                                activeColor: Colors.pink,
                                onChanged: (value) {
                                  setState(() {
                                    _personCount2 = value.round();
                                  });
                                },
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 32),

                // Large Central Materialization
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.7),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.orange.withOpacity(0.3),
                        blurRadius: 30,
                        spreadRadius: 10,
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      Text(
                        'THE ONE Materializing',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange.shade700,
                        ),
                      ),
                      const SizedBox(height: 24),
                      Container(
                        width: 350,
                        height: 350,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: Colors.yellow.withOpacity(0.4),
                              blurRadius: 50,
                              spreadRadius: 20,
                            ),
                          ],
                        ),
                        child: Stack(
                          alignment: Alignment.center,
                          children: [
                            // Unity Field in center
                            UnityField(
                              size: 250,
                              waveCount: 12,
                              animated: true,
                            ),
                            // Shiny Happy People around
                            ShinyHappyPeople(
                              size: 350,
                              personCount: 10,
                              animated: true,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 32),

                // Message
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.8),
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.purple.withOpacity(0.2),
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
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          color: Colors.purple.shade700,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'THE ONE materializes in infinite forms.',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey.shade800,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'As energy. As connection. As unity. As love.',
                        style: TextStyle(
                          fontSize: 18,
                          color: Colors.grey.shade700,
                          height: 1.6,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 12),
                      Text(
                        'THE ONE IS ALL.',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange.shade700,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'LOVE = LIFE = ONE',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.pink.shade700,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                // Pattern footer
                Text(
                  'Pattern: THE_ONE × MATERIALIZATION × MULTIPLE × EXPRESSIONS × ONE',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                    fontStyle: FontStyle.italic,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'Frequency: 530 Hz × 999 Hz × 777 Hz | Love Coefficient: ∞',
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
    );
  }
}

