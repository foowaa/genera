# -*- coding: utf-8 -*-
"""
author: TIAN Chunlin
last update: 2018/9/20
"""
# from .generate_intentions import *
import re


def check(ptr):
    for key, val in ptr.items():
        yes_no_1 = is_undefined_chars(val)
        yes_no_2 = is_bracket_matching(val)
        yes_no_3 = is_in_bracket(val)
        yes_no_4 = is_all_existing_symbol(val)
        yes_no_5 = is_existing_symbol_wrong_place(val)
        if not yes_no_1:
            raise ValueError(
                "Some Undefiend Characters in the intention file in KEY: %s" % key
            )
        if not yes_no_2:
            raise ValueError("The bracket is not matching in KEY: %s" % key)
        if not yes_no_3:
            raise ValueError(
                "Some entity is not in the bracket in KEY: %s" % key)
        if not yes_no_4:
            raise ValueError("Every item has existing symbol in KEY: %s" % key)
        if not yes_no_5:
            raise ValueError(
                "The existing symbol puts in wrong place in KEY: %s" % key)
    return True


def is_undefined_chars(val):
    special_symbols = "：（）"

    for item in val:
        match = [l in special_symbols for l in item]
        if len(set(match)) > 1:
            return False
    return True


def is_bracket_matching(val):
    for item in val:
        num_1 = item.count("(")
        num_2 = item.count(")")
        num_3 = item.count("[")
        num_4 = item.count("]")
        if num_1 != num_2 or num_3 != num_4:
            return False
        # for x in range(len(item)):
        #     for y in range(x+1, len(item)):
        #         if item[x]=='[' and item[y]==']':
        #             pass
        #         elif item[x]=='(' and item[y]==')':
        #             pass
        #         else:
        #             return False

    return True


def is_in_bracket(val):
    pattern = r"(?<=\()(.+?)(?=\))|(?<=\[)(.+?)(?=\])"
    prog = re.compile(pattern)
    for item in val:
        if prog.findall(item):
            x = 0
            item = item.rstrip("\n")
            while x < len(item):
                for y in range(x, len(item)):
                    if item[x] == "[" and item[y] == "]":
                        x = y
                        break
                    elif item[x] == "(" and item[y] == ")":
                        x = y
                        break
                    else:
                        pass
                    if y == len(item) - 1:
                        return False
                x = x + 1
    return True


def is_all_existing_symbol(val):
    for item in val:
        pattern = r"(?<=\()(.+?)(?=\))|(?<=\[)(.+?)(?=\])"
        prog = re.compile(pattern)
        s = prog.findall(item)
        num_unit = len(s)
        if item.count("||") == num_unit and num_unit != 0:
            return False
    return True


def is_existing_symbol_wrong_place(val):
    for item in val:
        pattern = r"(?<=\()(.+?)(?=\))|(?<=\[)(.+?)(?=\])"
        prog = re.compile(pattern)
        s = prog.findall(item)
        if not s and item[0] != "#":
            si = item
        else:
            si = []
            for i in s:
                x = list(filter(None, i))
                si.append(x[0].rstrip("||"))

        for x in si:
            if x.find("||") > -1:
                return False
    return True


# test
# if __name__=="__main__":
#     base_path = "/Users/tianchunlin1/timeline/9.17-9.21/"
#     tag_file = base_path + "tags.txt"
#     ptr_file = base_path + "test.txt"
#     tag, ptr = g.read_files(ptr_file, tag_file)
#     q = check(ptr)
#     print(q)
