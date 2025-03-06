# aegis
Aegis is open-source software for managing IoT devices. It uses HaLow Wi-Fi for communication and runs on Docker and Kubernetes for deployment and scaling. Written in Python with a RESTful API, the central server collects data from endpoints with software-defined radios and wireless Alfa cards. 



## Prerequisites
- Python 3.10+ (`python3 --version`)
- Docker (`docker --version`)
- Git (`git --version`)

## Setup Steps

```bash
# 1. Clone the Repository
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 2. Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Configure API Key in the root of the proejct
# Create a .env file with your API key (generate one or use a provided key)
echo "AEGIS_API_KEY=your-unique-api-key-here" > .env

# 4. Install Client Dependencies
cd client
pip install gpsd-py3 requests python-dotenv
cd ..

# 5. Build and Run Server with Docker
cd server
docker build -t aegis-server .
source ../.env
docker run -d -p 8000:8000 -v $(pwd):/app -e AEGIS_API_KEY="$AEGIS_API_KEY" --name aegis aegis-server

# 6. Populate Database
# Add API key to database (use the same key as in .env)
docker exec -it aegis python manage.py shell
# In shell, run:
# from search.models import APIKey
# APIKey.objects.create(key="your-unique-api-key-here")
# exit()

# Populate documents from static/docs/
python populate_docs.py

# 7. Run Client
cd ../client
source ../.env
python client.py

# 8. Access the Application
# - Console: Open http://localhost:8000/console in a browser
# - Documents: Open http://localhost:8000/search






