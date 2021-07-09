from embedded_webserver_thread import FlaskThread, FLASK_PORT, FLASK_HOME_URL, FLASK_SHUTDOWN_ENDPOINT
import webview
from requests import get
from time import sleep

if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    sleep(1)

    webview.create_window('New hunt', FLASK_HOME_URL)
    done = webview.start()

    response = get(FLASK_SHUTDOWN_ENDPOINT)
    print(response)