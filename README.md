# flutter

## Repository Role

Repository นี้เป็น **เครื่องมือเชื่อมต่อ / Implementation Tooling** ที่แยกออกจาก Repository หลักด้าน Enterprise Architecture โดยตั้งใจให้สามารถพัฒนา ทดสอบ และเปลี่ยนแปลงได้อย่างอิสระ โดยไม่ทำลายเอกสารและ Architecture Contract ของระบบหลัก

### Architecture Boundary

- **Architecture Source of Truth:** `ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`
- **Tooling / Integration / Implementation:** `flutter`
- Repository นี้ **ไม่แทนที่** และ **ไม่เขียนทับ** Architecture Source of Truth
- การเชื่อมต่อระหว่างสอง Repository ต้องผ่าน Contract, Version และ Interface ที่กำหนดไว้อย่างชัดเจน
- สามารถแตก Version / Branch / Implementation ได้โดยไม่กระทบ Version ของ Architecture หลัก

### Upstream Architecture Repository

https://github.com/phakphoum38-stack/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH

### Relationship

```text
ENTERPRISE_API_ARCHITECTURE_LOGIC_TH
        │
        │ Architecture Contract
        │ Version / Interface
        ▼
      flutter
        │
        ├── Integration
        ├── Tooling
        ├── Runtime Support
        └── Implementation
```

หลักการคือ **แยก Architecture ออกจากเครื่องมือ แต่เชื่อมกันด้วย Contract** เพื่อให้ทั้งสอง Repository สามารถพัฒนาเป็นอิสระและยังรักษาความเข้ากันได้ระหว่าง Version ได้
