## Personalized Movie Recommendation System Project

### Setup 

1. Download & Install Docker Desktop [Docker Desktop](https://www.docker.com/products/docker-desktop/) 
2. Run Docker Desktop 
3. Clone or Download Repository [Personalized-Movie-Recommendation-System](https://github.com/yejinyeo/Personalized-Movie-Recommendation-System)
4. Open repo in IDE `cd Personalized-Movie-Recommendation-System` 
5. Make sure ports 3307, 8001, 3001 are not preoccupied 
6. Build Docker Image & Run Images in Containers `docker-compose up` 
7. Happy coding! 

--- 

### Project Structure

- GitHub 
- Docker 
- Database: MySQL `/mysql`
- API: FastAPI Python `/api`
- Frontend: React JS `/frontend` 

--- 

### GitHub

```shell
git clone https://github.com/yejinyeo/Personalized-Movie-Recommendation-System.git
```

--- 

### Dev Env - Docker Compose

- [Docker](https://www.docker.com/) 
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) 

```shell
cd Personalized-Movie-Recommendation-System
docker-compose build
docker-compose up
```

#### Project Development Container Host Ports

- DB server `http://localhost:3307` 
- API server `http://localhost:8001` 
- Frontend `http://localhost:3001` 

--- 

### MySQL 

`/mysql` 

- Initial DB: `/mysql/db/dump.sql` 
- Initial container ENV settings: `/mysql/local.env` 

--- 

### FastAPI 

`/api` 

- Database connector: `/api/database/connector.py` 
- movieLens  
  - movieLens controllers: `/api/movieLens/controllers.py` 
  - movieLens routers: `/api/movieLens/routers.py` 
- FastAPI main app: `/api/main.py` 

--- 

### Frontend React 

`/frontend` 

- [React app](https://create-react-app.dev/docs/) 
- [Tailwind CSS](https://tailwindcss.com/docs/) 

--- 
