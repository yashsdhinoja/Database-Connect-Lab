# MoodTrackerAI - Hybrid Surveillance & Behavioral Engine

MoodTrackerAI is a full-stack Python backend architecture that processes user activity, screen time, and engagement metrics to dynamically analyze user mood and deliver real-time content recommendations.

It utilizes a **Polyglot Persistence Architecture**, linking structured user profile data in **Supabase (PostgreSQL)** with high-volume behavioral analytics streaming into **MongoDB Atlas (NoSQL)** via a shared `user_id` (UUID).

---

## 🏛 System Architecture

![System Architecture Diagram](docs/architecture_diagram.png)

- **Client Layer:** Front-end application tracking user interactions (watch time, skips, likes, comments).
- **FastAPI Backend:** Central engine split into modular routes (`users` and `analytics`).
- **Supabase (PostgreSQL):** Stores relational data (user profile, posts, followers, comments).
- **MongoDB Atlas (NoSQL):** Stores high-frequency unstructured data (screen time, activity logs, sentiment/mood states).

---

## 📁 Repository Folder Structure

```text
MoodTrackerAI/
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Centralized environment variable configurations
│
├── database/
│   ├── __init__.py
│   ├── supabase_client.py   # Supabase client setup
│   └── mongo_client.py      # PyMongo client setup
│
├── models/
│   ├── __init__.py
│   ├── user_models.py       # Pydantic schemas for Supabase
│   └── activity_models.py   # Pydantic schemas for MongoDB
│
├── routes/
│   ├── __init__.py
│   ├── users.py             # User profile endpoints (Supabase)
│   └── analytics.py         # Activity & sentiment logic (MongoDB)
│
├── .env                     # API keys & Connection strings (Git Ignored)
├── .gitignore
├── main.py                  # FastAPI Application Entrypoint
└── requirements.txt         # Dependencies
```

📋 1. Prerequisites
Before setting up the project, make sure you have the following installed and configured:

Python: Version 3.10 or higher installed on your system.

Git: Installed for version control.

Supabase Account: A free tier project on Supabase.

MongoDB Atlas Account: A free cluster set up on MongoDB Atlas.

⚙️ 2. Installation & Environment Setup
Follow these commands to clone the repository and set up your Python environment:

Clone the Repository:

Bash
git clone [https://github.com/your-username/MoodTrackerAI.git](https://github.com/your-username/MoodTrackerAI.git)
cd MoodTrackerAI
Create a Virtual Environment:

Bash
# On Windows (PowerShell / Command Prompt)
python -m venv .venv

# On macOS / Linux
python3 -m venv .venv
Activate the Virtual Environment:

Bash
# On Windows (PowerShell)
.\.venv\Scripts\activate

# On Windows (Command Prompt)
.venv\Scripts\activate.bat

# On macOS / Linux
source .venv/bin/activate
Install Required Packages:

Bash
pip install -r requirements.txt
🗄️ 3. Database Configuration
A. Supabase Setup (PostgreSQL)
Go to your Supabase Dashboard and open the SQL Editor.

Run the following SQL query to create the user profiles and comments tables:

SQL
-- Create user profiles table
CREATE TABLE public.profiles (
    user_id UUID PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE NOT NULL,
    age INT,
    no_posts INT DEFAULT 0,
    no_videos INT DEFAULT 0,
    followers_count INT DEFAULT 0,
    following_count INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create comments table
CREATE TABLE public.comments (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(user_id) ON DELETE CASCADE,
    post_id TEXT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
B. MongoDB Atlas Setup (NoSQL)
Log in to MongoDB Atlas and navigate to Network Access.

Add IP Address 0.0.0.0/0 (Allow Access from Anywhere).

Under Database Access, create a database user and note down the username and password.

Click Connect on your M0 Cluster, select Drivers (Python), and copy your SRV connection string.

🔑 4. Environment Variables Setup
Create a .env file in the root folder of your project (MoodTrackerAI/.env) and populate it with your database connection keys:

Code snippet
# Supabase Configuration
SUPABASE_URL="[https://your-project-id.supabase.co](https://your-project-id.supabase.co)"
SUPABASE_KEY="your-supabase-anon-or-service-role-key"

# MongoDB Atlas Configuration
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
🚀 5. Running the Application
To run the FastAPI server locally with hot-reloading enabled, run:

Bash
uvicorn main:app --reload
Access Interactive API Documentation
Once the server starts running on http://127.0.0.1:8000, open your web browser and navigate to:

Swagger UI Docs: http://127.0.0.1:8000/docs

ReDoc Docs: http://127.0.0.1:8000/redoc

📜 6. License
Distributed under the MIT License. See LICENSE for more information.

