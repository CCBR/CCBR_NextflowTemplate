#!/usr/bin/env python
# this script gets called by bin/tool_name
import os
import re
import sys

# add script directory to the path to allow the CLI to work out-of-the-box
# without the need to install it via pip first
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.append(SCRIPT_DIR)
from src.__main__ import main

if (
    __name__ == "__main__"
):  # this block is adapted from the executable file created by `pip install`
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(main())
