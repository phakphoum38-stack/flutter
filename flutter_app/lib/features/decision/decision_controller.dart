import '../../core/models/execution_request.dart';
import '../../core/models/execution_response.dart';
import '../../core/services/defensive_api_service.dart';

class DecisionController {
  DecisionController(this._service);
  final DefensiveApiService _service;

  Future<ExecutionResponse> evaluate(ExecutionRequest request) => _service.evaluate(request);
}
