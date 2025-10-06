class Alert {
  final String severity;
  final String srcIp;
  final String dstIp;
  final String predictedClass;
  final double probability;
  final String timestampIso;

  const Alert({
    required this.severity,
    required this.srcIp,
    required this.dstIp,
    required this.predictedClass,
    required this.probability,
    required this.timestampIso,
  });
}
