# CivicBlogs Supabase Deployment Guide

## Overview
This guide walks you through deploying CivicBlogs with Supabase PostgreSQL database and Row Level Security (RLS).

## Prerequisites
- Supabase account and project
- Your Supabase project credentials:
  - Project URL: `https://beeydumbrvtrllpmmlos.supabase.co`
  - Database password: `YY_h025194166`
  - API Key (anon): `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

## Step 1: Database Setup

### 1.1 Access Supabase SQL Editor
1. Go to your Supabase project dashboard
2. Navigate to "SQL Editor" in the left sidebar
3. Create a new query

### 1.2 Execute Schema Creation
1. Copy the contents of `supabase_schema.sql`
2. Paste into the SQL editor
3. Click "Run" to create all tables and initial policies
4. Verify all tables are created successfully

### 1.3 Apply Advanced Policies
1. Copy the contents of `supabase_policies.sql`
2. Paste into a new SQL query
3. Execute to add advanced security policies
4. Check for any errors in the logs

### 1.4 Verify RLS Status
```sql
-- Check that RLS is enabled on all tables
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;
```

## Step 2: Django Configuration

### 2.1 Update Database Settings
Update your `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YY_h025194166@db.beeydumbrvtrllpmmlos.supabase.co:5432/postgres

# Supabase Configuration  
SUPABASE_URL=https://beeydumbrvtrllpmmlos.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlZXlkdW1icnZ0cmxscG1tbG9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY5NTc2NzUsImV4cCI6MjA3MjUzMzY3NX0.ObDXuAjF_cGk6ASGNQIzbtZ4mW15nyyU8inaRaNPtqE
```

### 2.2 Install Additional Dependencies
```bash
pip install dj-database-url psycopg2-binary
```

## Step 3: Authentication Setup

### 3.1 Enable Authentication in Supabase
1. Go to Authentication → Settings
2. Enable email authentication
3. Configure email templates
4. Set up redirect URLs for your application

### 3.2 Create Admin User
Execute in Supabase SQL Editor:
```sql
-- Insert admin user profile (after user signs up via Supabase Auth)
INSERT INTO profiles (id, username, full_name, role, is_active)
VALUES (
  'your-auth-user-uuid-here', -- Get this from auth.users table
  'admin',
  'Admin User',
  'admin',
  true
);
```

## Step 4: Content Setup

### 4.1 Create Initial Categories
```sql
INSERT INTO categories (name, slug, description, color) VALUES
('เทคโนโลยี', 'technology', 'ข่าวสารและบทความเกี่ยวกับเทคโนโลยี', '#3b82f6'),
('การเมือง', 'politics', 'ข่าวการเมืองและประชาธิปไตย', '#ef4444'),
('สังคม', 'society', 'ประเด็นสังคมและการใช้ชีวิต', '#10b981'),
('สิ่งแวดล้อม', 'environment', 'ปัญหาสิ่งแวดล้อมและการอนุรักษ์', '#22c55e');
```

### 4.2 Create Sample Tags
```sql
INSERT INTO tags (name, slug, description) VALUES
('ข่าวสาร', 'news', 'ข่าวสารทั่วไป'),
('เทคโนโลยี', 'technology', 'เทคโนโลยีและนวัตกรรม'),
('สังคม', 'society', 'ประเด็นทางสังคม'),
('การศึกษา', 'education', 'การศึกษาและการเรียนรู้');
```

## Step 5: Security Configuration

### 5.1 Verify RLS Policies
Test the policies with different user roles:

```sql
-- Test as anonymous user (should only see published content)
SET ROLE anon;
SELECT * FROM posts WHERE status = 'published';

-- Test as authenticated user
SET ROLE authenticated;
SELECT * FROM posts WHERE author_id = auth.uid();
```

### 5.2 Configure API Keys
- **Anon Key**: Use for client-side operations (public data only)
- **Service Role Key**: Use for server-side operations (full access)
- **Never expose service role key** in client-side code

## Step 6: File Storage Setup

### 6.1 Configure Supabase Storage
1. Go to Storage in Supabase dashboard
2. Create buckets:
   - `blog-images` (for featured images)
   - `media-files` (for general uploads)
3. Set up storage policies:

```sql
-- Policy for blog images bucket
CREATE POLICY "Anyone can view blog images" ON storage.objects
FOR SELECT USING (bucket_id = 'blog-images');

CREATE POLICY "Authenticated users can upload blog images" ON storage.objects
FOR INSERT WITH CHECK (
  bucket_id = 'blog-images' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

### 6.2 Update Django Media Settings
```python
# In settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.supabase.SupabaseStorage'
SUPABASE_STORAGE_BUCKET = 'blog-images'
```

## Step 7: Testing and Validation

### 7.1 Test Database Connection
```bash
python manage.py check --database default
```

### 7.2 Run Migrations (if using Django models)
```bash
python manage.py migrate
```

### 7.3 Test RLS Policies
Create test queries to verify:
- Anonymous users can only read published content
- Authors can only edit their own posts
- Admins have elevated permissions

## Step 8: Performance Optimization

### 8.1 Database Indexes
The schema includes optimized indexes for:
- Post queries (status, publication date, category)
- Comment queries (post association, approval status)
- Search functionality (text search, tag filtering)

### 8.2 Connection Pooling
For production, consider using:
```env
DATABASE_URL=postgresql://postgres:password@pooler.supabase.co:6543/postgres
```

### 8.3 Real-time Subscriptions
Enable real-time for dynamic updates:
```javascript
// Example client-side subscription
const subscription = supabase
  .from('posts')
  .on('*', (payload) => {
    console.log('Change received!', payload)
  })
  .subscribe()
```

## Step 9: Monitoring and Maintenance

### 9.1 Set Up Monitoring
- Monitor database performance in Supabase dashboard
- Set up alerts for connection limits
- Track slow queries and optimize as needed

### 9.2 Backup Strategy
- Supabase provides automated backups
- Consider additional backup strategies for critical data
- Test restore procedures regularly

### 9.3 Security Auditing
```sql
-- Regular security audit queries
SELECT * FROM audit_logs WHERE created_at > NOW() - INTERVAL '7 days';

-- Check for unusual access patterns
SELECT event_type, COUNT(*) 
FROM analytics 
WHERE created_at > NOW() - INTERVAL '1 day'
GROUP BY event_type;
```

## Troubleshooting

### Common Issues

1. **Connection Issues**
   - Verify database URL and credentials
   - Check IP allowlist in Supabase settings
   - Confirm SSL requirements

2. **Permission Denied Errors**
   - Verify RLS policies are correctly configured
   - Check user roles and authentication state
   - Review policy conditions for edge cases

3. **Performance Issues**
   - Analyze query performance in Supabase dashboard
   - Add missing indexes for frequently queried columns
   - Consider policy optimization for complex conditions

### Useful Queries

```sql
-- Check RLS policy usage
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public';

-- Monitor active connections
SELECT count(*) as active_connections 
FROM pg_stat_activity 
WHERE state = 'active';

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals,
    most_common_freqs,
    histogram_bounds,
    correlation
FROM pg_stats
WHERE schemaname = 'public';
```

## Production Checklist

- [ ] All RLS policies tested and verified
- [ ] Admin user created and roles assigned
- [ ] Storage buckets configured with proper policies
- [ ] Environment variables secured
- [ ] Backup and monitoring set up
- [ ] Performance testing completed
- [ ] Security audit passed
- [ ] Documentation updated

## Support

For issues:
1. Check Supabase logs in dashboard
2. Review Django debug output
3. Consult Supabase documentation
4. Contact support via official channels

---

**Security Note**: Always follow the principle of least privilege. Grant users only the minimum permissions necessary for their role.