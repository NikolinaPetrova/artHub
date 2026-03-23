# АrtHub

ArtHub is a full-featured web application built with Django that allows artists to share, organize and interact with creative content.

Users can create accounts, share artworks, organize them into albums, join groups, participate in discussions and engage with content through likes, comments, and notifications.

---

## Features

### Users
- User registration and authentication
- Automatic Profile creation (via Django signals)
- Automatic default album creation (via Django signals)
- Email confirmation on registration (Celery shared tasks)

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
  - Tag system (auto-cleaned input)
  - Search by title or tags
  - Displayed in user profile (Gallery tab)

---

### Albums
- Each user can create multiple albums
- An album can contain multiple artworks
- An artwork can belong to multiple albums
- Albums are displayed in the user profile
- Only the owner can edit or delete an album
- Default album is automatically created upon registration

---

### Tags

- Tags are entered in a single field (comma-separated)
- Automatic:
    - Duplicate removal
    - Whitespace trimming
- One tag can be associated with multiple artworks

---

### Interactions

**Comments**

- Comment on artwork and group posts
- Nested replies (infinite depth supported)
- Permissions:
  - Owner can edit/delete own comments
  - Artwork/Post owner can delete comments
- Ordered by creation time

**Likes**

- Like/unlike
  - Artworks
  - Posts
  - Comments
- One like per user per object

---

### Gallery
- Displays all artworks
- Quick preview overlay

---

### Groups

Groups allow users to collaborate, share artworks and interact in communities.

**Core Features**
- Create and manage groups
- Join policies:
  - Open
  - Approval-based
- Roles
  - Admin
  - Moderator
  - Member

---

### Group Folders
- Organize artworks inside groups
- Each group can have multiple folders
- Default folder: Featured
- Users can select a folder when submitting artwork (applied after approval for members)
- Admins and moderators can manage folders

---

### Artwork Submissions
- Members submit artwork to groups
- Admins and moderators can:
  - Approve - artwork is added to group/folder
  - Reject
- Auto-approval for admins/moderators

---
### Membership System

- Join/leave groups
- Join requests for private groups
- Moderation system for approvals

---

### Posts
- Members can create posts inside groups
- Posts support:
  - Images
  - Comments
  - Likes

---

### Notifications

Real-time notification system for user interactions:
- New comments
- Replies
- Likes
- New group posts
- Join requests (sent/approved/rejected)
- Artwork submissions updates

**Includes:**
- REST API endpoints (Django REST Framework)
- Unread notifications count
- Mark as read functionality

---

## Technologies
- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** Server-rendered HTML (Django Templates), CSS, JavaScript
- **Async Tasks:** Celery
- **API:** Django REST Framework

---

## Project Structure
```
artHub/  
├── accounts/       # Custom user logic, authentication and signals
├── albums/         # Album management
├── artHub/         # Core Django project settings and URL configuration
├── artworks/       # Artworks, tags, search
├── common/         # Shared views (Home page, 400, 403, 404, 500)
├── groups/         # Groups, posts, submissions
├── interactions/   # Comments and likes
├── notifications/  # Notifications system + API
├── static/         # CSS, Images
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
DB_NAME=arthub_demo
DB_USER=demo_user
DB_PASS=demo123
DB_PORT=5432
DB_HOST=127.0.0.1
```
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

### 4. Apply migrations
```bash
python manage.py migrate
```

## Demo Data

The project includes a fully populated demo database for easy testing and exploration.
It contains:
- Pre-created users
- Albums
- Artworks
- Tags
- Comments
- Likes

After running:
```bash
python manage.py migrate
```
All demo data will be available immediately.

---

## Demo Users
Use the following accounts to log in locally:
- **Username:** alice | **Password:** 123pass123
- **Username:** dave | **Password:** 123pass123

### 5. Run the development server
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
