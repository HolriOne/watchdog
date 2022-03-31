from lib2to3.pgen2 import token
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler
import zulip


def send_msg_zulip(msg_for_send):
    client = zulip.Client(config_file="./zuliprc")
    # Send a stream message
    request = {
        "type": "stream",
        "to": "test_alerts",
        "topic": "123",
        "content": msg_for_send,
    }
    result = client.send_message(request)


class FileEventHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        send_msg_zulip("Внесены изменения в: " + event.src_path)

    def on_moved(self, event):
        # if exist backup file
        if event.src_path + "~" == event.dest_path:
            return
        send_msg_zulip("Перемещен: " + event.src_path)
            
    def on_deleted(self, event):
        send_msg_zulip("Удален: " + event.src_path)
    
    def on_created(self, event):
        send_msg_zulip("Добавлен: " + event.src_path)

if __name__ == "__main__": 
    path="./"
    observer = Observer()
    event_handler = FileEventHandler(ignore_patterns=['*.swp', '*.swx', '*.swpx'])
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    