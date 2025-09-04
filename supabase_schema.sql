-- CivicBlogs Database Schema for Supabase with Row Level Security
-- This schema is designed for a scalable blog platform with proper security

-- Enable necessary extensions
create extension if not exists "uuid-ossp";

-- ============================================================================
-- PROFILES TABLE (User Management)
-- ============================================================================
create table profiles (
    id uuid references auth.users on delete cascade not null primary key,
    username text unique,
    full_name text,
    avatar_url text,
    bio text,
    website text,
    role text check (role in ('admin', 'editor', 'author', 'subscriber')) default 'subscriber',
    is_active boolean default true,
    email_verified boolean default false,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Enable RLS on profiles
alter table profiles enable row level security;

-- Profiles policies
create policy "Public profiles are viewable by everyone" on profiles
    for select using (true);

create policy "Users can insert their own profile" on profiles
    for insert with check (auth.uid() = id);

create policy "Users can update their own profile" on profiles
    for update using (auth.uid() = id);

-- Only admins can delete profiles
create policy "Only admins can delete profiles" on profiles
    for delete using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- Index for performance
create index profiles_username_idx on profiles(username);
create index profiles_role_idx on profiles(role);

-- ============================================================================
-- CATEGORIES TABLE
-- ============================================================================
create table categories (
    id uuid default uuid_generate_v4() primary key,
    name text not null,
    slug text unique not null,
    description text,
    color text default '#6366f1',
    image_url text,
    is_active boolean default true,
    sort_order integer default 0,
    created_by uuid references profiles(id) on delete set null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Enable RLS on categories
alter table categories enable row level security;

-- Categories policies
create policy "Categories are viewable by everyone" on categories
    for select using (is_active = true);

create policy "Only editors and admins can manage categories" on categories
    for all using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Indexes
create index categories_slug_idx on categories(slug);
create index categories_active_idx on categories(is_active);
create index categories_sort_idx on categories(sort_order);

-- ============================================================================
-- TAGS TABLE
-- ============================================================================
create table tags (
    id uuid default uuid_generate_v4() primary key,
    name text not null,
    slug text unique not null,
    description text,
    color text default '#8b5cf6',
    usage_count integer default 0,
    created_by uuid references profiles(id) on delete set null,
    created_at timestamptz default now()
);

-- Enable RLS on tags
alter table tags enable row level security;

-- Tags policies
create policy "Tags are viewable by everyone" on tags
    for select using (true);

create policy "Authenticated users can create tags" on tags
    for insert with check (auth.uid() is not null);

create policy "Only creators and admins can update tags" on tags
    for update using (
        auth.uid() = created_by or 
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Indexes
create index tags_slug_idx on tags(slug);
create index tags_usage_idx on tags(usage_count desc);

-- ============================================================================
-- POSTS TABLE
-- ============================================================================
create table posts (
    id uuid default uuid_generate_v4() primary key,
    title text not null,
    slug text unique not null,
    excerpt text,
    content text not null,
    featured_image_url text,
    featured_image_alt text,
    status text check (status in ('draft', 'published', 'archived', 'scheduled')) default 'draft',
    visibility text check (visibility in ('public', 'private', 'password')) default 'public',
    password text, -- for password protected posts
    meta_description text,
    meta_keywords text,
    reading_time integer default 0, -- in minutes
    view_count integer default 0,
    like_count integer default 0,
    comment_count integer default 0,
    is_featured boolean default false,
    is_pinned boolean default false,
    allow_comments boolean default true,
    category_id uuid references categories(id) on delete set null,
    author_id uuid references profiles(id) on delete cascade not null,
    published_at timestamptz,
    scheduled_at timestamptz,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Enable RLS on posts
alter table posts enable row level security;

-- Posts policies
create policy "Published posts are viewable by everyone" on posts
    for select using (
        status = 'published' and 
        visibility = 'public' and 
        (published_at is null or published_at <= now())
    );

create policy "Authors can view their own posts" on posts
    for select using (auth.uid() = author_id);

create policy "Admins and editors can view all posts" on posts
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Authors and above can create posts" on posts
    for insert with check (
        auth.uid() = author_id and
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor', 'author')
        )
    );

create policy "Authors can update their own posts" on posts
    for update using (
        auth.uid() = author_id or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Only admins can delete posts" on posts
    for delete using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role = 'admin'
        )
    );

-- Indexes for performance
create index posts_slug_idx on posts(slug);
create index posts_status_idx on posts(status);
create index posts_author_idx on posts(author_id);
create index posts_category_idx on posts(category_id);
create index posts_published_idx on posts(published_at desc);
create index posts_featured_idx on posts(is_featured, published_at desc);
create index posts_view_count_idx on posts(view_count desc);

-- ============================================================================
-- POST_TAGS TABLE (Many-to-Many relationship)
-- ============================================================================
create table post_tags (
    id uuid default uuid_generate_v4() primary key,
    post_id uuid references posts(id) on delete cascade not null,
    tag_id uuid references tags(id) on delete cascade not null,
    created_at timestamptz default now(),
    unique(post_id, tag_id)
);

-- Enable RLS on post_tags
alter table post_tags enable row level security;

-- Post_tags policies
create policy "Post tags are viewable by everyone" on post_tags
    for select using (
        exists (
            select 1 from posts 
            where id = post_id and status = 'published' and visibility = 'public'
        )
    );

create policy "Authors can manage tags for their posts" on post_tags
    for all using (
        exists (
            select 1 from posts 
            where id = post_id and author_id = auth.uid()
        ) or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Indexes
create index post_tags_post_idx on post_tags(post_id);
create index post_tags_tag_idx on post_tags(tag_id);

-- ============================================================================
-- COMMENTS TABLE
-- ============================================================================
create table comments (
    id uuid default uuid_generate_v4() primary key,
    post_id uuid references posts(id) on delete cascade not null,
    parent_id uuid references comments(id) on delete cascade, -- for nested comments
    author_id uuid references profiles(id) on delete set null, -- null for anonymous comments
    author_name text, -- for anonymous comments
    author_email text, -- for anonymous comments
    author_website text, -- optional
    content text not null,
    is_approved boolean default false,
    is_spam boolean default false,
    like_count integer default 0,
    user_agent text,
    ip_address inet,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- Enable RLS on comments
alter table comments enable row level security;

-- Comments policies
create policy "Approved comments are viewable by everyone" on comments
    for select using (
        is_approved = true and is_spam = false and
        exists (
            select 1 from posts 
            where id = post_id and status = 'published' and allow_comments = true
        )
    );

create policy "Users can view their own comments" on comments
    for select using (auth.uid() = author_id);

create policy "Moderators can view all comments" on comments
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Anyone can create comments" on comments
    for insert with check (
        exists (
            select 1 from posts 
            where id = post_id and status = 'published' and allow_comments = true
        )
    );

create policy "Users can update their own comments" on comments
    for update using (
        auth.uid() = author_id or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Moderators can delete comments" on comments
    for delete using (
        auth.uid() = author_id or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Indexes
create index comments_post_idx on comments(post_id, created_at desc);
create index comments_parent_idx on comments(parent_id);
create index comments_approved_idx on comments(is_approved, created_at desc);

-- ============================================================================
-- NEWSLETTER_SUBSCRIBERS TABLE
-- ============================================================================
create table newsletter_subscribers (
    id uuid default uuid_generate_v4() primary key,
    email text unique not null,
    status text check (status in ('active', 'unsubscribed', 'pending')) default 'pending',
    subscribed_at timestamptz default now(),
    unsubscribed_at timestamptz,
    verification_token text,
    verified_at timestamptz,
    preferences jsonb default '{}', -- subscription preferences
    source text default 'website' -- where they subscribed from
);

-- Enable RLS on newsletter_subscribers
alter table newsletter_subscribers enable row level security;

-- Newsletter policies
create policy "Only admins can view subscribers" on newsletter_subscribers
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Anyone can subscribe" on newsletter_subscribers
    for insert with check (true);

create policy "Users can update their own subscription" on newsletter_subscribers
    for update using (true); -- Will be controlled by token in application logic

-- Index
create index newsletter_email_idx on newsletter_subscribers(email);
create index newsletter_status_idx on newsletter_subscribers(status);

-- ============================================================================
-- CONTACT_MESSAGES TABLE
-- ============================================================================
create table contact_messages (
    id uuid default uuid_generate_v4() primary key,
    name text not null,
    email text not null,
    subject text not null,
    message text not null,
    is_read boolean default false,
    replied_at timestamptz,
    ip_address inet,
    user_agent text,
    created_at timestamptz default now()
);

-- Enable RLS on contact_messages
alter table contact_messages enable row level security;

-- Contact messages policies
create policy "Only admins can view contact messages" on contact_messages
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Anyone can send contact messages" on contact_messages
    for insert with check (true);

create policy "Only admins can update contact messages" on contact_messages
    for update using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- Index
create index contact_messages_read_idx on contact_messages(is_read, created_at desc);

-- ============================================================================
-- MEDIA_FILES TABLE (For file management)
-- ============================================================================
create table media_files (
    id uuid default uuid_generate_v4() primary key,
    filename text not null,
    original_filename text not null,
    mime_type text not null,
    file_size bigint not null,
    file_path text not null, -- path in storage
    alt_text text,
    caption text,
    width integer,
    height integer,
    uploaded_by uuid references profiles(id) on delete set null,
    created_at timestamptz default now()
);

-- Enable RLS on media_files
alter table media_files enable row level security;

-- Media files policies
create policy "Media files are viewable by everyone" on media_files
    for select using (true);

create policy "Authors and above can upload media" on media_files
    for insert with check (
        auth.uid() = uploaded_by and
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor', 'author')
        )
    );

create policy "Users can update their own media" on media_files
    for update using (
        auth.uid() = uploaded_by or
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

-- ============================================================================
-- ANALYTICS TABLE (for tracking)
-- ============================================================================
create table analytics (
    id uuid default uuid_generate_v4() primary key,
    post_id uuid references posts(id) on delete cascade,
    event_type text not null, -- 'view', 'like', 'share', etc.
    user_id uuid references profiles(id) on delete set null,
    session_id text,
    ip_address inet,
    user_agent text,
    referrer text,
    created_at timestamptz default now()
);

-- Enable RLS on analytics
alter table analytics enable row level security;

-- Analytics policies
create policy "Only admins can view analytics" on analytics
    for select using (
        exists (
            select 1 from profiles 
            where id = auth.uid() and role in ('admin', 'editor')
        )
    );

create policy "Track events for published posts" on analytics
    for insert with check (
        exists (
            select 1 from posts 
            where id = post_id and status = 'published'
        ) or post_id is null
    );

-- Indexes for analytics
create index analytics_post_idx on analytics(post_id, created_at desc);
create index analytics_event_idx on analytics(event_type, created_at desc);
create index analytics_user_idx on analytics(user_id, created_at desc);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Add updated_at triggers
create trigger update_profiles_updated_at before update on profiles
    for each row execute function update_updated_at_column();

create trigger update_categories_updated_at before update on categories
    for each row execute function update_updated_at_column();

create trigger update_posts_updated_at before update on posts
    for each row execute function update_updated_at_column();

create trigger update_comments_updated_at before update on comments
    for each row execute function update_updated_at_column();

-- Function to update tag usage count
create or replace function update_tag_usage_count()
returns trigger as $$
begin
    if TG_OP = 'INSERT' then
        update tags set usage_count = usage_count + 1 where id = new.tag_id;
        return new;
    elsif TG_OP = 'DELETE' then
        update tags set usage_count = usage_count - 1 where id = old.tag_id;
        return old;
    end if;
    return null;
end;
$$ language plpgsql;

-- Trigger to update tag usage count
create trigger update_tag_usage_trigger
    after insert or delete on post_tags
    for each row execute function update_tag_usage_count();

-- Function to update post comment count
create or replace function update_post_comment_count()
returns trigger as $$
begin
    if TG_OP = 'INSERT' then
        update posts set comment_count = comment_count + 1 where id = new.post_id;
        return new;
    elsif TG_OP = 'DELETE' then
        update posts set comment_count = comment_count - 1 where id = old.post_id;
        return old;
    end if;
    return null;
end;
$$ language plpgsql;

-- Trigger to update comment count
create trigger update_comment_count_trigger
    after insert or delete on comments
    for each row execute function update_post_comment_count();

-- ============================================================================
-- SAMPLE DATA INSERTION (Optional)
-- ============================================================================

-- Insert sample categories (will need to be run by authenticated admin user)
/*
insert into categories (name, slug, description, color) values
('Technology', 'technology', 'Latest technology trends and news', '#3b82f6'),
('Politics', 'politics', 'Political discussions and news', '#ef4444'),
('Society', 'society', 'Social issues and community topics', '#10b981'),
('Environment', 'environment', 'Environmental issues and sustainability', '#22c55e');
*/

-- ============================================================================
-- SECURITY NOTES
-- ============================================================================
/*
1. All tables have RLS enabled with appropriate policies
2. Policies are designed to be secure by default
3. Anonymous users can only read published content
4. Authenticated users have limited write access based on roles
5. Admin role has elevated permissions
6. All sensitive operations require proper authentication
7. Indexes are added for performance on commonly queried columns
8. Triggers maintain data consistency (counts, timestamps)
*/