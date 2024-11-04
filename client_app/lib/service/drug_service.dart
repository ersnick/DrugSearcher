import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>?> getDrugInfo(String name) async {
  final url = Uri.parse('http://b257-188-17-211-72.ngrok-free.app/v1/drug/$name');

  try {
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final decodedBody = utf8.decode(response.bodyBytes);
      return jsonDecode(decodedBody);
    } else {
      print("Error: ${response.statusCode}");
      return null;
    }
  } catch (e) {
    print("Failed to fetch drug info : $e");
    return null;
  }
}