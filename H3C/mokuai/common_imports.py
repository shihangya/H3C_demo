import pytest_atf
pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime
from mokuai.miji import connect
from mokuai.service import *
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time
from mokuai.android import *