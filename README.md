# flutter

## Repository Role

Repository นี้เป็น **Tooling / Integration / Implementation Workspace** ของระบบหลัก โดยทำงานแยกพื้นที่ตามชุดงานเมื่อจำเป็น และส่งผลลัพธ์กลับเข้าสู่ `main` ของระบบหลักตาม Contract ที่กำหนด

### Source of Truth

- `main` = จุดรวม Source Code และผลลัพธ์ที่ผ่านการรับเข้าแล้ว
- งานที่มีอยู่ใน `main` แล้ว **ห้ามสร้างซ้ำ** โดยไม่มีเหตุผล
- หากงานต้องพัฒนาเฉพาะไฟล์หรือชุดงาน ให้สร้าง Workspace/Branch เฉพาะงานเท่าที่จำเป็น
- Workspace ของแต่ละชุดสามารถทำงาน แก้ไข ทดสอบ และเก็บผลของชุดตัวเองได้
- เมื่อเสร็จแล้วให้ส่ง **Result / Change / Evidence** กลับ `main`

### Architecture Boundary

- **Architecture Source of Truth:** `ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`
- **Tooling / Integration / Implementation:** `flutter`
- Repository นี้ไม่แทนที่และไม่เขียนทับ Architecture Source of Truth
- การเชื่อมต่อระหว่างสอง Repository ต้องผ่าน Contract, Version และ Interface ที่กำหนดไว้อย่างชัดเจน

### Work Model

```text
                    MAIN
                     │
          ┌──────────┴──────────┐
          │                     │
       ชุดงาน 1              ชุดงาน 2
       Workspace             Workspace
          │                     │
       ทำ/Test               ทำ/Test
          │                     │
      Result 1              Result 2
          │                     │
          └──────────┬──────────┘
                     ▼
                    MAIN
                     │
               Final Gate เดียว
                     │
             Project Result
```

### Branch / Workspace Rule

1. ถ้ามีงานอยู่ใน `main` แล้ว ให้ใช้ของเดิม
2. สร้าง Branch/Workspace ใหม่เฉพาะเมื่อจำเป็นต้องทำงานแยกจาก `main`
3. ห้ามสร้าง Repository หรือพื้นที่เก็บผลซ้ำเพียงเพื่อเก็บผลลัพธ์
4. Source Code ยังคงอยู่ใน Workspace/Branch ที่ทำงานนั้น
5. Result และ Evidence ต้องอ้างอิงกลับไปยัง commit / workflow run ที่สร้างผลนั้น
6. งานที่ผ่านการตรวจแล้วจึงส่งกลับ `main`

### Result Contract

ผลจากแต่ละ Workspace ต้องสามารถระบุได้อย่างน้อย:

- ชุดงาน / Owner
- Commit SHA
- Workflow Run
- Test / Validation Status
- Result
- Evidence / Artifact
- Error / Blocker (ถ้ามี)

### Failure / Repair Loop

```text
Workspace
   │
   ▼
 Test / Validation
   │
   ├── PASS ──► Result ──► MAIN
   │
   └── FAIL ──► Diagnose / Repair ──► Test ใหม่
                                      │
                                      ▼
                                    MAIN
                                      │
                               Final Gate เดียว
```

### Upstream Architecture Repository

https://github.com/phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH

หลักการคือ **ทำงานแยกเมื่อจำเป็น เก็บผลของตัวเอง และส่ง Result กลับ `main` โดยไม่สร้างโครงสร้างซ้ำ** ขณะที่ทุกชุดงานสุดท้ายต้องผ่าน **Final Gate เดียว**