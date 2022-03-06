from pathlib import Path
from typing import List

from pycrashreport.crash_report import CrashReport


class CrashReports:
    """" manage crash reports """

    def __init__(self, client, crash_reports_dir):
        self._client = client
        self._crash_reports_dir = crash_reports_dir

    def set_symbolicated(self, enabled: bool = True):
        """
        enable/disable crash reports symbolication
        https://github.com/dlevi309/Symbolicator
        """
        with self._client.sc.open(
                '/var/root/Library/Preferences/com.apple.CrashReporter.plist') as pref:
            pref.set_dict({'SymbolicateCrashes': enabled})

    def list(self, prefixed='') -> List[CrashReport]:
        """ get a list of all crash reports as CrashReport parsed objects """
        result = []
        for root in self._client.roots:
            root = Path(root) / self._crash_reports_dir

            if not self._client.fs.accessible(root):
                continue

            for entry in self._client.fs.scandir(root):
                if entry.is_file() and entry.name.endswith('.ips') and entry.name.startswith(prefixed):
                    with self._client.fs.open(entry.path, 'r') as f:
                        result.append(CrashReport(f.readall().decode(), filename=entry.path))
        return result

    def clear(self, prefixed=''):
        """ remove all existing crash reports """
        for entry in self.list(prefixed=prefixed):
            self._client.fs.remove(entry.filename)
