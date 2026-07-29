import 'package:flutter/material.dart';

class AppTheme {

  static final ThemeData light = ThemeData(
    useMaterial3: true,

    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF38A3F0),
      brightness: Brightness.light,
    ),

    scaffoldBackgroundColor: const Color(0xFFF5F7FA),

    cardColor: Colors.white,
  );

  static final ThemeData dark = ThemeData(
    useMaterial3: true,

    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF38A3F0),
      brightness: Brightness.dark,
    ),

    scaffoldBackgroundColor: const Color(0xFF121212),

    cardColor: const Color(0xFF1E1E1E),
  );
}