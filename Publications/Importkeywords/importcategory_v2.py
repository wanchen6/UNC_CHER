#!/usr/bin/env python

import csv
import re
import xml.etree.ElementTree as etree

# Extract custom short title to ensure match with subtitle
# (rather than using citation metadata "Short Title")
def CDATA(string):
    return '[[CDATA[[' + string + ']]CDATA]]'

def indent(elem, level = 0):
    i = "\n" + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

category = input('Import author(a) or keywords(k)? ')
if category == 'a':
    fileInName = input('Author list: ')
elif category == 'k':
    fileInName = input('Keyword list: ')
else:
    print('Wrong category.')
    category = input('Import author(a) or keywords(k)? ')
    fileInName = input('Author/Keyword list: ')

rss = etree.Element('rss')
rss.set('version', '2.0')
rss.set('xmlns:excerpt', 'http://wordpress.org/export/1.2/excerpt/')
rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
rss.set('xmlns:wfw', 'http://wellformedweb.org/CommentAPI/')
rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
rss.set('xmlns:wp', 'http://wordpress.org/export/1.2/')
channel = etree.SubElement(rss, 'channel')
wxr_version = etree.SubElement(channel, 'wp:wxr_version')
wxr_version.text = '1.2'

with open(fileInName, 'r') as csvFile:

    def add_tag(key, value):
        if not value or value == '': return
        subelement = etree.SubElement(item, key)
        subelement.text = value

    def add_category(key, value):
        if not value or value == '': return
        subelement = etree.SubElement(item, key)
        subelement.text = value

    reader = csv.DictReader(csvFile)
    count = 0
    for row in reader:
        if row['Fullname'] == '': continue
        item = etree.SubElement(channel, 'item')
        add_tag('wp:post_type', 'post')
        add_tag('dc:creator', 'anonymous')
        add_tag('title', 'Not a real post')
        if category == 'a':
            category_tag = 'category domain="publication-authors" nicename="' + row['NiceName'] + '"'
        elif category == 'k':
            category_tag = 'category domain="publication-keywords" nicename="' + row['NiceName'] + '"'
        add_category(category_tag, CDATA(row['Fullname']))
        add_tag('content:encoded', CDATA(''))
        count += 1

csvFile.close()
indent(rss)
xmlString = etree.tostring(rss, encoding='utf-8').decode('utf-8')
xmlString = xmlString.replace('[[CDATA[[', '<![CDATA[')
xmlString = xmlString.replace(']]CDATA]]', ']]>')
if category == 'a':
    xmlString = re.sub('</category domain="publication-authors" nicename="'+"\S+"+'">','</category>',xmlString)
elif category == 'k':
    xmlString = re.sub('</category domain="publication-keywords" nicename="' + "\S+" + '">', '</category>', xmlString)

if xmlString != "":
    fileOutName = input('XML file:')
    with open(fileOutName, "w") as xmlFile:
        xmlFile.write(xmlString)
        print(str(count) + ' citations xml encoded to ' + fileOutName)
        xmlFile.close()
else:
    print(xmlString)
