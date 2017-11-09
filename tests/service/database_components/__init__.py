import threading
from service.database_server import database_server
import time

threading.Thread(target=database_server).start()
time.sleep(2)
