# АrtHub

ArtHub is a full-featured web application built with Django that allows artists to share, organize and interact with creative content.

Users can create accounts, share artworks, organize them into albums, join groups, participate in discussions and engage with content through likes, comments, and notifications.

---

## Live Demo
The project is deployed and can be accessed here:

**https://arthub-behze2a0fbhsd5at.italynorth-01.azurewebsites.net/**

The application can be explored directly in the browser without local setup.

### What can be tested
- user registration and login
- profile management
- artwork creation and gallery
- groups and posts
- comments and likes
- notifications
- password reset functionality

---

## Key Highlights
- Role-based permission system (Owner / Admin / Moderator / Member)
- Secure object-level access control using custom mixins
- Queryset scoping to prevent unauthorized access
- Asynchronous processing with Celery
- In-app notification system powered by Django REST Framework
- Drag-and-drop interface for adding artworks to group folders

---

## Features

### Authorization

**Django Permissions**
- Role-based moderation using Django auth Groups
- Predefined staff groups:
  - Content Editor
  - Content Moderator
- Group permissions are assigned with data migration
- Editors can edit selected content types
- Moderators can delete selected content types

**Object-Level Access Control**
- Custom mixins enforce ownership and permission checks
- Queryset scoping prevents unauthorized access to objects

**Group Role System**
- Each group has role-based permissions:
  - Owner
  - Admin
  - Moderator
  - Member
---

### Users
- User registration and authentication
- Automatic Profile creation (via Django signals)
- Automatic default album creation (via Django signals)
- Welcome email sent on registration (Celery shared tasks)
- Password reset email sent asynchronously with Celery

**Profile includes:**
- Username, Email
- First and Last name
- Professional artist flag
- Description
- Avatar and Banner

---

### Artworks
- Create artworks with:
    - Title
    - Description
    - Image URL
    - Artwork type (predefined choices)
    - Tags
- Assign artworks to:
  - Multiple albums
  - Multiple groups (via submissions)
- Features:
  - Tag system with automatic cleaning and validation
  - Search by title or tags
  - Gallery pagination
  - Displayed in user profile (Gallery tab)
  - Users can assign artworks only to their own albums

---

### Albums
- Each user can create multiple albums
- Album names must be unique per user
- An album can contain multiple artworks
- An artwork can belong to multiple albums
- Albums are displayed in the user profile
- Only the owner can edit or delete an album
- Default album is automatically created upon registration
- Artworks can be removed from albums during editing

---

### Tags

- Tags are entered in a single field (comma-separated)
- Automatic:
    - Duplicate removal
    - Whitespace trimming
- Tags support letters/numbers and multi-word names with spaces or hyphens
- One tag can be associated with multiple artworks

---

### Interactions

**Comments**

- Comment on artworks and group posts
- Nested replies (infinite depth supported)
- Permissions:
  - Owner can edit/delete own comments
  - Artwork owners and post authors can delete related comments
- Ordered by creation time

**Likes**

- Like/unlike
  - Artworks
  - Posts
  - Comments
- One like per user per object
- Database constraints ensure each like targets exactly one object

**Access Rules**
- Group membership is required for commenting and liking group post content

---

### Core Pages

**Home Page**
- Displays featured artworks
- Highlights the most liked artworks on the platform

**Gallery**
- Displays all artworks from the platform
- Search artworks by title or tags
- Tag-based navigation for quick filtering
- Dynamic loading of additional artworks via AJAX pagination

**Error Handling**
- Custom error pages (400, 403, 404, 500)
- User-friendly error pages
---

### Groups

Groups allow users to collaborate, share artworks and interact in communities.

**Core Features**
- Create and manage groups
- Automatic creation of a default **Featured** folder
- Group owner is automatically assigned an **Admin** role

**Join Policies**
- Open groups (instant membership)
- Approval-based groups with join requests

**Roles**
- Owner
- Admin
- Moderator
- Member
---

### Group Permissions
- Owner:
  - Full control over group, members and roles
- Admin:
  - Manage members and content
  - Approve/reject submissions
- Moderator:
  - Moderate content and submissions
- Member:
  - Submit artworks and create posts
---

### Group Folders
- Organize artworks inside groups
- Each group can have multiple folders
- Default folder: Featured
- Users can select a folder when submitting artwork (applied after approval for members)
- Admins and moderators can manage folders
- Artworks can be added to folders using drag-and-drop

---

### Artwork Submissions
- Members submit artwork to groups
- Admins and moderators can:
  - Approve - artwork is added to group/folder
  - Reject
- Auto-approval for admins/moderators
- Approved artworks are automatically added to the group and selected folder

---
### Membership System

- Join/leave groups
- Join requests for approval-based groups
- Role management for members

---

### Posts
- Members can create posts inside groups
- Posts support:
  - Images
  - Comments
  - Likes

---

### Notifications

In-app notification system for user interactions and group activity.

**Triggers**
- New comments on artworks and posts
- Replies to comments
- Likes on artworks, posts and comments
- New group posts
- Public group joins
- Join requests (sent/approved/rejected)
- Artwork submissions updates

**System Features**
- Centralized notification service
- Self-notifications are prevented automatically
- Notifications include target URLs for related content

**API**
- Built with Django REST Framework
- Fetch unread notifications
- Mark notifications as read
- Retrieve unread notifications count

---

## Technologies
- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** Server-rendered HTML (Django Templates), CSS, JavaScript
- **Media Storage**: Cloudinary (image hosting and delivery)
- **Async Tasks:** Celery (background task processing)
- **Message Broker:** Redis
- **API:** Django REST Framework

---

## Project Structure
```
artHub/  
├── accounts/       # Custom user logic, authentication and signals
├── albums/         # Album management
├── artHub/         # Core Django project settings and URL configuration
├── artworks/       # Artworks, tags, search
├── common/         # Shared views and error pages
├── groups/         # Groups, posts, submissions
├── interactions/   # Comments and likes
├── notifications/  # Notifications system + API
├── static/         # CSS, Images, JavaScript
└── templates/      # HTML Templates
```

---

## Environment Variables
The project uses environment variables for local development.
A `.env.example` file is included in the root directory as a template.

### Steps to set up your environment
1. Copy the example file to create your local `.env`:

```bash
cp .env.example .env    #Linux / Mac
copy .env.example .env  #Windows
```

2. Edit .env if needed. Example demo values:
```env
SECRET_KEY=local_secret_key

# Database
DB_NAME=arthub_demo
DB_USER=demo_user
DB_PASS=demo123
DB_PORT=5432
DB_HOST=127.0.0.1

# Django settings
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=

# Optional SMTP configuration
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

# Cloudinary media storage
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

If SMTP credentials are not provided, emails can be tested locally using MailHog.

### Media Storage
User uploaded images are stored using Cloudinary.

If Cloudinary credentials are not provided, image upload features will be disabled.
The application can still be explored using the demo data included in the project.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/NikolinaPetrova/artHub.git
cd artHub
```
### 2. Create and activate a virtual environment
Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start local services (Redis + MailHog)
The project uses Docker Compose for development services.
```bash
docker-compose up -d
```

This starts:
- Redis (used by Celery)
- RedisInsight (Redis UI)
- MailHog (local email testing server)

MailHog interface:
```bash
http://127.0.0.1:8025
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Collect static files
```bash
python manage.py collectstatic
```
**This step prepares static files for production using WhiteNoise**

## Demo Data

The project includes demo data generated through data migrations for easier testing and exploration.

After running:
```bash
python manage.py migrate
```
The database will be automatically populated with:
- Demo users
- Albums
- Artworks
- Tags
- Comments
- Likes

This allows the application to be explored immediately without creating content manually.

---

## Demo Users
The following demo accounts can be used to explore the platform:
- **Username:** alice | **Password:** 123pass123 - member of **Content Editor** and **Content Moderator** groups
- **Username:** dave | **Password:** 123pass123 - member of **Content Editor** group

### 7. Run Celery worker
Linux / macOS
```bash
celery -A artHub worker -l info
```

Windows
```bash
celery -A artHub worker --loglevel=info --pool=solo
```

### 8. Run the development server
```bash
python manage.py runserver
```
Visit:
```
http://127.0.0.1:8000/
```
---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
