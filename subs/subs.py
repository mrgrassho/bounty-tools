#!/usr/bin/env python3
from sys import argv
import archive_fo
import crtsh
import wayback

q = argv[1]
a = archive_fo.data(q)
b = crtsh.data(q)
c = wayback.data(q)
d = sorted(a.union(b, c))
for elem in d:
    print(elem)