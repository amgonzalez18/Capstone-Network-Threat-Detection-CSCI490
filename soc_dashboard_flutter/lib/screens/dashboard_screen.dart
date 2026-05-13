import 'package:flutter/material.dart';
import '../models/alert_model.dart';
import '../services/firestore_service.dart';
import '../widgets/summary_card.dart';

class DashboardScreen extends StatelessWidget {
  DashboardScreen({super.key});

  final FirestoreService _firestoreService = FirestoreService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text("Network Threat Detection SOC Dashboard"),
        backgroundColor: Colors.black,
      ),
      body: StreamBuilder<List<AlertModel>>(
        stream: _firestoreService.getAlerts(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }

          if (snapshot.hasError) {
            return Center(
              child: Text(
                "Error loading alerts: ${snapshot.error}",
                style: const TextStyle(color: Colors.redAccent),
              ),
            );
          }

          final alerts = snapshot.data ?? [];

          final total = alerts.length;
          final attacks =
              alerts.where((alert) => alert.prediction == "attack").length;
          final benign =
              alerts.where((alert) => alert.prediction == "benign").length;

          return Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
              
              LayoutBuilder(
  builder: (context, constraints) {
    final isSmallScreen = constraints.maxWidth < 700;

    final cards = [
      SummaryCard(
        title: "Total Flows",
        count: total,
        icon: Icons.storage,
      ),
      SummaryCard(
        title: "Attacks",
        count: attacks,
        icon: Icons.warning,
      ),
      SummaryCard(
        title: "Benign",
        count: benign,
        icon: Icons.check_circle,
      ),
    ];

    if (isSmallScreen) {
      return Column(
        children: cards
            .map(
              (card) => Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: card,
              ),
            )
            .toList(),
      );
    }

    return Row(
      children: cards
          .map(
            (card) => Expanded(
              child: Padding(
                padding: const EdgeInsets.only(right: 12),
                child: card,
              ),
            ),
          )
          .toList(),
    );
  },
),
                const SizedBox(height: 20),
                Expanded(
                  child: Card(
                    color: Colors.grey[900],
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            "Recent Alerts",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 12),
                          Expanded(
                            child: alerts.isEmpty
                                ? const Center(
                                    child: Text(
                                      "No alerts found in Firestore.",
                                      style: TextStyle(color: Colors.white70),
                                    ),
                                  )
                                : ListView.builder(
                                    itemCount: alerts.length,
                                    itemBuilder: (context, index) {
                                      final alert = alerts[index];
                                      final isAttack =
                                          alert.prediction == "attack";

                                      return Card(
                                        color: isAttack
                                            ? Colors.red.withOpacity(0.25)
                                            : Colors.green.withOpacity(0.25),
                                        child: ListTile(
                                          leading: Icon(
                                            isAttack
                                                ? Icons.security
                                                : Icons.check_circle,
                                            color: isAttack
                                                ? Colors.redAccent
                                                : Colors.greenAccent,
                                          ),
                                          title: Text(
                                            alert.attackType,
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                          subtitle: Text(
                                            "Time: ${alert.timestamp}\n${alert.srcIp} → ${alert.dstIp}",
                                            style: const TextStyle(
                                              color: Colors.white70,
                                            ),
                                          ),
                                          trailing: Column(
                                            mainAxisAlignment:
                                                MainAxisAlignment.center,
                                            crossAxisAlignment:
                                                CrossAxisAlignment.end,
                                            children: [
                                              Text(
                                                alert.prediction,
                                                style: TextStyle(
                                                  color: isAttack
                                                      ? Colors.redAccent
                                                      : Colors.greenAccent,
                                                  fontWeight: FontWeight.bold,
                                                ),
                                              ),
                                              Text(
                                                "${alert.confidence}%",
                                                style: const TextStyle(
                                                  color: Colors.white70,
                                                ),
                                              ),
                                            ],
                                          ),
                                        ),
                                      );
                                    },
                                  ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}