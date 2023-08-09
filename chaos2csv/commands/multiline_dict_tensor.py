"""The Mulitline Dict Tensor Module.

This module iterates over all lines of the file and converts multilines, which belongs to each other 
into one single line. Additinal this approach also handles the dict style in which the file is 
saved. Also the tensor shaped data is transformed and saved
"""
from argparse import Namespace
import re
from typing import Any, Dict, List


class Runner:
    """Multiline Dict Runner"""

    def __init__(self) -> None:
        self.headers = []
        self.lines = []
        self.old_line = ""
        self.new_lines = []

    def run(self, args: Namespace, config: None | Dict[str, Any]) -> None:
        """run function of the module.

        Args:
            args (_type_): Arguments of CLI tool
            config (_type_): Configuration dict
        """
        print(config)
        self._fix_multiline(args)
        self._get_header()
        self._fix_dict()

    def save(self, args: Namespace, config: None | Dict[str, Any]) -> None:
        """save to csv file

        Args:
            args (Namespace): Arguments of CLI tool
            config (None | Dict[str, Any]): Configuration dict
        """
        if args.path.suffix == "csv":
            new_path = args.path.with_suffix(".new.csv")
        else:
            new_path = args.path.with_suffix(".csv")

        with open(new_path, "w", encoding="utf-8") as file:
            for line in self.new_lines:
                # write each item on a new line
                file.write(f"{line}\n")

    def _fix_multiline(self, args):
        with open(args.path, "r", encoding="utf-8") as file:
            for line in file:
                if re.match(r"\s", line):
                    self.old_line += line.rstrip("\r\n").lstrip()
                else:
                    self._check_oldline(line)

    def _fix_dict(self):
        self.new_lines.append(",".join(self.headers))
        for line in self.lines:
            new_line = ""
            splitted_line_by_tab = line.split("\t")
            for column in splitted_line_by_tab:
                _, value = map(str.strip, column.split(":", 1))
                if value.startswith("tensor("):
                    values = self._extract_tensor(value)
                    if new_line:
                        new_line += f",{','.join(values)}"
                    else:
                        new_line = ",".join(values)
                    continue
                if new_line:
                    new_line += f",{value}"
                else:
                    new_line = value
            self.new_lines.append(new_line)

    def _check_oldline(self, line: str) -> None:
        # else runs only first time
        if self.old_line:
            self.lines.append(self.old_line)
            self.old_line = line.rstrip("\r\n")
        else:
            self.old_line = line.rstrip("\r\n")

    def _get_header(self) -> None:
        # Pick first line and split at tab
        columns = self.lines[0].split("\t")
        # Foreach column split at ":" and use left side, also remove leading \s
        for column in columns:
            key, value = map(str.strip, column.split(":", 1))
            if value.startswith("tensor"):
                data = self._extract_tensor(value)
                self.headers.extend([f"{key}_{idx}" for idx in range(len(data))])
                continue
            self.headers.append(key)

    def _extract_tensor(self, value) -> List[str]:
        # 1. remove the leading "tensor(["
        # 2. use regex sub to replace "]," and anything following
        # 3. split to create list of values
        return re.sub(r"\]\,.*", "", value.replace("tensor([", "")).split(", ")
