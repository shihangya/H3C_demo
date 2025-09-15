from function.android import *
from function.miji import *

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["Android:///",])

while True:
    touch(Template(r"tpl1756968288713.png", record_pos=(-0.01, -0.052), resolution=(1200, 2670)))
    touch(Template(r"tpl1756968809513.png", record_pos=(-0.003, -0.048), resolution=(1200, 2670)))



