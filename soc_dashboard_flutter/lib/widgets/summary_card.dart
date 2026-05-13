import 'package:flutter/material.dart';

class SummaryCard extends StatelessWidget {
  final String title;
  final int count;
  final IconData icon;

  const SummaryCard({
    super.key,
    required this.title,
    required this.count,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.all(8),
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.grey[900],
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Icon(icon, size: 30, color: Colors.white),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: Colors.white70)),
                Text(
                  count.toString(),
                  style: const TextStyle(fontSize: 22, color: Colors.white),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}