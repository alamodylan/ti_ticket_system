import os
import sys

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(
    0,
    BASE_DIR
)

from app import create_app
from app.services.email_pop_inbox_service import (
    EmailPopInboxService
)


app = create_app()

with app.app_context():

    result = EmailPopInboxService.process_latest_emails(
        limit=20
    )

    print(result)