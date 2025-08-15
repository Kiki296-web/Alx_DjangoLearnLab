## Comment System

### Overview

Authenticated users can add comments to posts. Each comment belongs to a single post and has an author, content, and timestamps.

### Data Model

- **Comment**
  - `post` → `Post` (FK, `on_delete=CASCADE`)
  - `author` → `User` (FK)
  - `content` → `TextField`
  - `created_at`, `updated_at` → `DateTimeField`

### Permissions

- **Create**: Any authenticated user.
- **Edit/Delete**: Only the comment’s author.
- **View**: Public; all comments for a post are visible on the post detail page.

### UI / Templates

- **Post detail**: `blog/post_detail.html`
  - Lists comments under the post.
  - Shows the add-comment form to authenticated users.
- **Edit comment**: `blog/edit_comment.html`
- **Delete comment**: `blog/delete_comment.html`

### URLs

- `posts/<pk>/` → Post detail with comments (`post_detail`)
- `posts/<post_id>/comments/add/` → Add comment (`add_comment`)
- `comments/<pk>/edit/` → Edit comment (`edit_comment`)
- `comments/<pk>/delete/` → Delete comment (`delete_comment`)

### Security

- CSRF protection: All forms include `{% csrf_token %}`.
- Auth checks: Views are protected with `LoginRequiredMixin` and an author-ownership check (e.g., `UserPassesTestMixin` or a manual `request.user == comment.author` guard).
- Passwords: Managed by Django’s built-in hashing (unchanged by the comment feature).

### How to Use

1. Go to a post detail page.
2. If logged in, fill the “Leave a Comment” form and submit.
3. To edit/delete your comment, use the links shown next to your comment.

### Notes

- Deleting a post removes its comments (cascade).
- Validation: the form rejects empty comments; customize max length or profanity checks as needed.
