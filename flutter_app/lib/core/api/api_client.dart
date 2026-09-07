import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_exception.dart';

class ApiClient {
  ApiClient({required this.baseUrl, http.Client? client}) : _client = client ?? http.Client();
  final String baseUrl;
  final http.Client _client;

  Future<Map<String, dynamic>> postJson(String path, Map<String, dynamic> body) async {
    final response = await _client.post(
      Uri.parse('$baseUrl$path'),
      headers: const {'content-type': 'application/json', 'accept': 'application/json'},
      body: jsonEncode(body),
    );
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw ApiException(response.body.isEmpty ? 'API request failed' : response.body, statusCode: response.statusCode);
    }
    final decoded = jsonDecode(response.body);
    if (decoded is! Map<String, dynamic>) throw const ApiException('Invalid API response');
    return decoded;
  }
}
