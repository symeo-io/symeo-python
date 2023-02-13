import subprocess
from typing import List


class ProcessRunnerPort:
    def run_process(self, process: List[str]) -> None:
        pass


class ProcessRunnerAdapter(ProcessRunnerPort):
    def run_process(self, process: List[str]) -> None:
        subprocess.run(process)
