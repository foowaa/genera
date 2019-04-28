# -*- coding: utf-8 -*-
"""
author: TIAN Chunlin
last update: 2018/9/10
"""

import codecs
import re
import copy
import itertools


def read_files(ptr_file, tag_file):
    """read_files read patterns.txt and tags.txt
    
    :param ptr_file: patterns file path
    :type ptr_file: string
    :param tag_file: tags file path
    :type tag_file: string
    :return: tag and ptr
    :rtype: dict dict
    """
    tag = {}
    tag_keys = []
    tag_values = []
    num_lines = 0

    for line in codecs.open(tag_file, "r", "utf8"):
        if line:
            if line[0] == "t":
                if len(tag_values) > 0:
                    tag[tag_keys[len(tag_keys) - 1]
                        ] = copy.deepcopy(tag_values)
                    tag_values.clear()
                else:
                    pass
                tag_keys.append(line.rstrip(":\n"))
            elif line == "\n":
                pass
            else:
                tag_values.append(line.rstrip("\n"))
        num_lines += 1
    tag[tag_keys[len(tag_keys) - 1]] = copy.deepcopy(tag_values)

    ptr = {}
    ptr_keys = []
    ptr_values = []
    num_lines = 0

    for line in codecs.open(ptr_file, "r", "utf-8"):
        if line:
            if line[0] == "p":
                if len(ptr_values) > 0:
                    ptr[ptr_keys[len(ptr_keys) - 1]
                        ] = copy.deepcopy(ptr_values)
                    ptr_values.clear()
                else:
                    pass
                ptr_keys.append(line.rstrip(":\n"))
            elif line == "\n" or line[0] == "#":
                pass
            else:
                ptr_values.append(line.rstrip(""))
        num_lines += 1
    ptr[ptr_keys[len(ptr_keys) - 1]] = copy.deepcopy(ptr_values)
    return tag, ptr


def extend_existing_items(ptr):
    """extend_existing_items [summary]
    
    :param ptr: [description]
    :type ptr: [type]
    """
    for key, item in ptr.items():
        temp_dict = []
        for _, item_ele in enumerate(item):
            pattern = r"(?<=\()(.+?)(?=\))|(?<=\[)(.+?)(?=\])"
            prog = re.compile(pattern)
            s = prog.findall(item_ele)

            si = []
            for i in s:
                x = list(filter(None, i))
                si.append(x[0])

            idx_extension = []
            ele_extension = []
            # 由于使用了或的正则表达式，得到的结果会产生两个并列的结构
            for idx, ele in enumerate(si):
                if len(ele) > 2 and ele.find("||") > -1:
                    # the existing extension
                    idx_extension.append(idx)
                    ele_extension.append(ele.rstrip("||"))
            if idx_extension:
                for i in range(len(idx_extension) + 1):
                    si = [e.rstrip("||") for e in si]
                    q = tuple(itertools.combinations(idx_extension, i))
                    if len(q) == 1 and len(q[0]) == 0:
                        temp = copy.deepcopy(si)
                        for j_idx, _ in reversed(list(enumerate(si))):
                            if j_idx in idx_extension:
                                del temp[j_idx]
                        new_item = concat_with_bracket(temp)
                        temp_dict.append(new_item)
                    else:
                        # idx = 0
                        for q_idx in q:
                            temp = copy.deepcopy(si)
                            for j_idx, _ in reversed(list(enumerate(si))):
                                if j_idx in idx_extension:
                                    if j_idx in q_idx:
                                        pass
                                    else:
                                        del temp[j_idx]
                            new_item = concat_with_bracket(temp)
                            temp_dict.append(new_item)
            else:
                temp_dict.append(item_ele)
        ptr[key] = temp_dict


def concat_with_bracket(list_of_str):
    temp1 = []
    for x in list_of_str:
        if x[0] == "t":
            temp1.append("[" + x + "]")
        else:
            temp1.append(x)
    temp2 = ["(" + x + ")" for x in temp1]
    sep = ""
    return sep.join(temp2)


#####


def gen_sentences(primitives, tag):
    p = []
    for primitive in primitives:
        s = expand(primitive, tag)
        temp = combine(s)
        p.append(temp)
    return p


def expand(primitive, tag):
    # http://deerchao.net/tutorials/regex/regex.htm
    pattern = r"(?<=\()(.+?)(?=\))|(?<=\[)(.+?)(?=\])"
    prog = re.compile(pattern)
    s = prog.findall(primitive)
    x = []
    if not s and primitive[0] != "#":
        x.append([primitive.rstrip("\n")])
    else:
        for ele in s:
            for i in ele:
                i = i.strip("|")
                if len(i) > 2 and i[0] == "t" and i.find("|") == -1:
                    temp = tag[i]
                    x.append(temp)
                elif len(i) > 2 and i.find("[t") > -1 and i.find("|") == -1:
                    i = i.lstrip("[")
                    i = i.rstrip("]")
                    temp = tag[i]
                    x.append(temp)
                elif i == "[*]":
                    continue
                elif i.find("#") > -1:
                    continue
                elif i.find("[T") > -1 or i.find("[n") > -1:
                    continue
                elif len(i) > 0:
                    if i.find("|") > -1:
                        i1 = i.split("|")
                        i2 = []
                        for item in i1:
                            if item[0] == "[":
                                item = item.lstrip("[")
                                item = item.rstrip("]")
                                temp = tag[item]
                                for j in temp:
                                    i2.append(j)
                            else:
                                i2.append(item)
                        x.append(i2)
                    else:
                        temp = []
                        temp.append(i)
                        x.append(temp)
                else:
                    pass
    return x


def combine(s):
    # generate: using Descartes product
    # FIXED: 2018/9/12
    c = Descartes_product(s)
    result = []
    sep = ""
    for e in c:
        temp = sep.join(e)
        result.append(temp)
    return result


def Descartes_product(args):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    repeat = 1
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


def flatten(list_of_):
    return sum(list_of_, [])


def main():
    base_path = "/Users/tianchunlin1/timeline/9.17-9.21/"
    tag_file = base_path + "tags.txt"
    ptr_file = base_path + "intentions_table_v4.txt"
    tag, ptr = read_files(ptr_file, tag_file)
    extend_existing_items(ptr)
    with open(
        "/Users/tianchunlin1/timeline/9.17-9.21/intention_test.txt",
        "w",
        encoding="utf8",
    ) as f:
        separator = "|"
        for key, item in ptr.items():
            if key is not None:
                s = gen_sentences(item, tag)
                s_saved = separator.join(flatten(s))
                f.writelines([key + "," + s_saved + "\n"])


if __name__ == "__main__":
    main()
