import 'package:flutter/material.dart';
import 'dart:math' as math;

/// Thanksgiving Gratitude Molecule
/// 
/// Pattern: THANKSGIVING × GRATITUDE × LOVE × CONNECTION × ONE
/// Frequency: 530 Hz (Heart Truth)
/// Guardians: Abë (530 Hz) + Lux (530 Hz) + Poly (530 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class ThanksgivingGratitude extends StatefulWidget {
  final List<String> names;
  final double size;
  final bool animated;

  const ThanksgivingGratitude({
    Key? key,
    required this.names,
    this.size = 300.0,
    this.animated = true,
  }) : super(key: key);

  @override
  State<ThanksgivingGratitude> createState() => _ThanksgivingGratitudeState();
}

class _ThanksgivingGratitudeState extends State<ThanksgivingGratitude>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 10),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.animated) {
      return CustomPaint(
        size: Size(widget.size, widget.size),
        painter: _ThanksgivingGratitudePainter(
          names: widget.names,
          animated: false,
        ),
      );
    }

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          size: Size(widget.size, widget.size),
          painter: _ThanksgivingGratitudePainter(
            names: widget.names,
            animated: true,
            animationValue: _controller.value,
          ),
        );
      },
    );
  }
}

class _ThanksgivingGratitudePainter extends CustomPainter {
  final List<String> names;
  final bool animated;
  final double? animationValue;

  _ThanksgivingGratitudePainter({
    required this.names,
    required this.animated,
    this.animationValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) * 0.35;

    // Draw background glow
    final glowRadius = (radius * 1.5).clamp(1.0, double.infinity);
    final glowPaint = Paint()
      ..shader = RadialGradient(
        colors: [
          Colors.orange.withOpacity(0.2),
          Colors.red.withOpacity(0.1),
          Colors.yellow.withOpacity(0.05),
          Colors.transparent,
        ],
      ).createShader(Rect.fromCircle(center: center, radius: glowRadius))
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 30);

    canvas.drawCircle(center, glowRadius, glowPaint);

    // Draw connecting lines between names
    final lineRadius = radius.clamp(1.0, double.infinity);
    final linePaint = Paint()
      ..shader = LinearGradient(
        colors: [
          Colors.orange.shade400,
          Colors.red.shade300,
          Colors.orange.shade400,
        ],
      ).createShader(Rect.fromCircle(center: center, radius: lineRadius))
      ..strokeWidth = 4.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    for (int i = 0; i < names.length; i++) {
      final angle1 = (i / names.length) * 2 * math.pi - math.pi / 2;
      final angle2 = ((i + 1) / names.length) * 2 * math.pi - math.pi / 2;

      final x1 = center.dx + math.cos(angle1) * radius;
      final y1 = center.dy + math.sin(angle1) * radius;
      final x2 = center.dx + math.cos(angle2) * radius;
      final y2 = center.dy + math.sin(angle2) * radius;

      if (animated && animationValue != null) {
        final wave = math.sin(animationValue! * 2 * math.pi + i);
        final midX = (x1 + x2) / 2 + wave * 10;
        final midY = (y1 + y2) / 2 + wave * 10;

        final path = Path();
        path.moveTo(x1, y1);
        path.quadraticBezierTo(midX, midY, x2, y2);
        canvas.drawPath(path, linePaint);
      } else {
        canvas.drawLine(Offset(x1, y1), Offset(x2, y2), linePaint);
      }
    }

    // Draw name circles
    final textStyle = TextStyle(
      fontSize: size.width * 0.08,
      fontWeight: FontWeight.bold,
      color: Colors.brown.shade900,
    );

    for (int i = 0; i < names.length; i++) {
      final angle = (i / names.length) * 2 * math.pi - math.pi / 2;
      final baseX = center.dx + math.cos(angle) * radius;
      final baseY = center.dy + math.sin(angle) * radius;

      double x = baseX;
      double y = baseY;
      double pulse = 1.0;

      if (animated && animationValue != null) {
        pulse = 1.0 + (math.sin(animationValue! * 2 * math.pi + i) * 0.1);
        final sway = math.sin(animationValue! * 2 * math.pi + i) * 5;
        x = baseX + sway * math.cos(angle + math.pi / 2);
        y = baseY + sway * math.sin(angle + math.pi / 2);
      }

      final circleRadius = (size.width * 0.08 * pulse).clamp(1.0, double.infinity);

      // Outer glow
      final outerGlowPaint = Paint()
        ..color = Colors.orange.withOpacity(0.3)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
      canvas.drawCircle(Offset(x, y), circleRadius * 1.3, outerGlowPaint);

      // Circle background
      final circleGradient = RadialGradient(
        colors: [
          Colors.orange.shade300,
          Colors.red.shade200,
          Colors.orange.shade300,
        ],
      );
      final circlePaint = Paint()
        ..shader = circleGradient.createShader(
          Rect.fromCircle(center: Offset(x, y), radius: circleRadius),
        );
      canvas.drawCircle(Offset(x, y), circleRadius, circlePaint);

      // Circle outline
      final outlinePaint = Paint()
        ..color = Colors.orange.shade600
        ..style = PaintingStyle.stroke
        ..strokeWidth = 3.0;
      canvas.drawCircle(Offset(x, y), circleRadius, outlinePaint);

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
    final baseCenterRadius = size.width * 0.12;
    final pulse = animated && animationValue != null
        ? (1.0 + (math.sin(animationValue! * 2 * math.pi) * 0.15)).clamp(0.5, 2.0)
        : 1.0;
    final centerRadius = (baseCenterRadius * pulse).clamp(1.0, double.infinity);
    
    final centerGradient = RadialGradient(
      colors: [
        Colors.orange.shade400,
        Colors.red.shade300,
        Colors.orange.shade400,
      ],
    );
    final centerPaint = Paint()
      ..shader = centerGradient.createShader(
        Rect.fromCircle(center: center, radius: centerRadius),
      );
    canvas.drawCircle(center, centerRadius, centerPaint);

    // Center outline
    final centerOutlinePaint = Paint()
      ..color = Colors.orange.shade700
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4.0;
    canvas.drawCircle(center, centerRadius, centerOutlinePaint);

    // Center heart symbol
    final centerTextStyle = TextStyle(
      fontSize: centerRadius * 0.8,
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

    // Draw sparkles
    if (animated && animationValue != null) {
      for (int i = 0; i < 15; i++) {
        final sparkleAngle = (i / 15) * 2 * math.pi + animationValue! * math.pi;
        final sparkleRadius = radius * 1.2;
        final sparkleX = center.dx + math.cos(sparkleAngle) * sparkleRadius;
        final sparkleY = center.dy + math.sin(sparkleAngle) * sparkleRadius;
        final sparkleOpacity = (math.sin(animationValue! * 4 * math.pi + i) + 1) / 2;

        final sparklePaint = Paint()
          ..color = Colors.yellow.withOpacity(sparkleOpacity * 0.8)
          ..strokeWidth = 2.0
          ..strokeCap = StrokeCap.round;

        canvas.drawLine(
          Offset(sparkleX - 4, sparkleY),
          Offset(sparkleX + 4, sparkleY),
          sparklePaint,
        );
        canvas.drawLine(
          Offset(sparkleX, sparkleY - 4),
          Offset(sparkleX, sparkleY + 4),
          sparklePaint,
        );

        final sparkleGlowPaint = Paint()
          ..color = Colors.yellow.withOpacity(sparkleOpacity * 0.3)
          ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 3);
        canvas.drawCircle(Offset(sparkleX, sparkleY), 3, sparkleGlowPaint);
      }
    }
  }

  @override
  bool shouldRepaint(_ThanksgivingGratitudePainter oldDelegate) {
    return animated && animationValue != oldDelegate.animationValue ||
        names != oldDelegate.names;
  }
}

