import 'package:flutter_test/flutter_test.dart';
import '../lib/core/models/execution_request.dart';

void main() {
  test('execution request contains only server-evaluated inputs', () {
    const request = ExecutionRequest(
      deviceId: 'device-1',
      serviceId: 'research-service',
      action: 'evaluate',
    );
    expect(request.toJson(), {
      'device_id': 'device-1',
      'service_id': 'research-service',
      'action': 'evaluate',
    });
    expect(request.toJson().containsKey('authorization'), isFalse);
    expect(request.toJson().containsKey('decision'), isFalse);
  });
}
