import 'package:flutter/material.dart';
import '../models/alert.dart';
import '../models/host_summary.dart';
import '../models/timeline_event.dart';

/// one alert used on the ALERT and Alert Detail pages
final demoAlert = const Alert(
  severity: 'High',
  srcIp: '192.168.1.5',
  dstIp: '10.0.0.2',
  predictedClass: 'SQL Injection',
  probability: 0.97,
  timestampIso: '2025-09-05T12:30Z',
);

/// watchlist summaries used on Watchlist page
final watchlist = <HostSummary>[
  const HostSummary(
    ip: '192.168.1.10',
    label: '(Windows VM)',
    alerts: 15,
    lastSeen: '10:45 AM',
    topAttacks: ['SSH Brute Force', 'SQL Injection'],
  ),
  const HostSummary(
    ip: '192.168.1.20',
    label: '(Ubuntu Web Server)',
    alerts: 22,
    lastSeen: '11:30 AM',
    topAttacks: ['Port Scan', 'DoS (Slowloris)'],
  ),
  const HostSummary(
    ip: '192.168.1.30',
    label: '(Raspberry Pi IoT device)',
    alerts: 5,
    lastSeen: '1:05 PM',
    topAttacks: ['DNS Exfiltration'],
  ),
];

/// timeline events for the Timeline page
final timeline = <TimelineEvent>[
  const TimelineEvent(
      time: '9/4 9:42 AM',
      label: 'Blue Team ML flags\nanomalous activity',
      color: Colors.blue),
  const TimelineEvent(
      time: '9/4 9:45 AM',
      label: 'Red Team launches nmap\nport scan on Target',
      color: Colors.red),
  const TimelineEvent(
      time: '9/4 9:46 AM',
      label: 'ML raises High Severity\nScan Alert',
      color: Colors.red),
  const TimelineEvent(
      time: '9/4 9:48 AM',
      label: 'Multiple failed SSH logins\ndetected by model',
      color: Colors.red),
];
