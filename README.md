# Stats Don't Lie

Stats Don't Lie is a Basketball Stats visualizer built using data from [basketball-reference](https://basketball-reference.com).

[Visit](https://stats-dont-lie.herokuapp.com)

## Technologies

- **Frontend:** React, D3.js, Apollo GraphQL
- **Backend:** Django, GraphQL (Graphene)
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose

## Quick Start with Docker

The easiest way to run this application is using Docker:

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- Git

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/purabshah8/stats-dont-lie.git
   cd stats-dont-lie
   ```

2. **Build and start the application:**
   ```bash
   # Build the Docker images
   docker compose build
   
   # Start the application (database + web server)
   docker compose up -d
   ```

3. **Seed the database with NBA data:**
   ```bash
   # This loads thousands of NBA records (takes several minutes)
   docker compose --profile seed up db-seed
   ```

4. **Access the application:**
   - Open your browser to: `http://localhost:8000`
   - **For network access:** To access from other devices on your network, add your machine's IP address to `ALLOWED_HOSTS` in `docker-compose.yml` and recreate the container with `docker compose up -d --force-recreate web`

### Management Commands

```bash
# View application logs
docker compose logs -f web

# View database logs  
docker compose logs -f db

# Stop the application
docker compose down

# Fresh start (removes all data)
docker compose down -v

# Rebuild after code changes
docker compose build --no-cache
```

## Local Development Setup

If you prefer to run without Docker:

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL 14+

### Setup Steps

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies and build frontend:**
   ```bash
   npm install
   npm run postinstall
   ```

4. **Set up PostgreSQL database:**
   ```bash
   # Create database
   createdb nba
   
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   ```

5. **Seed the database (optional):**
   ```bash
   export DJANGO_DEVELOPMENT=1
   python create_db.py
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Environment Configuration

The application supports different environments:

- **Docker (Production):** SSL enabled, optimized settings
- **Local Development:** Set `DJANGO_DEVELOPMENT=1` for SSL-free database connections

## Data Sources

Basketball Reference stores all its NBA data in HTML tables. The application scrapes and processes:

- Player statistics and biographical data
- Team information and standings  
- Game results and detailed box scores
- Referee assignments
- Historical data across multiple seasons