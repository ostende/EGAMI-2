# uncompyle6 version 2.13.2
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
# [GCC 5.4.0 20160609]
# Embedded file name: /usr/lib/enigma2/python/Tools/LXMLTools.py
# Compiled at: 2017-10-02 01:52:09


def elementsWithTag(el, tag):
    if isinstance(tag, str):
        s = tag
        tag = lambda x: x == s
    for x in el:
        if not x.tag:
            continue
        if tag(x.tag):
            yield x


def mergeText(nodelist):
    rc = ''
    for node in nodelist:
        if node.text:
            rc = rc + node.text

    return rc


def stringToXML(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace("'", '&apos;').replace('"', '&quot;')