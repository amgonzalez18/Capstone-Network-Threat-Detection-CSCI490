import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/alert_model.dart';

class FirestoreService {
  final CollectionReference alerts =
      FirebaseFirestore.instance.collection('alerts');

  Stream<List<AlertModel>> getAlerts() {
    return alerts
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map((doc) {
        return AlertModel.fromFirestore(
            doc.data() as Map<String, dynamic>);
      }).toList();
    });
  }
}