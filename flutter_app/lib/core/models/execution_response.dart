class ExecutionResponse {
  const ExecutionResponse({required this.decision, this.reason, this.correlationId});
  final String decision;
  final String? reason;
  final String? correlationId;
  factory ExecutionResponse.fromJson(Map<String, dynamic> json) => ExecutionResponse(
    decision: (json['decision'] ?? 'DENY').toString(),
    reason: json['reason']?.toString(),
    correlationId: json['correlation_id']?.toString(),
  );
}
