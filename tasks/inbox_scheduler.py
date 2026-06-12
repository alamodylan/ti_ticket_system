import os
import threading
import time


_scheduler_started = False


def start_inbox_scheduler(app):

    global _scheduler_started

    if _scheduler_started:
        print("INBOX SCHEDULER: ya estaba iniciado.")
        return

    # Evita doble ejecución en algunos entornos debug/reloader
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        return

    _scheduler_started = True

    interval_seconds = int(
        app.config.get(
            "INBOX_SCHEDULER_INTERVAL_SECONDS",
            120
        )
    )

    def worker():

        print("\n====================")
        print("INBOX SCHEDULER INICIADO")
        print(f"Intervalo: {interval_seconds} segundos")
        print("====================\n")

        # Espera inicial para que la app arranque completa
        time.sleep(15)

        while True:

            try:

                with app.app_context():

                    from app.services.email_pop_inbox_service import (
                        EmailPopInboxService
                    )

                    result = EmailPopInboxService.process_latest_emails(
                        limit=20
                    )

                    print("\n====================")
                    print("INBOX SCHEDULER RESULT")
                    print(result)
                    print("====================\n")

            except Exception as error:

                print("\n====================")
                print("ERROR INBOX SCHEDULER")
                print(str(error))
                print("====================\n")

            time.sleep(
                interval_seconds
            )

    thread = threading.Thread(
        target=worker,
        daemon=True
    )

    thread.start()