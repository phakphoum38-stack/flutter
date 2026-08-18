# Architecture Boundary

`flutter` เป็น Tooling / Integration / Implementation Repository แยกจาก Architecture Source of Truth

Upstream:
`https://github.com/phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`

## Contract Pin

Current foundation contract:

```text
anef-core-contract: 0.1.0
```

Implementation ต้องระบุ Contract Version ที่รองรับ และห้ามตีความ Architecture โดยอาศัย convention ที่ไม่ได้อยู่ใน Contract

## Control Plane / Data Plane

```text
CONTROL PLANE
  API
  Workflow
  Version
  Policy
  Scheduler
       │
       ▼
DATA PLANE
  Queue
  Runner
  Execution
  Logs
  Artifacts
```

Control Plane สร้างและจัดการ Execution Plan ส่วน Data Plane ทำการส่งมอบและ execute ตาม Plan ที่ถูก pin แล้ว

## Execution Contract

```text
Workflow Definition
        │ resolve
        ▼
Execution Plan
        │ snapshot
        ▼
Execution Snapshot
        │
        ▼
Execution (pinned workflow_version_id)
```

Runner ไม่ควร resolve Workflow Definition ใหม่เองระหว่าง execution

## Runner Contract

Runner ต้องประกาศ:

- protocol version
- OS / architecture
- executor type
- runtime versions
- CPU / memory / GPU capability
- feature capabilities

Scheduler ต้องตรวจ compatibility ก่อน assignment

## Artifact / Secret Boundary

Artifact เป็น first-class reference ที่เก็บใน durable storage ไม่ผูกกับ lifecycle ของ Runner

Secret ต้องเป็น reference ไปยัง Secret Provider และห้ามใส่ plaintext secret ลง Workflow Definition, Event, Snapshot หรือ Log
