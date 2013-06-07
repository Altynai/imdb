#!/usr/bin/env python
# -*- coding: utf-8 -*-

def string2int(string):
	try:
		return int(string)
	except ValueError:
		return string

# =================test==================== #
def test():
	print type(string2int("-1"))
	print type(string2int("asa"))

if __name__ == '__main__':
	test()