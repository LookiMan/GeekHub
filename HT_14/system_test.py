import os
from typing import Union

from utils import get_path


class SystemTest(object):
    def __init__(self, logger):
        self.logger = logger

    def check_directories(self, directories: Union[list, tuple]) -> bool:
        error_flag = False

        for directory in directories:
            if not os.path.exists(get_path(directory)):
                self.logger.error("Відсутня директорія '%s'" % directory)

                error_flag = True

        return error_flag

    def check_files(self, files: Union[list, tuple]) -> bool:
        error_flag = False

        for filename in files:
            if not os.path.exists(filename):
                self.logger.error("Відсутній файл '%s'" % filename)

                error_flag = True

        return error_flag

    def check_system_directories(self) -> bool:
        return self.check_directories(("system",))

    def check_system_files(self) -> bool:
        filenames = []

        for directory in ("system_file",):
            for filename in ("db.sqlite3",):
                filenames.append(get_path(directory, filename))

        return self.check_files(filenames)

    def start(self) -> None:
        self.logger.info("Початок перевірки...")

        errors = [
            self.check_system_directories(),
            self.check_system_files(),
        ]

        if any(errors):
            self.logger.error("Завершення програми через критичну помилку")
            raise Exception("Виявлено критичну помилку")
        else:
            self.logger.info("Перевірка пройшла успішно")
