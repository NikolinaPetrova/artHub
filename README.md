# АrtHub

ArtHub is a web application built with Django that allows users to create accounts, share artworks, organize them into albums, interact through comments and nested replies.
The platform is designed to support different types of artists and creative content.

---

## Features

### Users
- User registration and authentication
- Automatic default album creation on registration (via Django signals)
- User profile includes:
    - Username
    - Email
    - First name
    - Last name
    - Professional artist flag

---

### Artworks
- Create artworks with:
    - Title
    - Description
    - Image URL
    - Artwork type (validated with predefined choices)
    - Tags
- Assign artworks to one or multiple albums
- Each artwork can have multiple tags
- All artworks are displayed on the Home page
- Search functionality:
    - Search artworks by title
    - Search artworks by tags

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

### Comments and Nested Replies

- Users can comment on artworks
- Support for nested replies (reply to a comment or another reply)
- Comment permissions:
    - Edit/Delete by comment owner
    - Artwork owner can delete any comment under their artwork
- Comments are displayed hierarchically
- Ordered by creation time

---

### Likes
- Users can like/unlike artworks
- One like per user per artwork (unique constraint)

---

### Gallery
- Displays all artworks created by the currently logged-in user
- Overlay button for quick artwork details

---

## Technologies
- Python
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript for buttons and overlays for comments

---

## Project Structure
```
artHub/
├── accounts/   # Custom user logic, authentication and signals
├── albums/     # Album management and relations to artworks
├── artHub/     # Core Django project settings and URL configuration
├── artworks/   # Artworks, tags, comments, likes
├── common/     # Shared views (Home page, 404), Search functionality 
├── static/     # CSS, Images
└── templates/  # HTML Templates
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
