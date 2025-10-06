import 'package:flutter/material.dart';
import '../data/dummy_data.dart';

class WatchlistScreen extends StatelessWidget {
  const WatchlistScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Watchlist')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: watchlist.length,
        itemBuilder: (context, i) {
          final h = watchlist[i];
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('${h.ip} ${h.label}',
                    style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                const SizedBox(height: 8),
                _bullet('Alerts: ${h.alerts}'),
                _bullet('Last Seen: ${h.lastSeen}'),
                _bullet('Top Attacks: ${h.topAttacks.join(", ")}'),
              ]),
            ),
          );
        },
      ),
    );
  }

  Widget _bullet(String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('•  ', style: TextStyle(fontSize: 18)),
          Expanded(child: Text(text)),
        ],
      ),
    );
  }
}
