# -*- coding: utf-8 -*-
# Pseudocode of news posting of CHER
# Convert pseudocode to Python code

import csv, sys, time, os
from datetime import date
from datetime import timedelta
from datetime import datetime
import tkinter, tkinter.filedialog
import html
from operator import itemgetter

funding_inst = ''

class htmlGenerater:
    def __init__(self):
        # Create the main window widget.
        self.main_window = tkinter.Tk()

        # Create the widgets in first row and format them
        self.select_file_button = tkinter.Button(self.main_window, text='Select a file', width=18, bg = "lightblue", font = "Calibri 10 bold", command=self.select_file).grid(row=0, column=0, padx=5, pady=8)
        self.file_name = tkinter.StringVar()
        self.file_name_label = tkinter.Label(self.main_window, textvariable=self.file_name, width=40, fg="black").grid(row=0, column=1, padx=5, pady=8)  # Label to display selected file name

        # Create the widgets in second row and format them
        self.html_button = tkinter.Button(self.main_window, text='Develop HTML', width=18, bg = "lightblue", font = "Calibri 10 bold", command=self.create_html).grid(row=2, column=0, padx=5, pady=8)
        self.html_name = tkinter.StringVar()
        self.html_name_label = tkinter.Label(self.main_window, textvariable=self.html_name, width=40, fg="black").grid(row=2, column=1, padx=5, pady=8)  # Label to display frequency value

        # Enter the tkinter main loop
        tkinter.mainloop()

    # When user clicks 'Select a file' button, this function is called to open a file dialog and obtain the file name
    def select_file(self):
        # Set options for this file dialog
        self.file_opts = options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('text files', '.csv')]
        options['title'] = 'File Selector'

        # The askopenfilename function opens the file dialog and returns the name of the file the user selected
        filename = tkinter.filedialog.askopenfilename(**self.file_opts)
        # Remove directory path information
        index = filename.rfind('/')
        if index >= 0:
            filename = filename[index+1:]
        # Set the value of the file name if one was selected, else display a message
        if filename:
            self.file_name.set(filename)
        else:
            self.file_name.set('No file was selected')

    def create_html(self):
        # Initiate HTML
        html_head = '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t\t<link rel="Stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600">\n\t\t<!--[if !mso]><\!--><style>\n\t\t\t#event tr:nth-child(even){background-color: #f2f2f2;}\n\t\t\t.donate tr {height: 250px;}\n\t\t</style>\n\t\t<!-- <![endif]-->\n\t\t<!--[if (gte mso 9)|(IE)]>\n\t\t<style>\n\t\t\t.date-div {\n\t\t\t\tborder: #56a0d3 2px solid !important;}\n\t\t</style>\n\t\t<![endif]-->\n\t\t<style>\n\t\t\ta {\n\t\t\t\tcolor: #56a0d3;\n\t\t\t\tfont-weight: 400;\n\t\t\t\ttext-decoration: none;}\n\t\t\ta:hover {\n\t\t\t\tcolor: #2F5597;}\n\t\t\ta img:hover {\n\t\t\t\topacity: 0.8;}\n\t\t\t.header-img-small {\n\t\t\t\tdisplay: none;}\n\t\t\t#canspamBarWrapper {\n\t\t\t\tbackground-color: #333;}\n\t\t\t.donate tr {\n\t\t\t\tbackground: linear-gradient(to right, rgba(255,255,255,0.7), rgba(255,255,255,0) 40%), url(https://cher.unc.edu/files/2016/09/iStock_99601497_XXLARGE-e1476727779129.jpg);\n\t\t\t\tbackground-repeat: no-repeat;\n\t\t\t\tbackground-size: cover;\n\t\t\t\tbackground-position: center center;}\n\t\t\t.donate a {\n\t\t\t\twidth: 250px;}\n\t\t\t#associate table, #funding table {\n\t\t\t\tborder-bottom: 2px #f2f2f2 solid;}\n\t\t\t@media only screen and (max-width: 1500px) {\n\t\t\t\t.news-title {\n\t\t\t\t\tfont-size:1.8em !important;}\n\t\t\t\t.title,\n\t\t\t\t.location-award,\n\t\t\t\t.date {\n\t\t\t\t\tfont-size:1em !important;\n\t\t\t\t\tmargin:0 !important;}\n\t\t\t\t.abstract {\n\t\t\t\t\tfont-size:0.9em !important;}\n\t\t\t\t\t}\n\t\t\t@media only screen and (max-width: 50em) {\n\t\t\t\t.news-title[style] {\n\t\t\t\t\tfont-size: 1.5em !important;}\n\t\t\t\t.title[style]{\n\t\t\t\t\tfont-size:1em !important;}\n\t\t\t\t\t.date[style],\n\t\t\t\t.location-award[style],\n\t\t\t\t.abstract[style]{\n\t\t\t\t\tfont-size: 0.8em !important;\n\t\t\t\t\tfont-weight:300 !important;}\n\t\t\t\t.donate img, .donate a {\n\t\t\t\t\twidth: 200px;}\n\t\t\t\t.donate td {\n\t\t\t\t\tvertical-align: bottom;}\n\t\t\t\t.event-date{\n\t\t\t\t\twidth: 10%;\n\t\t\t\t\tpadding-left:0;}\n\t\t\t\t.event-image{\n\t\t\t\t\twidth: 30%;}\n\t\t\t\t.event-date {\n\t\t\t\t\tfont-size: 0.8em;\n\t\t\t\t\tvertical-align: top;}\n\t\t\t\t.date-div {\n\t\t\t\t\twidth: 100% !important;\n\t\t\t\t\tmargin-top: 10px;}\n\t\t\t\t.date-div div{\n\t\t\t\t\tpadding:0 !important;}\n\t\t\t\t.event-content .abstract {\n\t\t\t\t\tdisplay:none;}\n\t\t\t\t.social-icon img {\n\t\t\t\t\twidth: 40px;}}\n\t\t\t@media only screen and (max-width: 30em) {\n\t\t\t\t.header-img-large {\n\t\t\t\t\tdisplay: none !important;}\n\t\t\t\t.header-img-small {\n\t\t\t\t\tdisplay: block;}\n\t\t\t\t.social-icon {\n\t\t\t\t\tbottom: 2% !important;}\n\t\t\t\t.news-nav[style] {\n\t\t\t\t\tfont-size:14px !important;}\n\t\t\t\t.donate img, .donate a {\n\t\t\t\t\twidth: 150px;}\n\t\t\t\t.event-title{\n\t\t\t\t\tmargin-left: 20px;}\n\t\t\t\t#event{\n\t\t\t\t\tmargin: 0 !important;}\n\t\t\t\t#event h1 {\n\t\t\t\t\tmargin-left: 0 !important;\n\t\t\t\t\tmargin-right: 0 !important;}\n\t\t\t\t.more-event {\n\t\t\t\t\tmargin-right: 20px}\n\t\t\t\t.event-date {\n\t\t\t\t\twidth:20%;padding-left:10px;}\n\t\t\t\t.event-content {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\twidth: 90%;}\n\t\t\t\t.event-image {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\twidth: 90%;}\n\t\t\t\t#associate td, #funding td {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\twidth: 100%;}\n\t\t\t\t#associate .image, #funding .image {\n\t\t\t\t\twidth: 80%;}\n\t\t\t}\n\t\t</style>\n\t</head>'
        html_foot = '\n\t\t\t\t<div style="margin-top: 1em;margin-right: 20px;text-align: right">\n\t\t\t\t\t<a href="https://cher.unc.edu/news-announcements/" target="_blank"><img src="https://cher.unc.edu/files/2017/03/more-funding.png" width="300"></a>\n\t\t\t\t</div>\n\t\t\t<!--[if mso]>\n\t\t\t<table border="0" cellpadding="8" cellspacing="0" width="100%"><tbody><tr bgcolor="#56a0d3"><td>\n\t\t\t<![endif]-->\n\t\t\t<div class="news-nav" style="margin:0;background-color: #56a0d3;text-align: center;padding: 10px;color: #fff;clear: both;font-size: 20px;">\n\t\t\t\t<a href="#associate" style="text-decoration: none; color: #fff;">CHER News</a> | \n\t\t\t\t<a href="#event" style="text-decoration: none; color: #fff;">Events</a> | \n\t\t\t\t<a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a>\n\t\t\t</div>\n\t\t\t<!--[if mso]>\n\t\t\t</td></tr></tbody></table>\n\t\t\t<![endif]-->\n\t\t\t<center style="background-color: #333">\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%" bgcolor="#333" id="canspamBarWrapper">\n\t\t\t\t\t<tr><td align="center">\n\t\t\t\t\t\t<img alt="UNC CHER" width="250" src="https://cher.unc.edu/files/2015/05/Center-for-Health-Equity-Research_White-4.png">\n\t\t\t\t\t</td></tr>\n\t\t\t\t\t<tr ><td align="center">\n\t\t\t\t\t\t<h2 style="margin: 0.5em 0;color: #fff; font-size: 1.2em;font-weight:300;">Innovation | Equity | Collaboration</h2>\n\t\t\t\t\t</td></tr>\n\t\t\t\t\t<tr><td align="center">\n\t\t\t\t\t\t<div>\n\t\t\t\t\t\t\t<a target="_blank" style="margin-right: 10px" href="https://www.facebook.com/cher.unc.edu"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/facebook_circle.png"></a>\n\t\t\t\t\t\t\t<a target="_blank" style="margin-right: 10px" href="https://twitter.com/uncCHER"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/twitter_circle.png"></a>\n\t\t\t\t\t\t\t<a target="_blank" href="https://plus.google.com/u/0/113618129434863244332"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/google_circle.png"></a>\n\t\t\t\t\t\t</div>\n\t\t\t\t\t</td></tr>\n\t\t\t\t\t<tr>\n\t\t\t\t\t\t<td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;">\n\t\t\t\t\t\t<table border="0" cellpadding="0" cellspacing="0" id="canspamBar">\n\t\t\t\t\t\t\t<tr><td align="center" valign="top" style="color:#fff; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;">This email was sent to <a href="mailto:*|EMAIL|*" target="_blank" style="color:#56a0d3 !important;">*|EMAIL|*</a><br><a href="*|ABOUT_LIST|*" target="_blank" style="color:#fff !important;"><em>why did I get this?</em></a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="*|UNSUB|*" style="color:#56a0d3 !important;"><em>unsubscribe</em></a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="*|UPDATE_PROFILE|*" style="color:#fff !important;">update subscription preferences</a><br>*|LIST:ADDRESSLINE|*<br><br>*|REWARDS|*</td>\n\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t</table>\n\t\t\t\t\t</td>\n\t\t\t\t\t</tr>\n\t\t\t\t</table>\n\t\t\t\t<style type="text/css">\n\t\t\t\t\t@media only screen and (max-width: 480px){\n\t\t\t\t\ttable#canspamBar td{font-size:14px !important;}\n\t\t\t\t\ttable#canspamBar td a{display:block !important; margin-top:10px !important;}}\n\t\t\t\t</style>\n\t\t\t</center>'
        # Locate the CSV and read it
        filename = self.file_name.get()
        inst = self.readInst()

        # Call read_content
        try:
            with open(filename, 'r', encoding='utf-8', newline='', errors='replace') as csvfile:
                funding_file = 'Tablepress_import_WZ_' + datetime.today().strftime("%m.%d.%y") + '.csv'
                funding_csv = open(funding_file, 'w', newline='',)
                fieldnames = ['Institution', 'Funding', 'Application Due Date', 'Amount of Funding']
                writer = csv.DictWriter(funding_csv, fieldnames=fieldnames)
                writer.writeheader()
                csv_content = csv.DictReader(csvfile, delimiter = ',')
                csv_content = list(csv_content)
                csv_content = self.sortEvent(csv_content) + self.sortNews(csv_content) + self.sortFunding(csv_content) + self.sortFundingAbstract(csv_content)
                print(len(csv_content))
                html_body_email, html_body_wordpress = self.read_content(csv_content, inst, writer)
            csvfile.close()
            if html_body_email == None or html_body_wordpress == None:
                html_body_email = '<body></body>'
                html_body_wordpress = '<body></body>'
            else:
                html_body_email = '''\n\t<body style="margin:0; font:300 1em/2em 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; color:#666; text-decoration: none; background-color: #333">\n\t\t<div style="max-width: 1000px; margin:auto; background-color: #fff">\n\t\t\t<!--[if (gte mso 9)|(IE)]><table border="0" cellspacing="0" cellpadding="5" width="100%"><tr><td align="center">\n\t\t\t<![endif]-->\n\t\t\t<div style="width:100%;text-align:center;margin: 0;">\n\t\t\t\t<a href="*|ARCHIVE|*" style="text-decoration: none; color: #56a0d3; font-size: 12px; ">This email contains images. View this email in your browser.</a>\n\t\t\t</div>\n\t\t\t<!--[if (gte mso 9)|(IE)]></td>\n\t\t\t\t<td align="right"><a target="_blank" style="display:inline-block; margin-right: 10px" href="https://www.facebook.com/cher.unc.edu"><img width="40" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/facebook_circle.png"></a></td>\n\t\t\t\t<td align="right"><a target="_blank" style="display:inline- block; margin-right: 10px" href="https://twitter.com/uncCHER"><img width="40" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/twitter_circle.png"></a></td>\n\t\t\t\t<td align="right"><a target="_blank" style="display:inline-block" href="https://plus.google.com/u/0/113618129434863244332"><img width="40" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/google_circle.png"></a></td>\n\t\t\t\t<td width="1"></td></tr>\n\t\t\t</table>\n\t\t\t<![endif]-->\n\t\t\t<div class="news-header" style="position: relative; overflow: hidden; max-width:1000px;">\n\t\t\t\t<table border="0" cellspacing="0" cellpadding="0" align="center" width="100%">\n\t\t\t\t\t<tbody>\n\t\t\t\t\t\t<tr class="header-img-large"><td><img src="https://cher.unc.edu/files/2017/03/cher-newsletter-bg.png" width="100%" alt="newsletter background" style="width: 100%; max-width:1000px;display:block;"></td></tr>\n\t\t\t\t\t\t<tr class="header-img-small"><td><img src="https://cher.unc.edu/files/2017/03/cher-newsletter-bg-small.png" width="100%" alt="newsletter background" style="width: 100%;max-width:1000px;display:block;"></td></tr>\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t\t<!--[if !mso]><\!--><div class="social-icon-large social-icon" style="position: absolute; left: 2%; bottom: 10%">\n\t\t\t\t\t<a target="_blank" style="display:inline-block; margin-right: 10px" href="https://www.facebook.com/cher.unc.edu"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/facebook_circle.png"></a>\n\t\t\t\t\t<a target="_blank" style="display:inline- block; margin-right: 10px" href="https://twitter.com/uncCHER"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/twitter_circle.png"></a>\n\t\t\t\t\t<a target="_blank" style="display:inline-block" href="https://plus.google.com/u/0/113618129434863244332"><img width="50" alt="UNC CHER" src="https://cher.unc.edu/files/2017/03/google_circle.png"></a>\n\t\t\t\t</div><!-- <![endif]-->\n\t\t\t</div>\n\t\t\t<!--[if mso]>\n\t\t\t<table border="0" cellpadding="8" cellspacing="0" width="100%"><tbody><tr bgcolor="#56a0d3"><td>\n\t\t\t<![endif]-->\n\t\t\t<div class="news-nav" style="margin:0;background-color: #56a0d3;text-align: center;padding: 10px;color: #fff;clear: both;font-size: 20px;">\n\t\t\t\t<a href="#associate" style="text-decoration: none; color: #fff;">CHER News</a> | \n\t\t\t\t<a href="#event" style="text-decoration: none; color: #fff;">Events</a> | \n\t\t\t\t<a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a>\n\t\t\t</div>\n\t\t\t<!--[if mso]>\n\t\t\t</td></tr></tbody></table>\n\t\t\t<![endif]-->''' + html_body_email + html_foot + '\n\t\t</div>\n\t</body>\n</html>'

            # Combine the HTML text together
            html_doc_email = html_head + html_body_email
            html_doc_wordpress = html_body_wordpress

            # Print the whole HTML out in 2 versions: email, wordpress
            output_path_email = filename[:-4] + '_email.html'
            f = open(output_path_email, 'w', errors='ignore')
            f.write(html_doc_email)  # Without prettify, symbol will be removed by the beautifysoup
            f.close()
            output_path_wp = filename[:-4] + '_wp.html'
            f = open(output_path_wp, 'w', errors='ignore')
            f.write(html_doc_wordpress)  # Without prettify, or <br> will be generated by WP
            f.close()
            self.html_name.set(output_path_email+'\n'+output_path_wp+'\n'+funding_file)

        except FileNotFoundError as err:
            print('Cannot find the file.')
            print(err)

        except OSError as err:
            print('Error: An error occurred trying to read the file.')
            print(err)

        except ValueError as err:
            print('Error: Unicode error occurs when reading the file.')
            print(err)

            # except Exception as err:  # an exception was raised, but not IOError or ValueError
            # print('An error occurred.')
            # print(err)

    # Search content in dictionary
    def search(self, myDict, searchFor):
        for row in myDict:
            values = row.values()
            if searchFor in values:
                return True
        return False

    # Sort the csv file by category
    def sortEvent(self, csv_content):
        #csv_content_filter_event = [x for x in csv_content if x['category'] == 'CHER Event' or x['category'] == 'External Event']
        csv_content_filter_event = filter(lambda x: x['category'] == 'CHER Event' or x['category'] == 'External Event', csv_content)
        csv_content_filter_event = sorted(csv_content_filter_event, key=itemgetter('category','event_start','event_end'))
        return csv_content_filter_event

    # Sort the csv file by category
    def sortNews(self, csv_content):
        #csv_content_filter_news = [y for y in csv_content if y['category'] == 'CHER News' or y['category'] == 'CHER Publication']
        csv_content_filter_news = filter(lambda x: x['category'] == 'CHER News' or x['category'] == 'CHER Publication', csv_content)
        csv_content_filter_news = sorted(csv_content_filter_news, key=itemgetter('category','post_date'), reverse=True)
        return csv_content_filter_news

    # Sort the csv file by category
    def sortFundingAbstract(self, csv_content):
        csv_content_filter_fa = filter(lambda x: x['category'] == 'Funding Abstract', csv_content)
        csv_content_filter_fa = sorted(csv_content_filter_fa, key=itemgetter('institution','dead_date'))
        return csv_content_filter_fa

    # Sort the csv file by category
    def sortFunding(self, csv_content):
        csv_content_filter_f = filter(lambda x: x['category'] == 'Funding', csv_content)
        csv_content_filter_f = sorted(csv_content_filter_f, key=lambda x: x['dead_date'])
        return csv_content_filter_f

    # Read institution into dict
    def readInst(self):
        inst_dict = {}
        filename = 'institution.csv'
        with open(filename, 'r', newline='') as csvfile:
            csv_content = csv.DictReader(csvfile)
            for row in csv_content:
                name = row['institution']
                inst_dict[name] = row['url']
        csvfile.close()
        return inst_dict

    def try_parsing_date(self, text):
        for fmt in ('%Y-%m-%d', '%m/%d/%y', '%m/%d/%Y'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')

    def fundingWriter(self):

        return writer

    # Find the content needed and write HTML
    def read_content(self, csv_content, inst, writer):
        content_html = ''
        event_html_headline = '\n\t\t\t<table class="donate" border="0" cellpadding="0" cellspacing="0" width="100%">\n\t\t\t\t<tbody><tr>\n\t\t\t\t\t<!--[if mso]><td><a href="http://giving.unc.edu/gift/custom/index.htm?fndpic=305530" target="_blank"><img src="https://cher.unc.edu/files/2017/05/newsletter-donate.png" width="100%"></a></td><![endif]-->\n\t\t\t\t\t<!--[if !mso]><\!--><td align="center" width="40%"><a href="http://giving.unc.edu/gift/custom/index.htm?fndpic=305530" target="_blank"><img width="250" src="https://cher.unc.edu/files/2017/05/donate-button.png"></a></td>\n\t\t\t\t\t<td width="60%"></td><!-- <![endif]-->\n\t\t\t\t</tr></tbody>\n\t\t\t</table>\n\t\t\t<table border="0" cellpadding="10" cellspacing="0" width="100%" style="font-weight:400; color: #fff; font-size: 24px;"><tbody><tr bgcolor="#aed2ea"><td><div style="margin-left: 10px">Other Resources</div></td></tr></tbody></table>\n\t\t\t<section id="event" style="margin: 0 20px;">\n\t\t\t\t<div class="event-title"><h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Upcoming Events</h1></div>\n\t\t\t\t<table border="0" cellspacing="0" cellpadding="10" align="left" width="100%">\n\t\t\t\t\t<tbody>'
        event_html_wp_headline = '[tab title="Upcoming Events"]'
        event_html = ''
        event_html_wp = ''
        funding_html_headline = '\n\t\t\t<section id="funding" class="offset" style="margin: 0 20px;">\n\t\t\t\t<div style="padding-top: 1em;border-top: #D9D9D9 1px solid;clear: both"></div><h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Funding Opportunities</h1>'
        funding_html_wp = '[tab title="Funding Opportunities"]<div class="funding-table">[table id=1 /]</div>[/tab]'
        funding_html = ''
        funding_abstract_html = '<section id="funding-list" class="offset" style="margin: 0 20px;">'
        associate_html = '\n\t\t\t<section id="associate" class="offset" style="margin: 0 20px;">'
        associate_html_wp = '[tab title="Our Associates" active="active"]'
        news_html_headline = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER News</h1>'
        news_html_wp_headline = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER News</h1>'
        news_html = ''
        news_html_wp = ''
        wip_html = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER Events</h1>'
        wip_html_wp = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER Events</h1>'
        pub_html = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Recent Publications</h1>'
        pub_html_wp = '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Recent Publications</h1>'

        # Set Counter for each section
        event_counter = 0
        funding_counter = 0
        funding_abstract_counter = 0

        # Read CSV
        for row in csv_content:
            id_content = row['ResponseID']
            try:
                headline_content = row['headline']
            except:
                headline_content = ''
            title_content = row['title']
            if row['institution'] == 'Other institution not in the list':
                institution_content = row['institution_info-Institution Name']
                inst_url_content = row['institution_info-URL']
            else:
                institution_content = row['institution']
                inst_url_content = inst[institution_content]
            location_content = row['location']
            post_date_content = row['post_date']
            dead_url_content = row['dead_url']
            dead_date_content = row['dead_date']
            apply_date_content = row['apply_date']
            event_start_content = row['event_start']
            event_end_content = row['event_end']
            post_url_content = row['post_url']
            category_content = row['category']
            award_amt_content = row['award_amt']
            img_url_content = row['img_url']
            final_txt_content = row['final_txt'].replace('/ ', '<br>')

            # Determine if we want to hide the information of this row
            if category_content == 'External Event':
                end_date = self.try_parsing_date(event_end_content).date()
                try:
                    event_start_date = self.try_parsing_date(event_start_content).date()
                except:
                    event_start_date = end_date
                if post_date_content != "":
                    post_date = self.try_parsing_date(post_date_content).date()
                else:
                    post_date = date.today()
                if event_start_date <= date.today() and headline_content != 'Y':
                    # break current loop
                    continue
                else:
                    # Add event to WordPress
                    # Add div
                    div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html_wp = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add image and abstract
                    final_txt_content = html.unescape(final_txt_content)
                    if img_url_content == '':
                        abstract_html_wp = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>'
                    else:
                        abstract_html_wp = '\n\t\t\t\t<span>\n\t\t\t\t\t<img class="image" src="' + img_url_content + '"  style="max-width: 33%; min-width:auto; max-height: 200px; height: auto; float: left; margin-bottom: 1em; margin-right: 1em;">\n\t\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t</span>'

                    # Add div
                    div_down_html = '\n\t\t\t</div>\n\t\t\t<div style="padding-top: 1em; border-top: #D9D9D9 1px solid; clear: both;"></div>'

                    # Add title
                    title_html = '\n\t\t\t\t\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add date
                    try:
                        start_date = self.try_parsing_date(event_start_content).date()
                        start_date_month_short = start_date.strftime('%b')
                        start_date_short = start_date.strftime('%d').replace(' 0', ' ')
                        # Add date in table
                        tr_top_html = '\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<td class="event-date" align="center" width="15%">\n\t\t\t\t\t\t\t\t<table class="date-div" cellspacing="0" cellpadding="1" align="center" width="60%" style="border: #56a0d3 4px solid">\n\t\t\t\t\t\t\t\t\t<tbody>\n\t\t\t\t\t\t\t\t\t\t<tr><td align="center" bgcolor="#fff" style="color: #56a0d3;font-weight: 500;">' + start_date_month_short + '</td></tr>\n\t\t\t\t\t\t\t\t\t\t<tr><td align="center" bgcolor="#56a0d3" style="color: #fff;font-weight: 500;">' + start_date_short + '</td></tr>\n\t\t\t\t\t\t\t\t\t</tbody>\n\t\t\t\t\t\t\t\t</table>\n\t\t\t\t\t\t\t</td>'
                        if event_start_content != event_end_content:
                            start_date_month = start_date.strftime('%B')
                            end_date_month = end_date.strftime('%B')
                            start_date_year = start_date.strftime('%Y')
                            end_date_year = end_date.strftime('%Y')
                            if (start_date_month != end_date_month) and (start_date_year == end_date_year):
                                start_date = start_date.strftime('%B %d - ').replace(' 0', ' ')
                                end_date = end_date.strftime('%B %d, %Y').replace(' 0',' ')
                            elif (start_date_month != end_date_month) and (start_date_year != end_date_year):
                                start_date = start_date.strftime('%B %d, %Y - ').replace(' 0', ' ')
                                end_date = end_date.strftime('%B %d, %Y').replace(' 0', ' ')
                            else:
                                start_date = start_date.strftime('%B %d - ').replace(' 0', ' ')
                                end_date = end_date.strftime(' %d, %Y').replace(' 0','')
                            event_date = start_date + end_date
                        else:
                            event_date = self.try_parsing_date(event_start_content).date().strftime('%B %d, %Y ').replace(' 0',' ')
                        date_html = '\n\t\t\t\t\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_date + '</h3>'
                    except:
                        date_html = '\n\t\t\t\t\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_start_content + '</h3>'

                    # Add location or award
                    location_award_html = '\n\t\t\t\t\t\t\t\t<h3 class="location-award" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + location_content + '</h3>'

                    # Add abstract
                    final_txt_content = html.unescape(final_txt_content)
                    abstract_html = '\n\t\t\t\t\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t\t\t\t</td>'

                    # Add image and title
                    if img_url_content == '':
                        image_html = ''
                        title_html = '\n\t\t\t\t\t\t\t<td class="event-content" align="left" valign="top" colspan="2">' + title_html
                    else:
                        image_html = '\n\t\t\t\t\t\t\t<td class="event-image" align="center" width="20%">\n\t\t\t\t\t\t\t\t<img width="100%" src="' + img_url_content + '" alt="' +institution_content+'">\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>'
                        title_html = '\n\t\t\t\t\t\t\t<td class="event-content" align="left" valign="top" width="65%">' + title_html

                    # Combine all events together for website
                    if headline_content == 'Y':
                        event_html_wp_headline = event_html_wp_headline + div_top_html + title_html_wp + date_html + location_award_html + abstract_html_wp + div_down_html
                    else:
                        event_html_wp = event_html_wp + div_top_html + title_html_wp + date_html + location_award_html + abstract_html_wp + div_down_html

                    # Combine events for email
                    if event_counter < 5 and post_date > date.today() - timedelta(days=15):
                        if headline_content == 'Y':
                            event_html_headline = event_html_headline + tr_top_html + title_html + date_html + location_award_html + abstract_html + image_html
                        else:
                            event_html = event_html + tr_top_html + title_html + date_html + location_award_html + abstract_html + image_html
                        # event counter increase by 1
                        event_counter = event_counter + 1

            elif category_content == 'CHER Event':
                end_date = self.try_parsing_date(event_end_content).date()
                if end_date <= date.today() and headline_content != 'Y':
                    # break current loop
                    continue
                else:
                    # Add div
                    div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add date
                    try:
                        if event_start_content != event_end_content:
                            start_date = self.try_parsing_date(event_start_content).date()
                            start_date_month = start_date.strftime('%B')
                            end_date_month = end_date.strftime('%B')
                            start_date_year = start_date.strftime('%Y')
                            end_date_year = end_date.strftime('%Y')
                            if (start_date_month != end_date_month) and (start_date_year == end_date_year):
                                start_date = start_date.strftime('%B %d - ').replace(' 0', ' ')
                                end_date = end_date.strftime('%B %d, %Y').replace(' 0',' ')
                            elif (start_date_month != end_date_month) and (start_date_year != end_date_year):
                                start_date = start_date.strftime('%B %d, %Y - ').replace(' 0', ' ')
                                end_date = end_date.strftime('%B %d, %Y').replace(' 0', ' ')
                            else:
                                start_date = start_date.strftime('%B %d - ').replace(' 0', ' ')
                                end_date = end_date.strftime(' %d, %Y').replace(' 0','')
                            event_date = start_date + end_date
                        else:
                            event_date = self.try_parsing_date(event_start_content).date().strftime('%B %d, %Y ').replace(' 0',' ')
                        date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_date + '</h3>'
                    except:
                        date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_start_content + '</h3>'

                    # Add location or award
                    location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + location_content + '</h3>'

                    # Add image and abstract
                    final_txt_content = html.unescape(final_txt_content)
                    if img_url_content == '':
                        abstract_html = '\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                    else:
                        abstract_html ='\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="25%" align="center"><img width="100%" class="image" src="'+ img_url_content +'" style="min-width: 180px; display: block;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                        abstract_html_wp = '\n\t\t\t\t<table class="news-content" border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="20%" align="center"><img width="100%" class="image" src="' + img_url_content + '" style="min-width: 180px; display: block;max-height: 250px;width: auto;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin-left: 10px; font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p></td>\n\t\t\t\t</tr></tbody></table>'

                    # Add div
                    div_down_html = '\n\t\t\t\t</div>'

                    # Combine events together
                    wip_html = wip_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                    wip_html_wp = wip_html_wp + div_top_html + title_html + date_html + location_award_html + abstract_html_wp + div_down_html

            elif category_content == 'Funding':
                if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                    dead_date = self.try_parsing_date(dead_date_content).date()
                    if post_date_content != "":
                        post_date = self.try_parsing_date(post_date_content).date()
                    else:
                        post_date = date.today()
                    if dead_date <= date.today() and headline_content != 'Y':
                        # break current loop
                        continue

                if award_amt_content.isdigit():
                    award_amt_content = '${:,.0f}'.format(float(award_amt_content))

                # Write funding in csv for Tablepress
                writer.writerow({'Institution': "<a href="+inst_url_content+"' target='_blank'>"+institution_content+"</a>", 'Funding': "<a href='"+post_url_content+"' target='_blank'>"+title_content+"</a><br>"+final_txt_content+"<br><a href='"+dead_url_content+"' target='_blank'>Register Now</a>",'Application Due Date': dead_date.strftime('%B %d, %Y').replace(' 0', ' '),'Amount of Funding': award_amt_content})

                if funding_counter > 3 or post_date > date.today() - timedelta(days=15):
                    # break current loop
                    continue

                if final_txt_content != '':
                    # Add div
                    div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none;  color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add date
                    date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">Deadline: ' + dead_date_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color:#56a0d3;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Apply Now</a></h3>'

                    # Add location or award
                    location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">Funding: ' + award_amt_content + '</h3>'

                    # Add image and abstract
                    final_txt_content = html.unescape(final_txt_content)
                    if img_url_content == '':
                        abstract_html = '\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                    else:
                        abstract_html ='\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="25%" align="center"><img width="100%" class="image" src="'+ img_url_content +'" style="min-width: 180px; display: block;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'

                    # Add div
                    div_down_html = '\n\t\t\t\t</div>'

                    # Combine funding for email
                    if headline_content == 'Y':
                        funding_html_headline = funding_html_headline + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                    else:
                        funding_html = funding_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                    # funding counter increase by 1
                    funding_counter = funding_counter + 1

            elif category_content == 'Funding Abstract':
                if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                    dead_date = self.try_parsing_date(dead_date_content).date()
                    if post_date_content != "":
                        post_date = self.try_parsing_date(post_date_content).date()
                    else:
                        post_date = date.today()
                    if dead_date <= date.today() and headline_content != 'Y':
                        # break current loop
                        continue

                if award_amt_content.isdigit():
                    award_amt_content = '${:,.0f}'.format(float(award_amt_content))

                # Write funding in csv for Tablepress
                writer.writerow({'Institution': "<a href="+inst_url_content+"' target='_blank'>"+institution_content+"</a>", 'Funding': "<a href='"+post_url_content+"' target='_blank'>"+title_content+"</a><br><a href='"+dead_url_content+"' target='_blank'>Register Now</a>",'Application Due Date': dead_date.strftime('%B %d, %Y').replace(' 0', ' '),'Amount of Funding': award_amt_content})

                if funding_abstract_counter > 2 or post_date < date.today() - timedelta(days=30):
                    # break current loop
                    continue

                global funding_inst
                # Add div
                div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                if institution_content == funding_inst:
                    # Add funding abstract
                    abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em; margin:0;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + dead_date_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Apply Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                    # Add div
                    div_down_html = '\n\t\t\t</div>'

                    # Combine funding for email
                    funding_abstract_html = funding_abstract_html + div_top_html + abstract_html + div_down_html
                    # funding abstract counter increase by 1
                    funding_abstract_counter = funding_abstract_counter + 1
                else:
                    # Add title
                    title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + inst_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + institution_content + '</a></h1>'

                    # Add funding abstract
                    abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em; margin:0;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + dead_date_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Apply Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                    # Add div
                    div_down_html = '\n\t\t\t</div>'

                    # Combine funding for email
                    funding_abstract_html = funding_abstract_html + div_top_html + title_html + abstract_html + div_down_html
                    # funding abstract counter increase by 1
                    funding_abstract_counter = funding_abstract_counter + 1

                funding_inst = institution_content

            elif category_content == 'CHER News':
                post_date = self.try_parsing_date(post_date_content).date()
                if post_date < date.today() - timedelta(days=16) and headline_content != 'Y':
                    # break current loop
                    continue
                else:
                    # Add div
                    div_top_html = '\n\t\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html = '\n\t\t\t\t\t<h1 class="title" style="font-weight: 400;margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a></h1>'

                    # Add date
                    #post_date_content = post_date.strftime('%B %d, %Y')
                    #date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400;margin: 0.5em 0 0.5em 0; font-size: 1.1em;">' + post_date_content + '</h3>'

                    # Add location or award
                    location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400;margin: 0 0 0.5em 0; font-size: 1.1em;">Institution: <a target="_blank" href="' + inst_url_content + '" style="text-decoration: none; color: #56a0d3;">' + institution_content + '</a></h3>'

                    # Add image and abstract
                    final_txt_content = html.unescape(final_txt_content)
                    if img_url_content == '':
                        abstract_html = '\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                    else:
                        abstract_html ='\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="25%" align="center"><img width="100%" class="image" src="'+ img_url_content +'" style="min-width: 180px; display: block;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                        abstract_html_wp = '\n\t\t\t\t<table class="news-content" border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="20%" align="center"><img width="100%" class="image" src="' + img_url_content + '" style="min-width: 180px; display: block;max-height: 250px;width: auto;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin-left: 10px; font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p></td>\n\t\t\t\t</tr></tbody></table>'

                    # Add div
                    div_down_html = '\n\t\t\t\t</div>'

                    # Combine events together
                    if headline_content == 'Y':
                        news_html_headline = news_html_headline + div_top_html + title_html + location_award_html + abstract_html + div_down_html
                        news_html_wp_headline = news_html_wp_headline + div_top_html + title_html + location_award_html + abstract_html_wp + div_down_html
                    else:
                        news_html = news_html + div_top_html + title_html + location_award_html + abstract_html + div_down_html
                        news_html_wp = news_html_wp + div_top_html + title_html + location_award_html + abstract_html_wp + div_down_html

            elif category_content == 'CHER Publication':
                post_date = self.try_parsing_date(post_date_content).date()
                if post_date < date.today() - timedelta(days=16) and headline_content != 'Y':
                    # break current loop
                    continue
                else:
                    # Add div
                    div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400;margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a></h1>'

                    # Add date
                    #post_date_content = post_date.strftime('%B %d, %Y')
                    #date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400;margin: 0.5em 0 0.5em 0; font-size: 1.1em;">' + post_date_content + '</h3>'

                    # Add location or award
                    location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400;margin: 0 0 0.5em 0; font-size: 1.1em;">Institution: <a target="_blank" href="' + inst_url_content + '" style="text-decoration: none; color: #56a0d3;">' + institution_content + '</a></h3>'

                    # Add image and abstract
                    final_txt_content = html.unescape(final_txt_content)
                    if img_url_content == '':
                        abstract_html = '\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                    else:
                        abstract_html ='\n\t\t\t\t<table border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="25%" align="center"><img width="100%" class="image" src="'+ img_url_content +'" style="min-width: 180px; display: block;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin: 0; font-weight: 300;line-height: 1.5em">'+ final_txt_content +'</p></td>\n\t\t\t\t</tr></tbody></table>'
                        abstract_html_wp = '\n\t\t\t\t<table class="news-content" border="0" cellpadding="5" cellspacing="0" width="100%"><tbody><tr>\n\t\t\t\t\t<td width="20%" align="center"><img width="100%" class="image" src="' + img_url_content + '" style="min-width: 180px; display: block;max-height: 250px;width: auto;"></td>\n\t\t\t\t\t<td valign="top"><p class="abstract" style="margin-left: 10px; font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p></td>\n\t\t\t\t</tr></tbody></table>'

                    # Add div
                    div_down_html = '\n\t\t\t\t</div>'

                    # Combine events together
                    pub_html = pub_html + div_top_html + title_html + location_award_html + abstract_html + div_down_html
                    pub_html_wp = pub_html_wp + div_top_html + title_html + location_award_html + abstract_html_wp + div_down_html

        # Add </section>
        event_html = event_html_headline + event_html + '\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t\t<div class="more-event" style="text-align: right">\n\t\t\t\t\t<a href="https://cher.unc.edu/news-announcements/" target="_blank"><img src="https://cher.unc.edu/files/2017/03/more-events.png" width="200"></a>\n\t\t\t\t</div>\n\t\t\t</section>'
        event_html_wp = event_html_wp_headline + event_html_wp + '[/tab]'
        funding_html = funding_html_headline + funding_html + '\n\t\t</section>'
        if funding_abstract_counter > 0:
            funding_abstract_html = funding_abstract_html + '\n\t\t\t</section>'
        else:
            funding_abstract_html = ''
        if wip_html == '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER Events</h1>':
            wip_html = ''
        if wip_html_wp == '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">CHER Events</h1>':
            wip_html_wp = ''
        if pub_html == '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Recent Publications</h1>':
            pub_html = ''
        if pub_html_wp == '<h1 style="font-weight: 600; margin: 0.5em 0 0.5em 0; font-size:1.5em; color: #E4A552;">Recent Publications</h1>':
            pub_html_wp = ''
        associate_html = associate_html + news_html_headline + news_html + wip_html + pub_html + '\n\t\t\t\t<div style="margin-top: 1em;text-align: right">\n\t\t\t\t\t<a href="https://cher.unc.edu/news-announcements/" target="_blank"><img src="https://cher.unc.edu/files/2017/03/more-news.png" width="200"></a>\n\t\t\t\t</div>\n\t\t\t</section>'
        associate_html_wp = associate_html_wp + news_html_wp_headline + news_html_wp + wip_html_wp + pub_html_wp + '[/tab]'

        # Combine html together
        content_html = associate_html + event_html + funding_html + funding_abstract_html
        content_html_WP = '[tabs class="cher-newsletter"]' + associate_html_wp + event_html_wp + funding_html_wp + '''[/tabs]\n<div style="margin-left: 20px">[button style="btn-default btn-lg" icon="glyphicon glyphicon-hand-up" align="left" iconcolor="#56a0d3" type="link" target="true" title="Subscribe to CHER Newsletter" link="http://eepurl.com/bE702D" linkrel=""]&nbsp;[button style="btn-default btn-lg" icon="glyphicon glyphicon-search" align="left" iconcolor="#56a0d3" type="link" target="true" title="Search Publications" link="https://cher.unc.edu/publication-search/" linkrel=""]</div>'''

        # Return content
        return content_html, content_html_WP


def main():
    csv_html = htmlGenerater()

main()
