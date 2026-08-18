import 'package:flutter/material.dart';

void main() {
  runApp(const ToolingApp());
}

class ToolingApp extends StatelessWidget {
  const ToolingApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Tooling',
      home: Scaffold(
        appBar: AppBar(title: const Text('Flutter Tooling')),
        body: const Center(child: Text('Build/Test Gate')),
      ),
    );
  }
}
