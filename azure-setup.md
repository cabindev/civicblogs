# Azure Service Principal Setup for GitHub Actions

## ขั้นตอนการตั้งค่า Azure Secrets

### 1. เปิด Azure Cloud Shell
1. ไปที่ [Azure Portal](https://portal.azure.com)
2. คลิกไอคอน Cloud Shell ที่มุมขวาบน (>_)
3. เลือก **Bash**

### 2. สร้าง Service Principal
รันคำสั่งนี้ใน Azure Cloud Shell:

```bash
# แทนที่ {subscription-id} ด้วย Subscription ID จริง
az ad sp create-for-rbac \
  --name "civicblogs-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/civicblogs-rg \
  --json-auth
```

### 3. หา Subscription ID
```bash
az account show --query id --output tsv
```

### 4. หา Tenant ID  
```bash
az account show --query tenantId --output tsv
```

## ผลลัพธ์ที่จะได้

จากคำสั่งใน step 2 จะได้ JSON แบบนี้:
```json
{
  "clientId": "12345678-1234-1234-1234-123456789012",
  "clientSecret": "your-client-secret-here",
  "subscriptionId": "12345678-1234-1234-1234-123456789012", 
  "tenantId": "12345678-1234-1234-1234-123456789012"
}
```

## นำข้อมูลไปใส่ใน GitHub Secrets

1. ไปที่ GitHub Repository: https://github.com/cabindev/civicblogs
2. Settings → Secrets and variables → Actions
3. คลิก "New repository secret" และเพิ่ม:

| Secret Name | Value จาก JSON |
|------------|----------------|
| `AZURE_CLIENT_ID` | `clientId` |
| `AZURE_CLIENT_SECRET` | `clientSecret` |  
| `AZURE_SUBSCRIPTION_ID` | `subscriptionId` |
| `AZURE_TENANT_ID` | `tenantId` |

## ตรวจสอบการตั้งค่า

เมื่อตั้งค่าเสร็จ ใน GitHub Repository ควรมี Secrets 4 ตัว:
- ✅ AZURE_CLIENT_ID
- ✅ AZURE_CLIENT_SECRET  
- ✅ AZURE_SUBSCRIPTION_ID
- ✅ AZURE_TENANT_ID

## ทดสอบ Auto-Deployment

1. แก้ไขไฟล์อะไรก็ได้ (เช่น README.md)
2. Commit และ Push:
   ```bash
   git add .
   git commit -m "Test auto deployment"
   git push origin main
   ```
3. ไปดู GitHub Actions tab ว่า workflow รันหรือไม่
4. รอ 3-5 นาที website จะอัพเดต!

## หมายเหตุ

- Service Principal จะมีสิทธิ์ contributor ใน Resource Group เท่านั้น
- ถ้าไม่มี Resource Group civicblogs-rg ให้สร้างก่อน
- GitHub Actions จะรันอัตโนมัติทุกครั้งที่ push ไป main branch