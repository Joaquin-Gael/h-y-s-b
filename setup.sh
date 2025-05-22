pip3 install uv
uv export --format requirements-txt > requirements.txt
ls
pip3 install -r requirements.txt
fastapi run main.py