import asyncio
import sshkeyboard
import time
import threading

def press(key):
    print(f"'{key}' pressed")

threading.Thread(target=sshkeyboard.listen_keyboard, args=(press,)).start()

print("Listening for keyboard events...")

time.sleep(3)
sshkeyboard.stop_listening()

