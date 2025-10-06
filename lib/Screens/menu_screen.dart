import 'package:flutter/material.dart';
import '../data/dummy_data.dart';

class MenuScreen extends StatelessWidget {
  const MenuScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final watchlistBadge = 2; // demo bubble

    return Scaffold(
      appBar: AppBar(title: const Text('SOC Console')),
      body: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 420),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _menuButton(
                  context,
                  label: 'Alert Detail Page',
                  onTap: () => Navigator.pushNamed(context, '/alertDetail'),
                ),
                _menuButton(
                  context,
                  label: 'Timeline View',
                  onTap: () => Navigator.pushNamed(context, '/timeline'),
                ),
                _menuButton(
                  context,
                  label: 'Asset View',
                  onTap: () => Navigator.pushNamed(context, '/assets'),
                ),
                Stack(
                  clipBehavior: Clip.none,
                  children: [
                    _menuButton(
                      context,
                      label: 'Watchlist',
                      onTap: () => Navigator.pushNamed(context, '/watchlist'),
                    ),
                    Positioned(
                      right: 16,
                      top: -6,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.red,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          '$watchlistBadge',
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _menuButton(BuildContext context, {required String label, required VoidCallback onTap}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: SizedBox(
        width: double.infinity,
        child: OutlinedButton(
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 16),
            textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
          ),
          onPressed: onTap,
          child: Text(label),
        ),
      ),
    );
  }
}
