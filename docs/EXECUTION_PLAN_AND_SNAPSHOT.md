# Execution Plan and Snapshot

## Rule

Workflow Definition และ Runtime Execution เป็นคนละ boundary

```text
Workflow Version
      │
      │ resolve
      ▼
Execution Plan
      │
      │ snapshot
      ▼
Execution Snapshot
      │
      ▼
Execution
```

Execution ต้อง pin:

- `workflow_id`
- `workflow_version_id`
- `contract_version`
- `snapshot_id`
- `trace_id`

## Reproducibility

Execution Snapshot ต้องเก็บ resolved values ที่จำเป็นต่อการ execute เช่น:

- DAG / dependencies
- resolved step definitions
- retry policy
- timeout policy
- runner requirements
- environment references
- artifact references

ไม่ควรเก็บ plaintext secrets ใน snapshot

## Immutability

เมื่อ Execution เริ่มแล้ว Snapshot ห้ามถูกแก้เพื่อเปลี่ยนความหมายของ execution เดิม

การเปลี่ยน Workflow ต้องสร้าง Version ใหม่และสร้าง Execution ใหม่
