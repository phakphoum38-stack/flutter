# Runner Protocol Contract

Runner เป็น Data Plane executor ที่รับ Execution Plan ซึ่งถูก resolve และ snapshot แล้ว

## Required identity

- `runner_id`
- `protocol_version`
- `capabilities`
- `execution_id`
- `attempt_id`
- `assignment_id`
- `fencing_token`

## Capability matching

Runner ต้องประกาศ capability อย่างน้อย:

```yaml
protocol_version: 1
os: linux
arch: amd64
executor: container
runtime:
  python: "3.12"
  node: "22"
resources:
  cpu: 8
  memory_mb: 16384
gpu: false
features:
  - artifact-upload
  - log-stream
```

Scheduler ต้องตรวจ requirement ของ Execution Plan กับ capability ก่อน assignment

## Ownership

Assignment ใช้ Lease + Fencing Token

```text
Runner A token=10
Runner B token=11

A กลับมาหลัง lease หมดอายุ
→ stale token
→ write rejected
→ stop execution
```

Runner เก่าไม่มีสิทธิ์เขียนทับ Owner ใหม่ใน Execution เดียวกัน

## Compatibility

Runner protocol และ capability เป็น versioned contract

- non-breaking capability เพิ่มได้
- breaking protocol ต้องเพิ่ม major version
- Scheduler ต้องไม่ส่งงานให้ Runner ที่ไม่รองรับ protocol ที่ Plan ต้องการ
