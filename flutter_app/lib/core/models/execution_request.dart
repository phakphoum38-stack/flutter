class ExecutionRequest {
  const ExecutionRequest({required this.deviceId, required this.serviceId, required this.action});
  final String deviceId;
  final String serviceId;
  final String action;
  Map<String, dynamic> toJson() => {'device_id': deviceId, 'service_id': serviceId, 'action': action};
}
