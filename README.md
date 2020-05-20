For test this code you need to install Docker and docker-compose.
visit below links:
    <https://docs.docker.com/engine/install/>
    <https://docs.docker.com/compose/install/>

For run project:
```
docker-compose up -d
python3 -m venv .env
. .env/bin/active
pip install -r req.txt
export FLASK_APP=app.py
flask run
```
