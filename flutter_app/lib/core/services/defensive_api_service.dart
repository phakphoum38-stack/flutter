import '../api/api_client.dart';
import '../models/execution_request.dart';
import '../models/execution_response.dart';

class DefensiveApiService {
  DefensiveApiService(this._api);
  final ApiClient _api;

  Future<ExecutionResponse> evaluate(ExecutionRequest request) async {
    final json = await _api.postJson('/v1/security/decision', request.toJson());
    return ExecutionResponse.fromJson(json);
  }
}
