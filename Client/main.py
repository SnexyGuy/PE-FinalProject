import socket

from unknown_client import *




address =socket.gethostbyname(socket.gethostname())

client = unknown_client(address)
client.start()


#לבנות פונקציות ומתודות שינקו חדרים שנפתחו ולא התחברו אליהם
#לבנות פונקציות ומתודות שיסגרו את החדר שנוצר במידה והיוצר מתנתק לפני שהתחברו לחדר