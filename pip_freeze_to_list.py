#!/usr/bin/env python
# coding: utf-8

import re

infile = "requirements.txt"
outfile = "requirements.txt"

with open(infile, "r") as f:
    skiplines = 2
    lines = [line.strip() for line in f][skiplines:]
    whitespace_pattern = re.compile(r"\s+")
    lines = [whitespace_pattern.sub("==", line) for line in lines]
    
with open(outfile, "w") as f:
    f.write("\n".join(lines))

