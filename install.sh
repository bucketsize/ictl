#!/bin/sh

python3 -m build
pip3 install dist/ictl-0.0.1-*.whl --force-reinstall
