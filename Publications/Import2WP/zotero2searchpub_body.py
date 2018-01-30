#!/usr/bin/env python3

"""Convert Zotero CSV export to WordPress XML import.

Customized for CHER website "SearchPub" custom post type.

version 1.1
2016 Dec 22

This script presumes a custom WordPress post-type 'SearchPub',
created with the WordPress 'Toolset Types' plugin.

Use:
python3 zotero2searchpub.py input.csv output.xml

Requires Python 3 for correct CSV processing.

Uses 'python-titlecase' libary:
https://github.com/ppannuto/python-titlecase
which can be installed with the command:
pip3 install titlecase

Title duplicates:
WordPress will not import posts with the same title and post date
(ignoring time of day). This script does not assign post dates, so the
importer defaults to current date. If you try to import two posts with
the same title on the same day, the WordPress importer will report an
error and not import the second post. This script detects title duplicates
and appends "(2)", "(3)", ... to the end. The title can be changed back
after import with the WordPress editor, and WordPress then will not care
about the identical duplication.
"""

import sys
import csv
import time
import calendar
import xml.etree.ElementTree as etree
from titlecase import titlecase

if sys.version_info[0] < 3:
    raise 'Must be using Python 3, try: python3 zotero2searchpub.py input.csv output.xml'

if len(sys.argv) < 2:
    print('Input file not specified, try: python3 zotero2searchpub.py input.csv output.xml')
    sys.exit()

if len(sys.argv) < 3:
    print('Output file not specified, try: python3 zotero2searchpub.py input.csv output.xml')
    sys.exit()

def extract_title(title_subtitle):
    """Extract title from 'Title: Substitle'.

    Based on colon separation convention.
    Use this function instead of metadata "Short Title" to ensure match with
    corresponding `subtitle()` function.
    """
    if ':' in title_subtitle:
        return titlecase(title_subtitle.split(':', 2)[0].strip())
    return titlecase(title_subtitle.strip())

def extract_subtitle(title_subtitle):
    """Extract subtitle from 'Title: Substitle'.
    
    Based on colon separation convention.
    Returns `None` if no colon exists.
    Ignores any colon after first colon.
    """
    if ':' in title_subtitle:
        subtitle = title_subtitle.split(':', 2)[1].strip()
        if len(subtitle) > 0:
            return titlecase(subtitle)
    return None

def cleanup_journal(journal):
    """Remove subtitle, year, 'The', whitespace. '&' to 'and'. Title case."""
    journal = journal            \
        .split(':', 2)[0]    \
        .split('/', 2)[0]    \
        .split('(', 2)[0]    \
        .replace('.', ' ')   \
        .replace('&', " and ")
    if journal.startswith('The '):
        journal = journal[4:]
    journal = ' '.join(journal.split())
    journal = titlecase(journal)
    return journal


def extract_name_list(zotero_name_list):
    """Convert Zotero name list to Python name list.
    
    Input is a string of semicolon separated 'Lastname, Firstname' names.
    Output is a Python list of 'Firstname Lastname' names.
    """
    names = []
    for name in zotero_name_list.split('; '):
        if ', ' in name:
            last_comma_first = name.split(', ', 2)
            first = last_comma_first[1].strip()
            last = last_comma_first[0].strip()
            names.append(first + " " + last)
        else:
            names.append(name.strip())
    return names

def extract_date(zotero_date):
    """Convert Zotero date string to Python Unix time.
    
    Defaults to 1st if day is missing.
    Defaults to January if month is missing.
    """
    length = len(zotero_date)
    if length == 10:
        date_format = '%Y-%m-%d'
    elif length == 7:
        date_format = '%Y-%m'
    elif length == 4:
        date_format = '%Y'
    else:
        return None
    return str(calendar.timegm(time.strptime(zotero_date, date_format)))

def extract_date_specificity(zotero_date):
    """Detect date specificity of Zotero date string.
    
    Returns 'ymd', 'ym', or 'y' string.
    """
    length = len(zotero_date)
    if length == 10:
        return 'ymd'
    elif length == 7:
        return 'ym'
    elif length == 4:
        return 'y'
    return None    

def extract_extra(zotero_extra_list, zotero_extra_key):
    """Extract value for key from Zotero key-value-string.

    Zotero 'Extra'' field stores data as a space separated string:
    'key1: value1 key2: value2 key3: value3'.
    This function extracts a value for a key from such a string. 
    """
    if zotero_extra_list is None or zotero_extra_key is None:
        return None
    words = zotero_extra_list.split(' ')
    for i in range(0, len(words)-1):
        if words[i] == zotero_extra_key + ':':
            return words[i+1]
    return None

def CDATA(string):
    """Temporarily wrap a string in a CDATA marker.
    
    Wraps a string in '[[CDATA[[' ']]CDATA]]' markers.
    For later conversion to '<![CDATA[' ']]>' markers,
    after XML conversion.
    """
    return '[[CDATA[[' + string + ']]CDATA]]'

def indent(elem, level = 0):
    """Prettify XML indenting."""
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

fileInName = sys.argv[1]

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

used_titles = {}
title_collision_did_occur = False

with open(fileInName, encoding='utf-8-sig') as csv_file:
    reader = csv.DictReader(csv_file)
    count = 0
    for row in reader:
        if row['Item Type'] == '': continue
        item = etree.SubElement(channel, 'item')
        def add_element(key, value):
            if not value or value == '': return
            subelement = etree.SubElement(item, key)
            subelement.text = value
        def add_taxonomy(taxonomy, name, slug):
            if not name or name == '' or not slug or slug == '': return
            category = etree.SubElement(item, 'category')
            category.set('domain', taxonomy)
            category.set('nicename', slug)
            category.text = name
        def add_meta(key, value):
            if not value or value == '': return
            postmeta = etree.SubElement(item, 'wp:postmeta')
            meta_key = etree.SubElement(postmeta, 'wp:meta_key')
            meta_key.text = key
            meta_value = etree.SubElement(postmeta, 'wp:meta_value')
            meta_value.text = value
        add_element('wp:post_type', 'searchpub')
        title = extract_title(row['Title'])
        while title in used_titles:
            use_count = used_titles[title] + 1
            used_titles[title] = use_count
            new_title = title + ' (' + str(use_count)  + ')'
            print('Title duplicate "' + title + '" changed to "' + new_title + '".')
            title_collision_did_occur = True
            title = new_title
        used_titles[title] = 1
        add_element('title', title)
        add_element('dc:creator', 'anonymous')
        add_meta('wpcf-searchpub-subtitle', extract_subtitle(row['Title']))
        add_meta('wpcf-searchpub-date', extract_date(row['Date']))
        add_meta('wpcf-searchpub-date-specificity', extract_date_specificity(row['Date']))
        for name in extract_name_list(row['Author']):
            slug = name.lower().replace('. ', '-').replace(' ','-')
            add_meta('wpcf-searchpub-ordered-authors', name)
            add_taxonomy('searchpub-author', name, slug)
        add_meta('wpcf-searchpub-publication', cleanup_journal(row['Publication Title']))
        add_meta('wpcf-searchpub-volume', row['Volume'])
        add_meta('wpcf-searchpub-issue', row['Issue'])
        add_meta('wpcf-searchpub-pages', row['Pages'])
        add_meta('wpcf-searchpub-doi', row['DOI'])
        add_meta('wpcf-searchpub-pmcid', extract_extra(row['Extra'], 'PMCID'))
        add_meta('wpcf-searchpub-url', row['Url'])
        add_meta('wpcf-searchpub-abstract', CDATA(row['Abstract Note']))
        search_list = (
            row['Title'], 
            row['Author'],
            row['Date'],
            row['Publication Title'], 
            row['Volume'],
            row['Issue'],
            row['Pages'],
            extract_extra(row['Extra'], 'PMCID'),
            row['Url'],
            row['Abstract Note'])
        search_string = '\n'.join(str(s) for s in search_list if s is not None)
        add_element('content:encoded', CDATA(search_string))
        count += 1

if title_collision_did_occur:
    print("Title duplicate changes can be changed back after WordPress import.")

indent(rss)
xmlString = etree.tostring(rss, encoding='utf-8')
xmlString = xmlString.replace('[[CDATA[['.encode(), '<![CDATA['.encode())
xmlString = xmlString.replace(']]CDATA]]'.encode(), ']]>'.encode())

fileOutName = sys.argv[2]
with open(fileOutName, "wb") as xmlFile:
    xmlFile.write(xmlString)
    print(str(count) + ' citations xml encoded to ' + fileOutName)
