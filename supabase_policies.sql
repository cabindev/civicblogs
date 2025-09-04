-- CivicBlogs Row Level Security Policies
-- Run this after creating the main schema

-- ============================================================================
-- ADVANCED SECURITY POLICIES
-- ============================================================================

-- Policy for viewing draft posts (only authors and editors)
create policy "Authors can view draft posts" on posts
    for select using (
        status = 'draft' and (
            auth.uid() = author_id or
            exists (
                select 1 from profiles 
                where id = auth.uid() and role in ('admin', 'editor')
            )
        )
    );

-- Policy for scheduled posts
create policy "Scheduled posts are visible when published" on posts
    for select using (
        status = 'scheduled' and 
        scheduled_at <= now() and
        visibility = 'public'
    );

-- Policy for password protected posts (will be handled in application layer)
create policy "Password protected posts need verification" on posts
    for select using (
        visibility = 'password' and
        status = 'published' and
        (
            -- This will be handled in application logic
            -- Users need to provide correct password
            auth.uid() = author_id or
            exists (
                select 1 from profiles 
                where id = auth.uid() and role in ('admin', 'editor')
            )
        )
    );

-- ============================================================================
-- COMMENT MODERATION POLICIES
-- ============================================================================

-- Policy for comment approval (auto-approve for trusted users)
create policy "Auto-approve comments from trusted users" on comments
    for insert with check (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor', 'author')
        )
    );

-- Policy for nested comments (replies)
create policy "Can reply to approved comments" on comments
    for insert with check (
        parent_id is null or
        exists (
            select 1 from comments 
            where id = parent_id and is_approved = true
        )
    );

-- ============================================================================
-- ENHANCED ANALYTICS POLICIES
-- ============================================================================

-- Policy for tracking user interactions
create policy "Track authenticated user events" on analytics
    for insert with check (
        (user_id = auth.uid() and auth.uid() is not null) or
        (user_id is null) -- anonymous tracking
    );

-- Policy for viewing own analytics
create policy "Users can view their own analytics" on analytics
    for select using (
        user_id = auth.uid() or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- ============================================================================
-- CONTENT MANAGEMENT POLICIES
-- ============================================================================

-- Policy for featured posts (only editors and admins)
create policy "Only editors can feature posts" on posts
    for update using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    ) with check (
        -- Only allow updating featured status if user is editor/admin
        not (old.is_featured != new.is_featured) or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Policy for pinned posts (only admins)
create policy "Only admins can pin posts" on posts
    for update using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    ) with check (
        not (old.is_pinned != new.is_pinned) or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- ============================================================================
-- USER ROLE MANAGEMENT POLICIES
-- ============================================================================

-- Policy for role changes (only admins can change roles)
create policy "Only admins can change user roles" on profiles
    for update using (
        auth.uid() = id and old.role = new.role -- users can update other fields
    ) with check (
        (old.role = new.role) or -- role didn't change
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- Policy for deactivating users (only admins)
create policy "Only admins can deactivate users" on profiles
    for update using (
        auth.uid() = id and old.is_active = new.is_active -- user can't change their active status
    ) with check (
        (old.is_active = new.is_active) or -- status didn't change
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- ============================================================================
-- MEDIA MANAGEMENT POLICIES
-- ============================================================================

-- Policy for media file access based on post visibility
create policy "Media files follow post visibility" on media_files
    for select using (
        -- Always allow if user is authenticated and is uploader or admin
        (
            auth.uid() = uploaded_by or
            exists (
                select 1 from profiles 
                where id = auth.uid() and role in ('admin', 'editor')
            )
        ) or
        -- Or if the media is used in a published post
        exists (
            select 1 from posts 
            where featured_image_url = media_files.file_path 
            and status = 'published' 
            and visibility = 'public'
        )
    );

-- ============================================================================
-- NEWSLETTER MANAGEMENT POLICIES
-- ============================================================================

-- Policy for newsletter subscription management
create policy "Users can manage their newsletter subscription" on newsletter_subscribers
    for update using (
        -- Users can update their own subscription using email verification
        -- This will be handled in application logic with proper tokens
        true
    ) with check (
        -- Only allow updating status and verification fields
        old.email = new.email -- email cannot be changed
    );

-- ============================================================================
-- AUDIT AND LOGGING POLICIES
-- ============================================================================

-- Create audit log table for sensitive operations
create table audit_logs (
    id uuid default uuid_generate_v4() primary key,
    table_name text not null,
    operation text not null,
    old_values jsonb,
    new_values jsonb,
    user_id uuid references profiles(id) on delete set null,
    ip_address inet,
    user_agent text,
    created_at timestamptz default now()
);

-- Enable RLS on audit_logs
alter table audit_logs enable row level security;

-- Audit logs policies (only admins can view)
create policy "Only admins can view audit logs" on audit_logs
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- ============================================================================
-- FUNCTIONS FOR COMPLEX POLICIES
-- ============================================================================

-- Function to check if user can moderate content
create or replace function can_moderate()
returns boolean as $$
begin
    return exists (
        select 1 from profiles 
        where id = auth.uid() and role in ('admin', 'editor')
    );
end;
$$ language plpgsql security definer;

-- Function to check if user is content author
create or replace function is_content_author(content_author_id uuid)
returns boolean as $$
begin
    return auth.uid() = content_author_id;
end;
$$ language plpgsql security definer;

-- Function to check if post is publicly accessible
create or replace function is_post_public(post_row posts)
returns boolean as $$
begin
    return post_row.status = 'published' 
           and post_row.visibility = 'public' 
           and (post_row.published_at is null or post_row.published_at <= now());
end;
$$ language plpgsql;

-- ============================================================================
-- PERFORMANCE OPTIMIZATION POLICIES
-- ============================================================================

-- Create partial indexes for better performance
create index concurrently posts_public_published_idx on posts(published_at desc) 
where status = 'published' and visibility = 'public';

create index concurrently comments_approved_by_post_idx on comments(post_id, created_at desc) 
where is_approved = true and is_spam = false;

create index concurrently profiles_active_users_idx on profiles(created_at desc) 
where is_active = true;

-- ============================================================================
-- SECURITY FUNCTIONS FOR APPLICATION USE
-- ============================================================================

-- Function to safely increment view count
create or replace function increment_post_views(post_uuid uuid)
returns void as $$
begin
    -- Only increment if post is published and public
    update posts 
    set view_count = view_count + 1 
    where id = post_uuid 
      and status = 'published' 
      and visibility = 'public';
      
    -- Log the view for analytics
    insert into analytics (post_id, event_type, user_id, created_at)
    values (post_uuid, 'view', auth.uid(), now());
end;
$$ language plpgsql security definer;

-- Function to safely like a post
create or replace function toggle_post_like(post_uuid uuid)
returns boolean as $$
declare
    like_exists boolean;
begin
    -- Check if user already liked this post
    select exists(
        select 1 from analytics 
        where post_id = post_uuid 
          and event_type = 'like' 
          and user_id = auth.uid()
    ) into like_exists;
    
    if like_exists then
        -- Remove like
        delete from analytics 
        where post_id = post_uuid 
          and event_type = 'like' 
          and user_id = auth.uid();
        update posts set like_count = like_count - 1 where id = post_uuid;
        return false;
    else
        -- Add like
        insert into analytics (post_id, event_type, user_id, created_at)
        values (post_uuid, 'like', auth.uid(), now());
        update posts set like_count = like_count + 1 where id = post_uuid;
        return true;
    end if;
end;
$$ language plpgsql security definer;

-- ============================================================================
-- WEBHOOK AND REAL-TIME POLICIES
-- ============================================================================

-- Enable real-time for public content
alter publication supabase_realtime add table posts;
alter publication supabase_realtime add table comments;
alter publication supabase_realtime add table categories;

-- Real-time policies will follow the same RLS rules

-- ============================================================================
-- BACKUP AND RECOVERY CONSIDERATIONS
-- ============================================================================

-- Create a function to export user data (GDPR compliance)
create or replace function export_user_data(user_uuid uuid)
returns jsonb as $$
declare
    user_data jsonb;
begin
    -- Only allow users to export their own data or admins
    if auth.uid() != user_uuid and not can_moderate() then
        raise exception 'Unauthorized';
    end if;
    
    select jsonb_build_object(
        'profile', to_jsonb(p.*),
        'posts', (
            select jsonb_agg(to_jsonb(posts.*))
            from posts 
            where author_id = user_uuid
        ),
        'comments', (
            select jsonb_agg(to_jsonb(comments.*))
            from comments 
            where author_id = user_uuid
        )
    )
    into user_data
    from profiles p
    where p.id = user_uuid;
    
    return user_data;
end;
$$ language plpgsql security definer;

-- ============================================================================
-- FINAL SECURITY RECOMMENDATIONS
-- ============================================================================

/*
IMPORTANT SECURITY CONSIDERATIONS:

1. API Keys:
   - Use anon key only for public read operations
   - Use service role key only in server-side code
   - Never expose service role key in client-side code

2. Authentication:
   - Implement proper JWT validation
   - Use auth.uid() in all policies
   - Consider implementing additional rate limiting

3. Data Validation:
   - Validate all inputs in application layer
   - Use check constraints for data integrity
   - Implement proper sanitization for user content

4. Performance:
   - Monitor policy execution performance
   - Add appropriate indexes for policy conditions
   - Consider using functions for complex policy logic

5. Audit:
   - Log all sensitive operations
   - Monitor failed authentication attempts
   - Regular security audits of policies

6. Backup:
   - Regular database backups
   - Test restore procedures
   - Consider point-in-time recovery
*/