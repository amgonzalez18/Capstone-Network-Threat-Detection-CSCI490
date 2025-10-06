import 'package:flutter/material.dart';
import '../data/dummy_data.dart';

class AlertScreen extends StatelessWidget {
  const AlertScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final a = demoAlert;
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('ALERT',
                      style: TextStyle(
                        color: Colors.red.shade600,
                        fontSize: 36,
                        fontWeight: FontWeight.w800,
                        letterSpacing: 2,
                      )),
                  const SizedBox(height: 18),
                  _kv('Severity', a.severity, strongValue: true, valueColor: Colors.red),
                  _kv('Source IP', a.srcIp),
                  _kv('Destination IP', a.dstIp),
                  _kv('Predicted Class', a.predictedClass),
                  _kv('Probability', a.probability.toStringAsFixed(2)),
                  _kv('Time stamp', a.timestampIso),
                  const SizedBox(height: 24),
                  FilledButton(
                    style: FilledButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                    ),
                    onPressed: () => Navigator.pushReplacementNamed(context, '/menu'),
                    child: const Text('NEXT', style: TextStyle(fontSize: 18, letterSpacing: 1)),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _kv(String k, String v, {bool strongValue = false, Color? valueColor}) {
    final base = TextStyle(fontSize: 14, color: Colors.grey.shade700);
    final val = strongValue
        ? base.copyWith(fontWeight: FontWeight.w800, color: valueColor ?? Colors.black)
        : base.copyWith(fontWeight: FontWeight.w600);
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: RichText(
        textAlign: TextAlign.center,
        text: TextSpan(style: base, children: [
          TextSpan(text: '$k: '),
          TextSpan(text: v, style: val),
        ]),
      ),
    );
  }
}
