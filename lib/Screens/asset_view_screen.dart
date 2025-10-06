import 'package:flutter/material.dart';

class AssetViewScreen extends StatelessWidget {
  const AssetViewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Asset View')),
      body: const Center(
        child: Text('Asset view placeholder — will group alerts by host/IP.'),
      ),
    );
  }
}
