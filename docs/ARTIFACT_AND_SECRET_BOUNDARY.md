# Artifact and Secret Boundary

## Artifacts

Artifact เป็น first-class object และต้องมี durable ownership แยกจาก Runner

```text
Runner
  │
  ▼
Artifact Store
  │
  ├── artifact_id
  ├── execution_id
  ├── attempt_id
  ├── digest
  ├── size
  └── metadata
```

Runner ตายแล้ว Artifact ต้องยังเข้าถึงได้ตาม retention policy

## Secrets

Workflow ใช้ Secret Reference ไม่ใช่ plaintext secret

```text
Workflow
  │
  ▼
secret_ref
  │
  ▼
Secret Provider
  │
  ▼
Runner
```

ห้าม plaintext secret ปรากฏใน:

- Workflow Definition
- Execution Snapshot
- Queue payload
- Event payload
- Logs
- Error message
- Artifact metadata

ระบบควรมี secret redaction ที่ log boundary และห้ามส่ง secret ผ่าน event ที่ไม่จำเป็น
