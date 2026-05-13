class AlertModel {
  final String srcIp;
  final String dstIp;
  final String prediction;
  final String attackType;
  final double confidence;
  final DateTime timestamp;

  AlertModel({
    required this.srcIp,
    required this.dstIp,
    required this.prediction,
    required this.attackType,
    required this.confidence,
    required this.timestamp,
  });

  static DateTime _parseTimestamp(dynamic value) {
    if (value == null) {
      return DateTime.now();
    }

    if (value is DateTime) {
      return value;
    }

    if (value is String) {
      return DateTime.tryParse(value) ?? DateTime.now();
    }

    return value.toDate();
  }

  factory AlertModel.fromFirestore(Map<String, dynamic> data) {
    return AlertModel(
      srcIp: data['src_ip'] ?? '',
      dstIp: data['dst_ip'] ?? '',
      prediction: data['prediction'] ?? '',
      attackType: data['attack_type'] ?? '',
      confidence: (data['confidence'] ?? 0).toDouble(),
      timestamp: _parseTimestamp(data['timestamp']),
    );
  }
}