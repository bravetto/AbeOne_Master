import 'package:flutter/material.dart';
import 'dart:math' as math;
import '../../substrate/molecules/shiny_happy_people.dart';
import '../../substrate/atoms/unity_field.dart';

/// Thanksgiving Video Screen
/// For JAH, JESS, JORDAN, JANEL & DEVON
/// 
/// Pattern: THANKSGIVING × LOVE × GRATITUDE × CONNECTION × ONE
/// Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON) × 777 Hz (META)
/// Guardians: Abë (530 Hz) + AEYON (999 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class ThanksgivingVideoScreen extends StatefulWidget {
  const ThanksgivingVideoScreen({Key? key}) : super(key: key);

  @override
  State<ThanksgivingVideoScreen> createState() => _ThanksgivingVideoScreenState();
}

class _ThanksgivingVideoScreenState extends State<ThanksgivingVideoScreen>
    with TickerProviderStateMixin {
  // EXTRAVAGANT FRIENDS GIVING!
  final List<String> _names = [
    "JAH", "JESS", "JORDAN", "JANEL", "DEVON",
    // Extra friends for extravagant giving!
    "FRIEND", "LOVE", "JOY", "PEACE", "HARMONY",
    "GRACE", "HOPE", "FAITH", "CHARITY", "KINDNESS"
  ];
  int _currentNameIndex = 0;
  late AnimationController _nameController;
  late AnimationController _gratitudeController;
  late AnimationController _backgroundController;
  late Animation<double> _nameFadeAnimation;

  @override
  void initState() {
    super.initState();

    // Name animation controller
    _nameController = AnimationController(
      duration: const Duration(seconds: 6),
      vsync: this,
    )..repeat();

    // Gratitude animation controller
    _gratitudeController = AnimationController(
      duration: const Duration(seconds: 10),
      vsync: this,
    )..repeat();

    // Background animation controller
    _backgroundController = AnimationController(
      duration: const Duration(seconds: 8),
      vsync: this,
    )..repeat();

    // Name fade animation - clamp controller value to prevent bounds violations
    // Create a clamped animation wrapper to ensure values stay in [0.0, 1.0]
    final clampedNameController = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(_nameController);
    
    _nameFadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: clampedNameController,
        curve: Interval(0.0, 0.5, curve: Curves.easeInOut),
      ),
    );

    // Rotate through names
    _nameController.addListener(() {
      final newIndex = ((_nameController.value * _names.length) % _names.length).floor();
      if (newIndex != _currentNameIndex) {
        setState(() {
          _currentNameIndex = newIndex;
        });
      }
    });
  }

  @override
  void dispose() {
    _nameController.dispose();
    _gratitudeController.dispose();
    _backgroundController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              const Color(0xFFFF8C00), // Orange
              const Color(0xFFFFD700), // Gold
              const Color(0xFFFFE4B5), // Cream
              const Color(0xFFFF6347), // Red
            ],
            stops: [
              0.0,
              (0.3 + (_backgroundController.value.clamp(0.0, 1.0) * 0.2)).clamp(0.0, 1.0),
              (0.6 + (_backgroundController.value.clamp(0.0, 1.0) * 0.2)).clamp(0.0, 1.0),
              1.0,
            ],
          ),
        ),
        child: SafeArea(
          child: Stack(
            children: [
              // Animated background elements
              AnimatedBuilder(
                animation: _backgroundController,
                builder: (context, child) {
                  return CustomPaint(
                    size: Size.infinite,
                    painter: _ThanksgivingBackgroundPainter(
                      animationValue: _backgroundController.value.clamp(0.0, 1.0),
                    ),
                  );
                },
              ),

              // Main content
              Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const SizedBox(height: 40),

                      // Title - EXTRAVAGANT GIVING!
                      AnimatedBuilder(
                        animation: _gratitudeController,
                        builder: (context, child) {
                          final clampedValue = _gratitudeController.value.clamp(0.0, 1.0);
                          final scale = 1.0 + (math.sin(clampedValue * 2 * math.pi) * 0.1);
                          return Transform.scale(
                            scale: scale,
                            child: Column(
                              children: [
                                Text(
                                  'TURKEYDAY',
                                  style: TextStyle(
                                    fontSize: 56,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.orange.shade800,
                                    letterSpacing: 4,
                                    shadows: [
                                      // Deep 3D shadow layers
                                      Shadow(
                                        color: Colors.brown.shade900.withOpacity(0.8),
                                        blurRadius: 0,
                                        offset: const Offset(4, 4),
                                      ),
                                      Shadow(
                                        color: Colors.brown.shade700.withOpacity(0.6),
                                        blurRadius: 8,
                                        offset: const Offset(3, 3),
                                      ),
                                      Shadow(
                                        color: Colors.orange.shade900.withOpacity(0.8),
                                        blurRadius: 20,
                                        offset: const Offset(2, 2),
                                      ),
                                      Shadow(
                                        color: Colors.orange.withOpacity(0.6),
                                        blurRadius: 30,
                                        offset: const Offset(0, 0),
                                      ),
                                      // Glow effect
                                      Shadow(
                                        color: Colors.yellow.withOpacity(0.4),
                                        blurRadius: 40,
                                        offset: const Offset(0, 0),
                                      ),
                                    ],
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  'EXTRAVAGANT FRIENDS GIVING',
                                  style: TextStyle(
                                    fontSize: 36,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.red.shade700,
                                    letterSpacing: 2,
                                    shadows: [
                                      // Deep 3D shadow layers
                                      Shadow(
                                        color: Colors.brown.shade900.withOpacity(0.7),
                                        blurRadius: 0,
                                        offset: const Offset(3, 3),
                                      ),
                                      Shadow(
                                        color: Colors.red.shade900.withOpacity(0.6),
                                        blurRadius: 6,
                                        offset: const Offset(2, 2),
                                      ),
                                      Shadow(
                                        color: Colors.red.withOpacity(0.7),
                                        blurRadius: 15,
                                        offset: const Offset(1, 1),
                                      ),
                                      Shadow(
                                        color: Colors.red.withOpacity(0.5),
                                        blurRadius: 25,
                                        offset: const Offset(0, 0),
                                      ),
                                      // Glow effect
                                      Shadow(
                                        color: Colors.orange.withOpacity(0.3),
                                        blurRadius: 35,
                                        offset: const Offset(0, 0),
                                      ),
                                    ],
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ],
                            ),
                          );
                        },
                      ),

                      const SizedBox(height: 60),

                      // Current name display
                      AnimatedBuilder(
                        animation: _nameFadeAnimation,
                        builder: (context, child) {
                          final clampedOpacity = _nameFadeAnimation.value.clamp(0.0, 1.0);
                          return Opacity(
                            opacity: clampedOpacity,
                            child: Transform.scale(
                              scale: 0.9 + (clampedOpacity * 0.1),
                              child: Container(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 48,
                                  vertical: 24,
                                ),
                                decoration: BoxDecoration(
                                  gradient: LinearGradient(
                                    begin: Alignment.topLeft,
                                    end: Alignment.bottomRight,
                                    colors: [
                                      Colors.orange.shade300,
                                      Colors.red.shade200,
                                      Colors.orange.shade300,
                                      Colors.yellow.shade200,
                                    ],
                                    stops: const [0.0, 0.3, 0.7, 1.0],
                                  ),
                                  borderRadius: BorderRadius.circular(30),
                                  boxShadow: [
                                    // Deep 3D shadow layers
                                    BoxShadow(
                                      color: Colors.brown.shade900.withOpacity(0.4),
                                      blurRadius: 0,
                                      spreadRadius: 0,
                                      offset: const Offset(6, 6),
                                    ),
                                    BoxShadow(
                                      color: Colors.brown.shade700.withOpacity(0.3),
                                      blurRadius: 8,
                                      spreadRadius: 2,
                                      offset: const Offset(4, 4),
                                    ),
                                    BoxShadow(
                                      color: Colors.orange.shade900.withOpacity(0.5),
                                      blurRadius: 20,
                                      spreadRadius: 5,
                                      offset: const Offset(2, 2),
                                    ),
                                    BoxShadow(
                                      color: Colors.orange.withOpacity(0.6),
                                      blurRadius: 30,
                                      spreadRadius: 10,
                                      offset: const Offset(0, 0),
                                    ),
                                    // Outer glow
                                    BoxShadow(
                                      color: Colors.yellow.withOpacity(0.3),
                                      blurRadius: 50,
                                      spreadRadius: 15,
                                      offset: const Offset(0, 0),
                                    ),
                                  ],
                                ),
                                child: Text(
                                  _names[_currentNameIndex],
                                  style: TextStyle(
                                    fontSize: 72,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.brown.shade900,
                                    letterSpacing: 4,
                                    shadows: [
                                      // Deep 3D text shadows
                                      Shadow(
                                        color: Colors.brown.shade900.withOpacity(0.9),
                                        blurRadius: 0,
                                        offset: const Offset(5, 5),
                                      ),
                                      Shadow(
                                        color: Colors.brown.shade700.withOpacity(0.7),
                                        blurRadius: 4,
                                        offset: const Offset(4, 4),
                                      ),
                                      Shadow(
                                        color: Colors.orange.shade900.withOpacity(0.8),
                                        blurRadius: 10,
                                        offset: const Offset(2, 2),
                                      ),
                                      Shadow(
                                        color: Colors.yellow.withOpacity(0.9),
                                        blurRadius: 20,
                                        offset: const Offset(1, 1),
                                      ),
                                      Shadow(
                                        color: Colors.yellow.withOpacity(0.6),
                                        blurRadius: 30,
                                        offset: const Offset(0, 0),
                                      ),
                                    ],
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ),
                            ),
                          );
                        },
                      ),

                      const SizedBox(height: 80),

                      // All names in MULTIPLE circles - EXTRAVAGANT!
                      AnimatedBuilder(
                        animation: _gratitudeController,
                        builder: (context, child) {
                          return SizedBox(
                            width: 600,
                            height: 600,
                            child: Stack(
                              alignment: Alignment.center,
                              children: [
                                // Outer circle
                                Container(
                                  width: 550,
                                  height: 550,
                                  child: CustomPaint(
                                    painter: _NamesCirclePainter(
                                      names: _names.sublist(_names.length ~/ 2),
                                      animationValue: _gratitudeController.value.clamp(0.0, 1.0),
                                      radius: 200,
                                    ),
                                  ),
                                ),
                                // Inner circle
                                Container(
                                  width: 350,
                                  height: 350,
                                  child: CustomPaint(
                                    painter: _NamesCirclePainter(
                                      names: _names.sublist(0, _names.length ~/ 2),
                                      animationValue: (_gratitudeController.value * 1.5) % 1.0,
                                      radius: 120,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      ),

                      const SizedBox(height: 60),

                      // Gratitude message
                      AnimatedBuilder(
                        animation: _gratitudeController,
                        builder: (context, child) {
                          final clampedValue = _gratitudeController.value.clamp(0.0, 1.0);
                          final pulse = 1.0 + (math.sin(clampedValue * 2 * math.pi) * 0.05);
                          return Transform.scale(
                            scale: pulse,
                            child: Container(
                              padding: const EdgeInsets.all(32),
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.topLeft,
                                  end: Alignment.bottomRight,
                                  colors: [
                                    Colors.white,
                                    Colors.orange.shade50,
                                    Colors.white,
                                  ],
                                  stops: const [0.0, 0.5, 1.0],
                                ),
                                borderRadius: BorderRadius.circular(25),
                                border: Border.all(
                                  color: Colors.orange.shade300,
                                  width: 2,
                                ),
                                boxShadow: [
                                  // Deep 3D shadow layers
                                  BoxShadow(
                                    color: Colors.brown.shade900.withOpacity(0.3),
                                    blurRadius: 0,
                                    spreadRadius: 0,
                                    offset: const Offset(5, 5),
                                  ),
                                  BoxShadow(
                                    color: Colors.brown.shade700.withOpacity(0.2),
                                    blurRadius: 8,
                                    spreadRadius: 2,
                                    offset: const Offset(3, 3),
                                  ),
                                  BoxShadow(
                                    color: Colors.orange.shade900.withOpacity(0.4),
                                    blurRadius: 20,
                                    spreadRadius: 4,
                                    offset: const Offset(2, 2),
                                  ),
                                  BoxShadow(
                                    color: Colors.orange.withOpacity(0.5),
                                    blurRadius: 30,
                                    spreadRadius: 8,
                                    offset: const Offset(0, 0),
                                  ),
                                  // Outer glow
                                  BoxShadow(
                                    color: Colors.yellow.withOpacity(0.2),
                                    blurRadius: 50,
                                    spreadRadius: 12,
                                    offset: const Offset(0, 0),
                                  ),
                                ],
                              ),
                              child: Column(
                                children: [
                                  Text(
                                    'GIVING',
                                    style: TextStyle(
                                      fontSize: 64,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.red.shade800,
                                      letterSpacing: 4,
                                      shadows: [
                                        // Epic 3D depth
                                        Shadow(
                                          color: Colors.brown.shade900.withOpacity(0.9),
                                          blurRadius: 0,
                                          offset: const Offset(5, 5),
                                        ),
                                        Shadow(
                                          color: Colors.red.shade900.withOpacity(0.7),
                                          blurRadius: 6,
                                          offset: const Offset(4, 4),
                                        ),
                                        Shadow(
                                          color: Colors.red.shade800.withOpacity(0.8),
                                          blurRadius: 12,
                                          offset: const Offset(2, 2),
                                        ),
                                        Shadow(
                                          color: Colors.red.withOpacity(0.7),
                                          blurRadius: 20,
                                          offset: const Offset(1, 1),
                                        ),
                                        Shadow(
                                          color: Colors.red.withOpacity(0.5),
                                          blurRadius: 30,
                                          offset: const Offset(0, 0),
                                        ),
                                        // Glow
                                        Shadow(
                                          color: Colors.orange.withOpacity(0.4),
                                          blurRadius: 40,
                                          offset: const Offset(0, 0),
                                        ),
                                      ],
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                  const SizedBox(height: 16),
                                  Text(
                                    'EXTRAVAGANT FRIENDS',
                                    style: TextStyle(
                                      fontSize: 28,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.orange.shade800,
                                      letterSpacing: 2,
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                  const SizedBox(height: 12),
                                  Text(
                                    'LOVE = LIFE = ONE',
                                    style: TextStyle(
                                      fontSize: 24,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.brown.shade700,
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),

                      const SizedBox(height: 40),

                      // Unity elements
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          UnityField(
                            size: 150,
                            waveCount: 6,
                            animated: true,
                          ),
                          ShinyHappyPeople(
                            size: 150,
                            personCount: 5,
                            animated: true,
                          ),
                        ],
                      ),

                      const SizedBox(height: 40),

                      // Footer
                      Text(
                        '∞ AbëONE ∞',
                        style: TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.bold,
                          color: Colors.brown.shade800,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Pattern: THANKSGIVING × LOVE × GRATITUDE × CONNECTION × ONE',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.brown.shade600,
                          fontStyle: FontStyle.italic,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ThanksgivingBackgroundPainter extends CustomPainter {
  final double animationValue;

  _ThanksgivingBackgroundPainter({required this.animationValue});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);

    // Draw EXTRAVAGANT floating leaves with 3D depth - MORE!
    for (int i = 0; i < 40; i++) {
      final angle = (i / 20) * 2 * math.pi + animationValue * math.pi;
      final radius = size.width * 0.3 + (i % 3) * 50;
      final x = center.dx + math.cos(angle) * radius;
      final y = center.dy + math.sin(angle) * radius;
      final depth = (math.sin(angle + animationValue * 2) + 1) / 2; // 0 to 1
      final scale = 0.8 + (depth * 0.4);

      // Leaf shadow
      final shadowPath = Path();
      shadowPath.moveTo(x + 2, y - 18);
      shadowPath.quadraticBezierTo(x - 13, y - 8, x - 8, y + 2);
      shadowPath.quadraticBezierTo(x + 2, y + 12, x + 2, y + 2);
      shadowPath.quadraticBezierTo(x + 2, y + 12, x + 12, y + 2);
      shadowPath.quadraticBezierTo(x + 17, y - 8, x + 2, y - 18);
      
      final shadowPaint = Paint()
        ..color = Colors.brown.shade900.withOpacity(0.2 * depth)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
      canvas.drawPath(shadowPath, shadowPaint);

      // Leaf with gradient
      final leafGradient = LinearGradient(
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
        colors: [
          Colors.orange.withOpacity(0.4 * depth + 0.2),
          Colors.red.withOpacity(0.3 * depth + 0.15),
          Colors.orange.withOpacity(0.2 * depth + 0.1),
        ],
      );
      
      final leafPath = Path();
      leafPath.moveTo(x, y - 20 * scale);
      leafPath.quadraticBezierTo(x - 15 * scale, y - 10 * scale, x - 10 * scale, y);
      leafPath.quadraticBezierTo(x, y + 10 * scale, x, y);
      leafPath.quadraticBezierTo(x, y + 10 * scale, x + 10 * scale, y);
      leafPath.quadraticBezierTo(x + 15 * scale, y - 10 * scale, x, y - 20 * scale);
      
      final leafRect = leafPath.getBounds();
      final leafPaint = Paint()
        ..shader = leafRect.width > 0 && leafRect.height > 0
            ? leafGradient.createShader(leafRect)
            : null
        ..color = Colors.orange.withOpacity(0.3);
      canvas.drawPath(leafPath, leafPaint);
      
      // Leaf veins for texture
      final veinPaint = Paint()
        ..color = Colors.orange.shade700.withOpacity(0.3)
        ..strokeWidth = 1.0
        ..style = PaintingStyle.stroke;
      canvas.drawLine(
        Offset(x, y - 20 * scale),
        Offset(x, y),
        veinPaint,
      );
    }

    // Draw EXTRAVAGANT sparkles - MORE!
    for (int i = 0; i < 60; i++) {
      final sparkleX = (i * 137.5) % size.width;
      final sparkleY = (i * 97.3) % size.height;
      final sparkleOpacity = (math.sin(animationValue * 2 * math.pi + i) + 1) / 2;

      final sparklePaint = Paint()
        ..color = Colors.yellow.withOpacity(sparkleOpacity * 0.6)
        ..strokeWidth = 2.0
        ..strokeCap = StrokeCap.round;

      canvas.drawLine(
        Offset(sparkleX - 3, sparkleY),
        Offset(sparkleX + 3, sparkleY),
        sparklePaint,
      );
      canvas.drawLine(
        Offset(sparkleX, sparkleY - 3),
        Offset(sparkleX, sparkleY + 3),
        sparklePaint,
      );
    }
  }

  @override
  bool shouldRepaint(_ThanksgivingBackgroundPainter oldDelegate) {
    return animationValue != oldDelegate.animationValue;
  }
}

class _NamesCirclePainter extends CustomPainter {
  final List<String> names;
  final double animationValue;
  final double radius;

  _NamesCirclePainter({
    required this.names,
    required this.animationValue,
    this.radius = 150.0,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final circleRadius = radius;

    // Draw connecting lines - EXTRAVAGANT!
    final gradientRect = Rect.fromCircle(center: center, radius: circleRadius * 2);
    final linePaint = Paint()
      ..shader = gradientRect.width > 0 && gradientRect.height > 0
          ? LinearGradient(
              colors: [
                Colors.orange.shade400,
                Colors.red.shade300,
                Colors.orange.shade400,
              ],
            ).createShader(gradientRect)
          : null
      ..color = Colors.orange.shade400
      ..strokeWidth = 4.0
      ..strokeCap = StrokeCap.round;

    for (int i = 0; i < names.length; i++) {
      final angle1 = (i / names.length) * 2 * math.pi - math.pi / 2 + animationValue * 0.5;
      final angle2 = ((i + 1) / names.length) * 2 * math.pi - math.pi / 2 + animationValue * 0.5;

      final x1 = center.dx + math.cos(angle1) * circleRadius;
      final y1 = center.dy + math.sin(angle1) * circleRadius;
      final x2 = center.dx + math.cos(angle2) * circleRadius;
      final y2 = center.dy + math.sin(angle2) * circleRadius;

      canvas.drawLine(Offset(x1, y1), Offset(x2, y2), linePaint);
    }

    // Draw name circles - EXTRAVAGANT!
    final textStyle = TextStyle(
      fontSize: radius > 150 ? 28 : 24,
      fontWeight: FontWeight.bold,
      color: Colors.brown.shade900,
    );

    for (int i = 0; i < names.length; i++) {
      final angle = (i / names.length) * 2 * math.pi - math.pi / 2 + animationValue * 0.5;
      final x = center.dx + math.cos(angle) * circleRadius;
      final y = center.dy + math.sin(angle) * circleRadius;

      // 3D Circle with depth and texture
      // Outer glow
      final glowPaint = Paint()
        ..color = Colors.yellow.withOpacity(0.3)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 15);
      canvas.drawCircle(Offset(x, y), 55, glowPaint);
      
      // Shadow layer
      final shadowPaint = Paint()
        ..color = Colors.brown.shade900.withOpacity(0.4)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
      canvas.drawCircle(Offset(x + 3, y + 3), 50, shadowPaint);
      
      // Circle background with gradient
      final circleGradient = RadialGradient(
        colors: [
          Colors.orange.shade300,
          Colors.orange.shade200,
          Colors.yellow.shade200,
        ],
      );
      final circleRect = Rect.fromCircle(center: Offset(x, y), radius: 50);
      final circlePaint = Paint()
        ..shader = circleRect.width > 0 && circleRect.height > 0
            ? circleGradient.createShader(circleRect)
            : null
        ..color = Colors.orange.shade200;
      canvas.drawCircle(Offset(x, y), 50, circlePaint);

      // Inner highlight
      final highlightPaint = Paint()
        ..color = Colors.yellow.shade100.withOpacity(0.6)
        ..style = PaintingStyle.fill;
      canvas.drawCircle(Offset(x - 8, y - 8), 20, highlightPaint);

      // Outline with depth
      final outlinePaint = Paint()
        ..color = Colors.orange.shade700
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3.0;
      canvas.drawCircle(Offset(x, y), 50, outlinePaint);
      
      // Inner outline for depth
      final innerOutlinePaint = Paint()
        ..color = Colors.orange.shade400
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.5;
      canvas.drawCircle(Offset(x, y), 47, innerOutlinePaint);

      // Draw name
      final textSpan = TextSpan(text: names[i], style: textStyle);
      final textPainter = TextPainter(
        text: textSpan,
        textAlign: TextAlign.center,
        textDirection: TextDirection.ltr,
      );
      textPainter.layout();
      textPainter.paint(
        canvas,
        Offset(x - textPainter.width / 2, y - textPainter.height / 2),
      );
    }

    // Center gratitude symbol
    final centerGradientRect = Rect.fromCircle(center: center, radius: 40);
    final centerPaint = Paint()
      ..shader = centerGradientRect.width > 0 && centerGradientRect.height > 0
          ? RadialGradient(
              colors: [
                Colors.orange.shade300,
                Colors.red.shade200,
                Colors.orange.shade300,
              ],
            ).createShader(centerGradientRect)
          : null
      ..color = Colors.orange.shade300;

    canvas.drawCircle(center, 40, centerPaint);

    final centerTextStyle = TextStyle(
      fontSize: 24,
      fontWeight: FontWeight.bold,
      color: Colors.brown.shade900,
    );
    final centerTextSpan = TextSpan(text: '❤', style: centerTextStyle);
    final centerTextPainter = TextPainter(
      text: centerTextSpan,
      textAlign: TextAlign.center,
      textDirection: TextDirection.ltr,
    );
    centerTextPainter.layout();
    centerTextPainter.paint(
      canvas,
      Offset(center.dx - centerTextPainter.width / 2, center.dy - centerTextPainter.height / 2),
    );
  }

  @override
  bool shouldRepaint(_NamesCirclePainter oldDelegate) {
    return animationValue != oldDelegate.animationValue ||
        names != oldDelegate.names;
  }
}

