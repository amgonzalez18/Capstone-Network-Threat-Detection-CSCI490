import 'package:flutter/material.dart';
import '../data/dummy_data.dart';

class TimelineScreen extends StatelessWidget {
  const TimelineScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Timeline View')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: timeline.length,
        itemBuilder: (context, i) {
          final e = timeline[i];
          final isLast = i == timeline.length - 1;
          return Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(
                width: 72,
                child: Column(
                  children: [
                    Text(e.time, textAlign: TextAlign.center,
                        style: const TextStyle(fontSize: 12, color: Colors.blueGrey)),
                    const SizedBox(height: 6),
                    Container(width: 12, height: 12,
                        decoration: BoxDecoration(color: e.color, shape: BoxShape.circle)),
                    if (!isLast)
                      Container(width: 2, height: 60, color: Colors.blueGrey.shade200),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Container(
                  margin: const EdgeInsets.only(bottom: 12),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade100,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.grey.shade300),
                  ),
                  child: Text(e.label),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
