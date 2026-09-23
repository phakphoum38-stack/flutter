import unittest

from adapter import RepairRequestError, build_repair_envelope


BASE = {
    "repair_request_id": "rr-001",
    "lineage_id": "lineage-001",
    "base_sha": "0" * 40,
    "head_sha": "1" * 40,
    "file_path": "lib/example.dart",
    "fail_code": "AEOS-FLUTTER-TEST",
    "failure_evidence": "test_example failed at assertion",
    "allowed_files": ["lib/example.dart"],
    "repair_scope": "repair failing test without changing public API",
    "required_checks": ["flutter analyze", "flutter test"],
    "symbol": "Example",
    "line": 42,
    "column": 7,
}


class AdapterTests(unittest.TestCase):
    def test_accepts_scoped_code_repair(self):
        result = build_repair_envelope(BASE)
        self.assertEqual(result["status"], "READY_FOR_FLUTTERFIXCODE")
        self.assertEqual(result["request"]["head_sha"], BASE["head_sha"])
        self.assertEqual(len(result["request_sha256"]), 64)

    def test_rejects_lineage_failure(self):
        raw = {**BASE, "fail_code": "AEOS-LINEAGE-ORPHAN"}
        with self.assertRaisesRegex(RepairRequestError, "NOT-REPAIRABLE"):
            build_repair_envelope(raw)

    def test_rejects_unknown_failure_class(self):
        raw = {**BASE, "fail_code": "AEOS-SOMETHING-UNKNOWN"}
        with self.assertRaisesRegex(RepairRequestError, "UNKNOWN-FAILURE-CLASS"):
            build_repair_envelope(raw)

    def test_rejects_scope_violation(self):
        raw = {**BASE, "file_path": "lib/other.dart"}
        with self.assertRaisesRegex(RepairRequestError, "SCOPE-VIOLATION"):
            build_repair_envelope(raw)

    def test_rejects_missing_evidence(self):
        raw = {**BASE, "failure_evidence": ""}
        with self.assertRaisesRegex(RepairRequestError, "MISSING-EVIDENCE"):
            build_repair_envelope(raw)

    def test_rejects_invalid_sha(self):
        raw = {**BASE, "head_sha": "not-a-sha"}
        with self.assertRaisesRegex(RepairRequestError, "SHA-MISSING-OR-INVALID"):
            build_repair_envelope(raw)

    def test_rejects_same_sha(self):
        raw = {**BASE, "head_sha": BASE["base_sha"]}
        with self.assertRaisesRegex(RepairRequestError, "SHA-NOT-CHANGED"):
            build_repair_envelope(raw)

    def test_rejects_parent_path(self):
        raw = {**BASE, "file_path": "../lib/example.dart"}
        with self.assertRaisesRegex(RepairRequestError, "INVALID-FILE-PATH"):
            build_repair_envelope(raw)


if __name__ == "__main__":
    unittest.main()
