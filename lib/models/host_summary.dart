class HostSummary {
  final String ip;
  final String label;
  final int alerts;
  final String lastSeen;
  final List<String> topAttacks;

  const HostSummary({
    required this.ip,
    required this.label,
    required this.alerts,
    required this.lastSeen,
    required this.topAttacks,
  });
}
