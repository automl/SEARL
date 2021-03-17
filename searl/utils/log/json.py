"""
save log and show log

"""
import json
import os
import time
from pathlib import Path

from searl.utils.handler.base_handler import Handler


class LogJSON(Handler):

    def __init__(self, log_dir, file_name="json_log.json"):
        super().__init__()

        self.log_dir = Path(log_dir)

        self.file_name = file_name
        self.json_file = file_name

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.json_file = self.counting_name(self.log_dir, self.json_file, suffix=True)

        data = {"start": {'value': 0, 'time_step': None, 'time_stamp': self.time_stamp(), 'time': time.time()}}
        with open(self.log_dir / self.json_file, 'w+') as file:
            file.write(f"[ \n")
            file.write(json.dumps(data))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        with open(self.log_dir / self.json_file, 'a') as file:
            file.write(f"\n]")

    def jlog(self, key: str, value, time_step=None):
        data = {key: {'value': value, 'time_step': time_step, 'time_stamp': self.time_stamp(), 'time': time.time()}}
        with open(self.log_dir / self.json_file, 'a') as file:
            file.write(", \n")
            file.write(json.dumps(data))

    def load_json(self):
        data_list = []
        counter = 0
        counting_file_name = self.file_name.split('.')[0] + f"-{counter}" + self.file_name.split('.')[1]
        while os.path.isfile(self.log_dir / counting_file_name):
            with open(self.log_dir / counting_file_name, 'r') as file:
                data = json.load(file)
            data_list.append(data)

            counter += 1
            counting_file_name = self.file_name.split('.')[0] + f"-{counter}" + self.file_name.split('.')[1]

        return data_list
