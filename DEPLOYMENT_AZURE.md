# การ Deploy CivicBlogs ไป Azure App Service

## ขั้นตอนการ Deploy

### 1. เตรียม Azure Resources

#### สร้าง Resource Group
```bash
az group create --name civicblogs-rg --location "Southeast Asia"
```

#### สร้าง App Service Plan
```bash
az appservice plan create \
  --name civicblogs-plan \
  --resource-group civicblogs-rg \
  --sku B1 \
  --is-linux
```

#### สร้าง Web App
```bash
az webapp create \
  --resource-group civicblogs-rg \
  --plan civicblogs-plan \
  --name civicblogs-app \
  --runtime "PYTHON|3.11" \
  --deployment-source-url https://github.com/cabindev/civicblogs.git \
  --deployment-source-branch main
```

### 2. ตั้งค่า Environment Variables

```bash
az webapp config appsettings set \
  --resource-group civicblogs-rg \
  --name civicblogs-app \
  --settings \
    DEBUG=False \
    SECRET_KEY="your-production-secret-key-here" \
    USE_POSTGRES=True \
    SUPABASE_URL="https://beeydumbrvtrllpmmlos.supabase.co" \
    SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
    DATABASE_URL="postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres" \
    ALLOWED_HOSTS="civicblogs-app.azurewebsites.net,www.civicblogs.com" \
    WEBSITE_TIME_ZONE="Asia/Bangkok"
```

### 3. ตั้งค่า Startup Command

```bash
az webapp config set \
  --resource-group civicblogs-rg \
  --name civicblogs-app \
  --startup-file "startup.py && gunicorn --bind=0.0.0.0 --timeout 120 civicblogs.wsgi"
```

### 4. Enable Continuous Deployment

```bash
az webapp deployment source config \
  --resource-group civicblogs-rg \
  --name civicblogs-app \
  --repo-url https://github.com/cabindev/civicblogs.git \
  --branch main \
  --manual-integration
```

## การจัดการผ่าน Azure Portal

### 1. สร้าง Web App ใน Azure Portal

1. เข้าไปที่ [Azure Portal](https://portal.azure.com)
2. สร้าง **Resource Group** ใหม่: `civicblogs-rg`
3. สร้าง **App Service**:
   - **Name**: `civicblogs-app` (หรือชื่ที่ต้องการ)
   - **Runtime**: Python 3.11
   - **Operating System**: Linux
   - **Plan**: Basic B1 หรือมากกว่า

### 2. ตั้งค่า Configuration

ไปที่ **Configuration** > **Application Settings** และเพิ่ม:

| Name | Value |
|------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `your-production-secret-key-here` |
| `USE_POSTGRES` | `True` |
| `SUPABASE_URL` | `https://beeydumbrvtrllpmmlos.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `DATABASE_URL` | `postgresql://postgres.beeydumbrvtrllpmmlos:YY_h025194166@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres` |
| `ALLOWED_HOSTS` | `civicblogs-app.azurewebsites.net` |
| `WEBSITE_TIME_ZONE` | `Asia/Bangkok` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `1` |

### 3. ตั้งค่า Startup Command

ไปที่ **Configuration** > **General Settings**:
- **Startup Command**: `python startup.py && gunicorn --bind=0.0.0.0 --timeout 120 civicblogs.wsgi`

### 4. ตั้งค่า GitHub Actions (แนะนำ)

#### 4.1 ตั้งค่า Azure Secrets ใน GitHub
ไปที่ GitHub Repository > **Settings** > **Secrets and variables** > **Actions** และเพิ่ม:

| Secret Name | Value | วิธีหา |
|------------|-------|-------|
| `AZURE_CLIENT_ID` | `xxx-xxx-xxx` | Azure Portal > App registrations |
| `AZURE_TENANT_ID` | `xxx-xxx-xxx` | Azure Portal > Azure Active Directory |
| `AZURE_SUBSCRIPTION_ID` | `xxx-xxx-xxx` | Azure Portal > Subscriptions |

#### 4.2 สร้าง Service Principal (เพื่อใช้ใน GitHub Actions)
```bash
az ad sp create-for-rbac --name "civicblogs-github-actions" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/civicblogs-rg \
  --sdk-auth
```

#### 4.3 Deploy จาก GitHub

**วิธี 1: GitHub Actions (แนะนำ)**
- ✅ Workflow ถูกสร้างไว้แล้วที่ `.github/workflows/main_civicspace.yml`
- ✅ Auto-deploy ทุกครั้งที่ push ไป `main` branch
- ✅ Build และ test อัตโนมัติ

**วิธี 2: Azure Portal Deployment Center**
ไปที่ **Deployment Center**:
1. เลือก **GitHub**
2. เชื่อมต่อกับ Repository: `cabindev/civicblogs`
3. เลือก Branch: `main`
4. เลือก **GitHub Actions** สำหรับ Build Provider

## การ Monitor และ Debug

### 1. ดู Logs
```bash
az webapp log tail --name civicblogs-app --resource-group civicblogs-rg
```

### 2. SSH เข้า Container
```bash
az webapp ssh --name civicblogs-app --resource-group civicblogs-rg
```

### 3. ตรวจสอบ Application Logs
ไปที่ **Monitoring** > **Log stream** ใน Azure Portal

## Custom Domain (เพิ่มเติม)

### 1. เพิ่ม Custom Domain
```bash
az webapp config hostname add \
  --resource-group civicblogs-rg \
  --webapp-name civicblogs-app \
  --hostname www.civicblogs.com
```

### 2. เปิดใช้ SSL Certificate
```bash
az webapp config ssl bind \
  --resource-group civicblogs-rg \
  --name civicblogs-app \
  --certificate-thumbprint <thumbprint> \
  --ssl-type SNI
```

## การ Scale

### Scale Up (เพิ่ม Resource)
```bash
az appservice plan update \
  --name civicblogs-plan \
  --resource-group civicblogs-rg \
  --sku S1
```

### Scale Out (เพิ่ม Instance)
```bash
az appservice plan update \
  --name civicblogs-plan \
  --resource-group civicblogs-rg \
  --number-of-workers 2
```

## ข้อมูล Database

✅ **Supabase Database**: ยังคงใช้ Supabase เป็น Database ผ่าน API
- URL: `https://beeydumbrvtrllpmmlos.supabase.co`
- Connection: ผ่าน `DATABASE_URL` environment variable
- ไม่ต้องย้าย Database เพิ่มเติม

## หมายเหตุ

- ✅ Static files จัดการโดย WhiteNoise
- ✅ Media files สามารถใช้ Azure Blob Storage ได้ (เพิ่มเติม)
- ✅ Environment variables ปลอดภัยผ่าน Azure App Settings
- ✅ SSL Certificate อัตโนมัติจาก Azure
- ✅ Auto-scaling support

## ต้นทุน (ประมาณการ)

- **App Service B1**: ~฿1,500/เดือน
- **Bandwidth**: ~฿150-500/เดือน (ขึ้นกับ Traffic)
- **Custom Domain SSL**: ฟรี (Azure Managed Certificate)

รวม: **~฿1,650-2,000/เดือน**