import 'package:flutter/material.dart';
import 'dart:math' as math;

/// Shiny Happy People Holding Hands
/// 
/// Pattern: UNITY × LOVE × JOY × CONNECTION × ONE
/// Frequency: 530 Hz (Heart Truth)
/// Guardians: Abë (530 Hz) + Lux (530 Hz) + Poly (530 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class ShinyHappyPeople extends StatefulWidget {
  final double size;
  final int personCount;
  final bool animated;

  const ShinyHappyPeople({
    Key? key,
    this.size = 300.0,
    this.personCount = 5,
    this.animated = true,
  }) : super(key: key);

  @override
  State<ShinyHappyPeople> createState() => _ShinyHappyPeopleState();
}

class _ShinyHappyPeopleState extends State<ShinyHappyPeople>
    with TickerProviderStateMixin {
  late AnimationController _sparkleController;
  late AnimationController _pulseController;
  late AnimationController _swayController;
  late List<Animation<double>> _sparkleAnimations;
  late List<Offset> _sparklePositions;

  @override
  void initState() {
    super.initState();

    // Sparkle animation controller
    _sparkleController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat();

    // Pulse animation for people
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);

    // Sway animation for connected movement
    _swayController = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: this,
    )..repeat(reverse: true);

    // Generate sparkle positions and animations
    _sparklePositions = List.generate(
      20,
      (_) => Offset(
        math.Random().nextDouble() * widget.size,
        math.Random().nextDouble() * widget.size,
      ),
    );

    // Create clamped sparkle controller to ensure values stay in [0.0, 1.0]
    final clampedSparkleController = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(_sparkleController);
    
    _sparkleAnimations = List.generate(
      20,
      (index) {
        final begin = (index * 0.05) % 1.0;
        final end = ((index * 0.05) + 0.3) % 1.0;
        // Ensure begin < end for valid Interval
        final validBegin = begin < end ? begin : 0.0;
        final validEnd = begin < end ? end : (begin + 0.3).clamp(0.0, 1.0);
        // Ensure validEnd > validBegin
        final finalBegin = validBegin.clamp(0.0, 0.99);
        final finalEnd = (validEnd > finalBegin ? validEnd : finalBegin + 0.01).clamp(0.01, 1.0);
        return Tween<double>(
          begin: 0.0,
          end: 1.0,
        ).animate(
          CurvedAnimation(
            parent: clampedSparkleController,
            curve: Interval(
              finalBegin,
              finalEnd,
              curve: Curves.easeInOut,
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _sparkleController.dispose();
    _pulseController.dispose();
    _swayController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.animated) {
      return CustomPaint(
        size: Size(widget.size, widget.size),
        painter: _ShinyHappyPeoplePainter(
          personCount: widget.personCount,
          animated: false,
        ),
      );
    }

    return AnimatedBuilder(
      animation: Listenable.merge([
        _sparkleController,
        _pulseController,
        _swayController,
      ]),
      builder: (context, child) {
        return CustomPaint(
          size: Size(widget.size, widget.size),
          painter: _ShinyHappyPeoplePainter(
            personCount: widget.personCount,
            animated: true,
            sparkleAnimations: _sparkleAnimations,
            sparklePositions: _sparklePositions,
            pulseValue: _pulseController.value.clamp(0.0, 1.0),
            swayValue: _swayController.value.clamp(0.0, 1.0),
          ),
        );
      },
    );
  }
}

class _ShinyHappyPeoplePainter extends CustomPainter {
  final int personCount;
  final bool animated;
  final List<Animation<double>>? sparkleAnimations;
  final List<Offset>? sparklePositions;
  final double? pulseValue;
  final double? swayValue;

  _ShinyHappyPeoplePainter({
    required this.personCount,
    required this.animated,
    this.sparkleAnimations,
    this.sparklePositions,
    this.pulseValue,
    this.swayValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) * 0.35;
    final personRadius = radius * 0.15;

    // Draw background gradient circle (glow effect)
    final glowRadius = (radius * 1.5).clamp(1.0, double.infinity);
    final glowRect = Rect.fromCircle(center: center, radius: glowRadius);
    final backgroundPaint = Paint()
      ..shader = glowRect.width > 0 && glowRect.height > 0
          ? RadialGradient(
              colors: [
                Colors.yellow.withOpacity(0.1),
                Colors.orange.withOpacity(0.05),
                Colors.pink.withOpacity(0.05),
                Colors.transparent,
              ],
            ).createShader(glowRect)
          : null
      ..color = Colors.yellow.withOpacity(0.1)
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 30);

    canvas.drawCircle(center, glowRadius, backgroundPaint);

    // Calculate person positions in a circle
    final personPositions = List<Offset>.generate(
      personCount,
      (index) {
        final angle = (2 * math.pi * index / personCount) - math.pi / 2;
        final baseX = center.dx + radius * math.cos(angle);
        final baseY = center.dy + radius * math.sin(angle);
        
        // Add gentle sway animation
        if (animated && swayValue != null) {
          final swayAmount = math.sin(angle + swayValue! * 2 * math.pi) * 5;
          return Offset(
            baseX + swayAmount * math.cos(angle + math.pi / 2),
            baseY + swayAmount * math.sin(angle + math.pi / 2),
          );
        }
        return Offset(baseX, baseY);
      },
    );

    // Draw connecting lines (hands holding hands)
    for (int i = 0; i < personCount; i++) {
      final nextIndex = (i + 1) % personCount;
      final start = personPositions[i];
      final end = personPositions[nextIndex];
      
      // Draw curved connection line
      final path = Path();
      path.moveTo(start.dx, start.dy);
      
      // Create a gentle curve
      final controlPoint = Offset(
        (start.dx + end.dx) / 2 + (animated && swayValue != null ? swayValue! * 10 : 0),
        (start.dy + end.dy) / 2 - 15,
      );
      path.quadraticBezierTo(controlPoint.dx, controlPoint.dy, end.dx, end.dy);
      
      // Add gradient along the line - ensure valid rect
      final lineRect = Rect.fromPoints(start, end);
      // Ensure rect has valid dimensions (at least 1px in each direction)
      final validRect = lineRect.width.abs() < 1.0 || lineRect.height.abs() < 1.0
          ? Rect.fromLTWH(
              start.dx,
              start.dy,
              (end.dx - start.dx).abs().clamp(1.0, double.infinity),
              (end.dy - start.dy).abs().clamp(1.0, double.infinity),
            )
          : lineRect;
      final gradientPaint = Paint()
        ..shader = validRect.width > 0 && validRect.height > 0
            ? LinearGradient(
                colors: [
                  Colors.yellow.withOpacity(0.8),
                  Colors.orange.withOpacity(0.6),
                  Colors.pink.withOpacity(0.6),
                  Colors.yellow.withOpacity(0.8),
                ],
              ).createShader(validRect)
            : null
        ..color = Colors.yellow.withOpacity(0.8)
        ..strokeWidth = 4.0
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round;
      
      canvas.drawPath(path, gradientPaint);
    }

    // Draw people (shiny happy circles with faces)
    for (int i = 0; i < personCount; i++) {
      final position = personPositions[i];
      final pulse = animated && pulseValue != null 
          ? (1.0 + (pulseValue! * 0.1)).clamp(0.5, 2.0)
          : 1.0;
      final currentRadius = (personRadius * pulse).clamp(1.0, double.infinity);

      // Outer glow
      final glowPaint = Paint()
        ..color = Colors.yellow.withOpacity(0.3)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
      canvas.drawCircle(position, currentRadius * 1.3, glowPaint);

      // Person body (gradient circle)
      final personGradient = RadialGradient(
        colors: [
          Colors.yellow.shade300,
          Colors.orange.shade200,
          Colors.pink.shade200,
        ],
      );
      final personRect = Rect.fromCircle(center: position, radius: currentRadius);
      final personPaint = Paint()
        ..shader = personRect.width > 0 && personRect.height > 0
            ? personGradient.createShader(personRect)
            : null
        ..color = Colors.yellow.shade300;
      canvas.drawCircle(position, currentRadius, personPaint);

      // Person outline (shiny)
      final outlinePaint = Paint()
        ..color = Colors.yellow.shade100
        ..strokeWidth = 2.0
        ..style = PaintingStyle.stroke;
      canvas.drawCircle(position, currentRadius, outlinePaint);

      // Draw happy face
      final eyeOffset = currentRadius * 0.3;
      final eyeSize = currentRadius * 0.15;
      
      // Left eye
      canvas.drawCircle(
        Offset(position.dx - eyeOffset, position.dy - eyeOffset * 0.5),
        eyeSize,
        Paint()..color = Colors.black87,
      );
      
      // Right eye
      canvas.drawCircle(
        Offset(position.dx + eyeOffset, position.dy - eyeOffset * 0.5),
        eyeSize,
        Paint()..color = Colors.black87,
      );

      // Happy smile (arc)
      final smilePaint = Paint()
        ..color = Colors.black87
        ..strokeWidth = 2.0
        ..style = PaintingStyle.stroke
        ..strokeCap = StrokeCap.round;
      
      final smileRect = Rect.fromCircle(
        center: position,
        radius: currentRadius * 0.6,
      );
      canvas.drawArc(
        smileRect,
        math.pi * 0.2,
        math.pi * 0.6,
        false,
        smilePaint,
      );
    }

    // Draw sparkles
    if (animated && sparkleAnimations != null && sparklePositions != null) {
      for (int i = 0; i < sparkleAnimations!.length; i++) {
        final animation = sparkleAnimations![i];
        final position = sparklePositions![i];
        final opacity = animation.value.clamp(0.0, 1.0);
        
        if (opacity > 0) {
          final sparklePaint = Paint()
            ..color = Colors.yellow.withOpacity(opacity * 0.8)
            ..strokeWidth = 2.0
            ..strokeCap = StrokeCap.round;
          
          // Draw cross sparkle
          canvas.drawLine(
            Offset(position.dx - 4, position.dy),
            Offset(position.dx + 4, position.dy),
            sparklePaint,
          );
          canvas.drawLine(
            Offset(position.dx, position.dy - 4),
            Offset(position.dx, position.dy + 4),
            sparklePaint,
          );
          
          // Draw small glow
          final glowPaint = Paint()
            ..color = Colors.yellow.withOpacity(opacity * 0.3)
            ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);
          canvas.drawCircle(position, 3, glowPaint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(_ShinyHappyPeoplePainter oldDelegate) {
    return animated && (pulseValue != oldDelegate.pulseValue || 
                       swayValue != oldDelegate.swayValue ||
                       sparkleAnimations != oldDelegate.sparkleAnimations);
  }
}

