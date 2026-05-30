from app import create_app, db
from app.services.scheduler import start_scheduler

app = create_app()

if __name__ == '__main__':
    scheduler = start_scheduler(app)
    try:
        app.run(debug=True, port=5000, use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
