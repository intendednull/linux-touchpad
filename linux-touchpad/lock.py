import os
from contextlib import suppress
from pathlib import Path


class Lock:

    _lock: Path = Path(__file__).with_name('.lock')

    def __init__(self):
        if self.islocked():
            lockpid = self.getpid()
            with suppress(ProcessLookupError):
                os.kill(lockpid, 9)
            self.cleanup()

    def __enter__(self):
        self.create_lock()
        return self

    def __exit__(self, *args):
        self.cleanup()

    def create_lock(self):
        self._lock.write_text(str(os.getpid()))

    def cleanup(self):
        with suppress(FileNotFoundError):
            self._lock.unlink()

    @staticmethod
    def islocked() -> bool:
        return Lock._lock.exists()

    @staticmethod
    def getpid():
        return int(Lock._lock.read_text())
