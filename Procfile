web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
worker: cd frontend && streamlit run app.py --server.runOnSave true --server.folderWatchBlacklist [] --server.fileWatcherType watchdog