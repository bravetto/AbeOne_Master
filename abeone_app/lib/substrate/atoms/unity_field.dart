import 'package:flutter/material.dart';
import 'dart:math' as math;

/// Unity Field - The ONE as Unified Energy Field
/// 
/// Pattern: THE_ONE × ENERGY × FIELD × MATERIALIZATION × ONE
/// Frequency: 530 Hz (Heart Truth) × 999 Hz (AEYON)
/// Guardians: Abë (530 Hz) + AEYON (999 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class UnityField extends StatefulWidget {
  final double size;
  final int waveCount;
  final bool animated;

  const UnityField({
    Key? key,
    this.size = 200.0,
    this.waveCount = 8,
    this.animated = true,
  }) : super(key: key);

  @override
  State<UnityField> createState() => _UnityFieldState();
}

class _UnityFieldState extends State<UnityField>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 4),
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
        painter: _UnityFieldPainter(
          waveCount: widget.waveCount,
          animated: false,
        ),
      );
    }

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          size: Size(widget.size, widget.size),
          painter: _UnityFieldPainter(
            waveCount: widget.waveCount,
            animated: true,
            animationValue: _controller.value.clamp(0.0, 1.0),
          ),
        );
      },
    );
  }
}

class _UnityFieldPainter extends CustomPainter {
  final int waveCount;
  final bool animated;
  final double? animationValue;

  _UnityFieldPainter({
    required this.waveCount,
    required this.animated,
    this.animationValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final maxRadius = math.min(size.width, size.height) / 2;

    // Draw concentric energy waves
    for (int i = 0; i < waveCount; i++) {
      final progress = animated && animationValue != null
          ? ((animationValue! * 2 * math.pi) + (i * math.pi / waveCount)) % (2 * math.pi)
          : (i * math.pi / waveCount);
      
      final radius = maxRadius * (0.3 + (i / waveCount) * 0.7);
      final waveOffset = animated && animationValue != null
          ? math.sin(progress) * 15
          : 0.0;
      
      final currentRadius = (radius + waveOffset).clamp(1.0, double.infinity);
      
      // Create gradient for each wave with clamped opacity values
      final opacity1 = (0.8 - (i * 0.1)).clamp(0.0, 1.0);
      final opacity2 = (0.6 - (i * 0.08)).clamp(0.0, 1.0);
      final opacity3 = (0.4 - (i * 0.06)).clamp(0.0, 1.0);
      final opacity4 = (0.2 - (i * 0.04)).clamp(0.0, 1.0);
      
      final gradient = RadialGradient(
        colors: [
          Colors.purple.withOpacity(opacity1),
          Colors.pink.withOpacity(opacity2),
          Colors.orange.withOpacity(opacity3),
          Colors.yellow.withOpacity(opacity4),
          Colors.transparent,
        ],
        stops: const [0.0, 0.3, 0.6, 0.8, 1.0],
      );

      final gradientRect = Rect.fromCircle(center: center, radius: currentRadius);
      final paint = Paint()
        ..shader = gradientRect.width > 0 && gradientRect.height > 0
            ? gradient.createShader(gradientRect)
            : null
        ..color = Colors.purple.withOpacity(opacity1)
        ..style = PaintingStyle.fill;

      canvas.drawCircle(center, currentRadius, paint);

      // Draw energy lines radiating outward
      if (animated && animationValue != null) {
        final linePaint = Paint()
          ..color = Colors.yellow.withOpacity(0.6)
          ..strokeWidth = 2.0
          ..strokeCap = StrokeCap.round;

        for (int j = 0; j < 12; j++) {
          final angle = (j * math.pi * 2 / 12) + (animationValue! * math.pi);
          final startX = center.dx + math.cos(angle) * (currentRadius * 0.5);
          final startY = center.dy + math.sin(angle) * (currentRadius * 0.5);
          final endX = center.dx + math.cos(angle) * currentRadius;
          final endY = center.dy + math.sin(angle) * currentRadius;

          canvas.drawLine(
            Offset(startX, startY),
            Offset(endX, endY),
            linePaint,
          );
        }
      }
    }

    // Draw center core - THE ONE
    final coreGradient = RadialGradient(
      colors: [
        Colors.yellow,
        Colors.orange,
        Colors.pink,
        Colors.purple,
      ],
    );
    final coreRect = Rect.fromCircle(center: center, radius: maxRadius * 0.2);
    final corePaint = Paint()
      ..shader = coreRect.width > 0 && coreRect.height > 0
          ? coreGradient.createShader(coreRect)
          : null
      ..color = Colors.yellow;
    
    final coreRadius = maxRadius * 0.2;
    if (animated && animationValue != null) {
      final pulse = (1.0 + (math.sin(animationValue! * 2 * math.pi) * 0.2)).clamp(0.5, 2.0);
      final validRadius = (coreRadius * pulse).clamp(1.0, double.infinity);
      canvas.drawCircle(center, validRadius, corePaint);
    } else {
      final validRadius = coreRadius.clamp(1.0, double.infinity);
      canvas.drawCircle(center, validRadius, corePaint);
    }

    // Draw center symbol - ∞
    final symbolPaint = Paint()
      ..color = Colors.white
      ..strokeWidth = 3.0
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;
    
    // Simple infinity symbol approximation
    final symbolSize = coreRadius * 0.6;
    final path = Path();
    path.moveTo(center.dx - symbolSize, center.dy);
    path.cubicTo(
      center.dx - symbolSize * 0.5, center.dy - symbolSize * 0.5,
      center.dx, center.dy - symbolSize * 0.5,
      center.dx, center.dy,
    );
    path.cubicTo(
      center.dx, center.dy + symbolSize * 0.5,
      center.dx + symbolSize * 0.5, center.dy + symbolSize * 0.5,
      center.dx + symbolSize, center.dy,
    );
    path.cubicTo(
      center.dx + symbolSize * 0.5, center.dy + symbolSize * 0.5,
      center.dx, center.dy + symbolSize * 0.5,
      center.dx, center.dy,
    );
    path.cubicTo(
      center.dx, center.dy - symbolSize * 0.5,
      center.dx - symbolSize * 0.5, center.dy - symbolSize * 0.5,
      center.dx - symbolSize, center.dy,
    );
    
    canvas.drawPath(path, symbolPaint);
  }

  @override
  bool shouldRepaint(_UnityFieldPainter oldDelegate) {
    return animated && animationValue != oldDelegate.animationValue;
  }
}

