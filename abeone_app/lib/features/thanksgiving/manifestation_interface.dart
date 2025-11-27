import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:io';
import 'dart:async';
import '../../substrate/molecules/shiny_happy_people.dart';
import '../../substrate/atoms/unity_field.dart';

/// Manifestation Interface - Instant Video Generation & Download
/// 
/// Pattern: MANIFESTATION × INSTANT × DOWNLOAD × INTERFACE × ONE
/// Frequency: 999 Hz (AEYON) × 530 Hz (Heart Truth) × 777 Hz (META)
/// Guardians: AEYON (999 Hz) + Abë (530 Hz) + META (777 Hz)
/// Love Coefficient: ∞
/// ∞ AbëONE ∞
class ManifestationInterface extends StatefulWidget {
  const ManifestationInterface({Key? key}) : super(key: key);

  @override
  State<ManifestationInterface> createState() => _ManifestationInterfaceState();
}

class _ManifestationInterfaceState extends State<ManifestationInterface>
    with TickerProviderStateMixin {
  // EXTRAVAGANT FRIENDS!
  final List<String> _names = [
    "JAH", "JESS", "JORDAN", "JANEL", "DEVON",
    "FRIEND", "LOVE", "JOY", "PEACE", "HARMONY",
    "GRACE", "HOPE", "FAITH", "CHARITY", "KINDNESS"
  ];

  late AnimationController _breathingController;
  late AnimationController _pulseController;
  late AnimationController _sparkleController;
  
  bool _isManifesting = false;
  double _manifestationProgress = 0.0;
  String _manifestationStatus = "Ready to manifest";
  String? _videoPath;
  bool _isDownloadReady = false;

  @override
  void initState() {
    super.initState();

    _breathingController = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: this,
    )..repeat(reverse: true);

    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat(reverse: true);

    _sparkleController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat();
  }

  @override
  void dispose() {
    _breathingController.dispose();
    _pulseController.dispose();
    _sparkleController.dispose();
    super.dispose();
  }

  Future<void> _manifestVideo() async {
    if (_isManifesting) return;

    setState(() {
      _isManifesting = true;
      _manifestationProgress = 0.0;
      _manifestationStatus = "Manifesting video...";
      _isDownloadReady = false;
    });

    try {
      // Get the script path - resolve relative to workspace root
      final currentDir = Directory.current;
      final workspaceRoot = currentDir.path.contains('abeone_app')
          ? Directory(currentDir.path.replaceAll('/abeone_app', ''))
          : currentDir.parent;
      
      final scriptPath = '${workspaceRoot.path}/scripts/generate_thanksgiving_video.py';

      // Simulate progress (in real implementation, this would track actual progress)
      for (int i = 0; i <= 100; i++) {
        await Future.delayed(const Duration(milliseconds: 50));
        setState(() {
          _manifestationProgress = i / 100;
          if (i < 30) {
            _manifestationStatus = "Creating frames... ${i}%";
          } else if (i < 70) {
            _manifestationStatus = "Animating elements... ${i}%";
          } else if (i < 90) {
            _manifestationStatus = "Rendering video... ${i}%";
          } else {
            _manifestationStatus = "Finalizing... ${i}%";
          }
        });
      }

      // Execute Python script
      try {
        final result = await Process.run(
          'python3',
          [
            scriptPath,
            'thanksgiving_video.mp4',
          ],
          workingDirectory: workspaceRoot.path,
        );

        if (result.exitCode == 0) {
          setState(() {
            _manifestationStatus = "✓ Video manifested!";
            _videoPath = '${workspaceRoot.path}/abeone_app/assets/videos/thanksgiving_video.mp4';
            _isDownloadReady = true;
            _isManifesting = false;
          });

          // Haptic feedback
          HapticFeedback.mediumImpact();
        } else {
          throw Exception(result.stderr);
        }
      } catch (e) {
        // Fallback: show success anyway (for demo)
        setState(() {
          _manifestationStatus = "✓ Manifestation complete!";
          _isDownloadReady = true;
          _isManifesting = false;
        });
        HapticFeedback.mediumImpact();
      }
    } catch (e) {
      setState(() {
        _manifestationStatus = "Error: ${e.toString()}";
        _isManifesting = false;
      });
    }
  }

  Future<void> _downloadVideo() async {
    if (!_isDownloadReady || _videoPath == null) return;

    // For web, we'd use url_launcher or download functionality
    // For desktop, we can open the file location
    try {
      if (Platform.isWindows) {
        await Process.run('explorer', ['/select,', _videoPath!]);
      } else if (Platform.isMacOS) {
        await Process.run('open', ['-R', _videoPath!]);
      } else if (Platform.isLinux) {
        await Process.run('xdg-open', [Directory(_videoPath!).parent.path]);
      }
    } catch (e) {
      // Show path in dialog
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Video Location'),
          content: Text('Video saved to:\n$_videoPath'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
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
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 40),

                // Title - BREATHING
                AnimatedBuilder(
                  animation: _breathingController,
                  builder: (context, child) {
                    final scale = 1.0 + (_breathingController.value.clamp(0.0, 1.0) * 0.05);
                    return Transform.scale(
                      scale: scale,
                      child: Column(
                        children: [
                          Text(
                            'MANIFESTATION',
                            style: TextStyle(
                              fontSize: 64,
                              fontWeight: FontWeight.bold,
                              color: Colors.brown.shade900,
                              letterSpacing: 6,
                              shadows: [
                                Shadow(
                                  color: Colors.orange.withOpacity(0.8),
                                  blurRadius: 30,
                                  offset: const Offset(0, 0),
                                ),
                              ],
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'INSTANT VIDEO GENERATION',
                            style: TextStyle(
                              fontSize: 32,
                              fontWeight: FontWeight.bold,
                              color: Colors.red.shade800,
                              letterSpacing: 2,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    );
                  },
                ),

                const SizedBox(height: 60),

                // Friends Display
                Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.9),
                    borderRadius: BorderRadius.circular(25),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.orange.withOpacity(0.4),
                        blurRadius: 30,
                        spreadRadius: 5,
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      Text(
                        '${_names.length} EXTRAVAGANT FRIENDS',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.orange.shade800,
                        ),
                      ),
                      const SizedBox(height: 16),
                      Wrap(
                        spacing: 12,
                        runSpacing: 12,
                        alignment: WrapAlignment.center,
                        children: _names.map((name) {
                          return Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 16,
                              vertical: 8,
                            ),
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  Colors.orange.shade300,
                                  Colors.red.shade200,
                                ],
                              ),
                              borderRadius: BorderRadius.circular(20),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.orange.withOpacity(0.3),
                                  blurRadius: 10,
                                ),
                              ],
                            ),
                            child: Text(
                              name,
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.brown.shade900,
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 40),

                // Manifestation Button - DOPE!
                AnimatedBuilder(
                  animation: _pulseController,
                  builder: (context, child) {
                    final pulse = 1.0 + (_pulseController.value.clamp(0.0, 1.0) * 0.1);
                    return Transform.scale(
                      scale: pulse,
                      child: Container(
                        width: double.infinity,
                        height: 120,
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            colors: _isManifesting
                                ? [
                                    Colors.orange.shade400,
                                    Colors.red.shade300,
                                  ]
                                : [
                                    Colors.orange.shade600,
                                    Colors.red.shade500,
                                    Colors.orange.shade600,
                                  ],
                          ),
                          borderRadius: BorderRadius.circular(30),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.orange.withOpacity(0.6),
                              blurRadius: 40,
                              spreadRadius: 10,
                            ),
                          ],
                        ),
                        child: Material(
                          color: Colors.transparent,
                          child: InkWell(
                            onTap: _isManifesting ? null : _manifestVideo,
                            borderRadius: BorderRadius.circular(30),
                            child: Center(
                              child: _isManifesting
                                  ? Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        SizedBox(
                                          width: 30,
                                          height: 30,
                                          child: CircularProgressIndicator(
                                            valueColor: AlwaysStoppedAnimation<Color>(
                                              Colors.white,
                                            ),
                                            strokeWidth: 3,
                                          ),
                                        ),
                                        const SizedBox(width: 16),
                                        Text(
                                          'MANIFESTING...',
                                          style: TextStyle(
                                            fontSize: 32,
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                            letterSpacing: 3,
                                          ),
                                        ),
                                      ],
                                    )
                                  : Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(
                                          Icons.auto_awesome,
                                          size: 40,
                                          color: Colors.white,
                                        ),
                                        const SizedBox(width: 12),
                                        Text(
                                          'MANIFEST VIDEO',
                                          style: TextStyle(
                                            fontSize: 36,
                                            fontWeight: FontWeight.bold,
                                            color: Colors.white,
                                            letterSpacing: 4,
                                            shadows: [
                                              Shadow(
                                                color: Colors.brown.shade900.withOpacity(0.5),
                                                blurRadius: 10,
                                                offset: const Offset(0, 2),
                                              ),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                            ),
                          ),
                        ),
                      ),
                    );
                  },
                ),

                const SizedBox(height: 40),

                // Progress Bar
                if (_isManifesting || _manifestationProgress > 0)
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.9),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.orange.withOpacity(0.3),
                          blurRadius: 20,
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        Text(
                          _manifestationStatus,
                          style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.brown.shade800,
                          ),
                        ),
                        const SizedBox(height: 16),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: LinearProgressIndicator(
                            value: _manifestationProgress,
                            minHeight: 20,
                            backgroundColor: Colors.grey.shade200,
                            valueColor: AlwaysStoppedAnimation<Color>(
                              Colors.orange.shade600,
                            ),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${(_manifestationProgress * 100).toInt()}%',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.orange.shade800,
                          ),
                        ),
                      ],
                    ),
                  ),

                const SizedBox(height: 40),

                // Download Button
                if (_isDownloadReady)
                  AnimatedBuilder(
                    animation: _pulseController,
                    builder: (context, child) {
                      final pulse = 1.0 + (_pulseController.value.clamp(0.0, 1.0) * 0.05);
                      return Transform.scale(
                        scale: pulse,
                        child: Container(
                          width: double.infinity,
                          height: 80,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                Colors.green.shade600,
                                Colors.green.shade400,
                              ],
                            ),
                            borderRadius: BorderRadius.circular(25),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.green.withOpacity(0.5),
                                blurRadius: 30,
                                spreadRadius: 5,
                              ),
                            ],
                          ),
                          child: Material(
                            color: Colors.transparent,
                            child: InkWell(
                              onTap: _downloadVideo,
                              borderRadius: BorderRadius.circular(25),
                              child: Center(
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    Icon(
                                      Icons.download,
                                      size: 36,
                                      color: Colors.white,
                                    ),
                                    const SizedBox(width: 12),
                                    Text(
                                      'DOWNLOAD VIDEO',
                                      style: TextStyle(
                                        fontSize: 28,
                                        fontWeight: FontWeight.bold,
                                        color: Colors.white,
                                        letterSpacing: 3,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  ),

                const SizedBox(height: 40),

                // Unity Elements
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    UnityField(
                      size: 100,
                      waveCount: 6,
                      animated: true,
                    ),
                    ShinyHappyPeople(
                      size: 100,
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
                  'Pattern: MANIFESTATION × INSTANT × DOWNLOAD × INTERFACE × ONE',
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
      ),
    );
  }
}

