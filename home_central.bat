showmouse.exe
python update.py
python -m pipenv run uvicorn app:asgi_app --host 0.0.0.0 --port 5000 --workers 1 --ws-ping-timeout 120 --timeout-keep-alive 60 --log-level "warning"
