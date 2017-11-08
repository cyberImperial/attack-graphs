import threading
from service.database_server import database_server
import time

threading.Thread(target=database_server).start()
print("DORMMMMMMMMMMMM")
time.sleep(3)
