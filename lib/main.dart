import 'package:flutter/material.dart';

// screens
import 'screens/alert_screen.dart';
import 'screens/menu_screen.dart';
import 'screens/watchlist_screen.dart';
import 'screens/timeline_screen.dart';
import 'screens/asset_view_screen.dart';

void main() => runApp(const SOCApp());

class SOCApp extends StatelessWidget {
  const SOCApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SOC Dashboard (Mock)',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.blue,
        brightness: Brightness.light,
      ),
      routes: {
        '/': (_) => const AlertScreen(),     // first screen
        '/menu': (_) => const MenuScreen(),  // main menu
        '/watchlist': (_) => const WatchlistScreen(),
        '/timeline': (_) => const TimelineScreen(),
        '/assets': (_) => const AssetViewScreen(),
        // '/alertDetail': (_) => ...  // (removed for now)
      },
    );
  }
}
