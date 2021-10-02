python3 update.py
python3 -m pipenv run uvicorn app:asgi_app --host 0.0.0.0 --port 5000 --workers 1 --ws-ping-timeout 120 --timeout-keep-alive 60
