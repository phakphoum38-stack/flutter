import 'package:flutter_test/flutter_test.dart';
import 'package:myapp/main.dart';

void main() {
  testWidgets('tooling app renders the build/test gate', (tester) async {
    await tester.pumpWidget(const ToolingApp());

    expect(find.text('Flutter Tooling'), findsOneWidget);
    expect(find.text('Build/Test Gate'), findsOneWidget);
  });
}
