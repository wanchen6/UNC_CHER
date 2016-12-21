# -*- coding: utf-8 -*-
# Pseudocode of news posting of CHER
# Convert pseudocode to Python code

import csv, sys, time, os
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
from datetime import datetime

funding_inst = ''

def main():
    # Initiate HTML
    html_head = '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t\t<link rel="Stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600">\n\t\t<style>\n\t\t\t@media only screen and (max-width: 50em) {\n\t\t\t\t.news-nav[style] {\n\t\t\t\t\tfont-size:14px !important;} \n\t\t\t\t.news-header[style] {\n\t\t\t\t\tbackground-image: url("https://cher.unc.edu/files/2015/05/About-Us-photo-small-2.jpg") !important;}\n\t\t\t\t.news-title[style] {\n\t\t\t\t\tfont-size: 1em !important;}\n\t\t\t\t.title[style],\n\t\t\t\t\t.date[style],\n\t\t\t\t.location-award[style],\n\t\t\t\t.abstract[style]{\n\t\t\t\t\tfont-size: 0.8em !important;\n\t\t\t\t\tfont-weigth:300 !important;} \n\t\t\t\t.cher-socialmedia div p[style] {\n\t\t\t\t\tfont-size:0.6em !important;} \n\t\t\t\t.cher-socialmedia div[style] {\n\t\t\t\t\tfloat:none !important;\n\t\t\t\t\ttext-align: center !important;}\n\t\t\t\t.contact-info[style] {\n\t\t\t\t\tdisplay: none !important;}\n\t\t\t\t.left-social,\n\t\t\t\t.right-logo {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\tfloat: none !important;\n\t\t\t\t\tpadding: 10px !important;}\n\t\t\t\t.image-inline {\n\t\t\t\t\twidth: 220px !important;}\n\t\t\t\t.news-header {\n\t\t\t\t\tpadding: 15px !important;}\n\t\t\t}\n\t\t\t@media only screen and (min-width: 1500px) {\n\t\t\t\t.news-header {\n\t\t\t\t\tpadding: 100px 100px !important;}\n\t\t\t}\n\t\t</style>\n\t</head>'
    html_foot = '\n\t<footer style="margin-top: 15px;">\n\t\t<div class="news-nav" style="margin:0;width: 100%;background-color: #56a0d3;text-align: center;padding: 10px;color: #fff;clear: both;font-size: 20px;">\n\t\t\t<a href="#event" style="text-decoration: none; color: #fff;">Events</a> | \n\t\t\t<a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a> | \n\t\t\t<a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a>\n\t\t</div>\n\t\t<div class="cher-socialmedia" style="background-color: #333;width:100%; height:250px;">\n\t\t\t<div style="float: left;padding-left: 5%;padding-top:20px;">\n\t\t\t\t<img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/CHER_logo.png" style="width: 200px; margin-bottom:5%;">\n\t\t\t\t<br>\n\t\t\t\t<a target="_blank" href="https://www.facebook.com/cher.unc.edu"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/facebook.png"></a>\n\t\t\t\t<a target="_blank" href="https://twitter.com/uncCHER"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/twitter.png"></a>\n\t\t\t\t<a target="_blank" href="https://plus.google.com/u/0/113618129434863244332"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/google.png"></a>\n\t\t\t\t<p style="clear:both; font-size: 14px; color: #fff;margin-bottom:0;">&copy; 2016 UNC Center for Health Equity Research</p>\n\t\t\t</div>\n\t\t\t<div class="contact-info" style="float:right;padding-top:20px;padding-right:5%;color:#fff;">\n\t\t\t\t<h2 style="line-height: 1.2em;margin-top:0;">VISIT OUR CENTER</h2>\n\t\t\t\t<p style="line-height: 1.2em;margin:0;">Center for Health Equity Research</p>\n\t\t\t\t<p style="line-height: 1.2em;margin:0;">323 MacNider Hall</p><p style="line-height: 1.2em;margin:0;">Campus Box 7240</p>\n\t\t\t\t<p style="line-height: 1.2em;margin:0;">333 South Columbia Street</p>\n\t\t\t\t<p style="line-height: 1.2em;margin:0;">Chapel Hill, NC 27599-7240</p>\n\t\t\t\t<p style="line-height: 1.2em;margin-bottom:0;">&#9742; 919.843.8271</p>\n\t\t\t\t<p style="line-height: 1.2em;margin:0;">&#9993; cher@unc.edu</p>\n\t\t\t</div>\n\t\t</div>\n\t</footer>'
    # Locate the CSV and read it
    file = str(input('Please enter your CSV path: '))
    filepath = os.path.abspath(file)

    # Call read_content
    try:
        with open(filepath, 'r', newline='', encoding='windows-1252') as csvfile:
            csv_content = csv.DictReader(csvfile)
            html_body_email,html_body_wordpress = read_content(csv_content)
        csvfile.close()
        if html_body_email == None or html_body_wordpress == None:
            html_body_email = '<body></body>'
            html_body_wordpress = '<body></body>'
        else:
            html_body_email = '''\n\t<body style="margin:0; font:300 1em/2em 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; color:#666; text-decoration: none;">\n\t\t<div style="width:100%;text-align:center;margin: 0;">\n\t\t\t<a href="*|ARCHIVE|*" style="text-decoration: none; color: #56a0d3; font-size: 12px; ">This email contains images. View this email in your browser</a>\n\t\t</div>\n\t\t<div class="news-header" style="background-color: #2F5597;margin: 0;color: #fff;padding: 30px 15px 30px 40px;background-image: url('https://cher.unc.edu/files/2013/05/About-Us-photo1-e1482271981454.jpg');background-repeat: no-repeat;background-size: cover;">\n\t\t\t<div class="right-logo" style="float: right; padding: 20px;">\n\t\t\t\t<a target="_blank" href="https://cher.unc.edu/"><img class="image-inline" src="https://cher.unc.edu/files/2015/05/Center-for-Health-Equity-Research_White-4.png" style="width: 400px;"></a>\n\t\t\t</div>\n\t\t\t<div class="left-social">\n\t\t\t\t<h1 style="font-size: 30px; font-weight: 400;">Center for Health Equity Research</h1>\n\t\t\t\t<h2 style="font-size: 20px; font-weight: 300;">Innovation | Equity | Collaboration</h2>\n\t\t\t\t<a target="_blank" href="https://www.facebook.com/cher.unc.edu"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/facebook.png"></a>\n\t\t\t\t<a target="_blank" href="https://twitter.com/uncCHER"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/twitter.png"></a>\n\t\t\t\t<a target="_blank" href="https://plus.google.com/u/0/113618129434863244332"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/google.png"></a>\n\t\t\t</div>\n\t\t</div>\n\t\t<div class="news-nav" style="margin:0;width: 100%;background-color: #56a0d3;text-align: center;padding: 10px;color: #fff;clear: both;font-size: 20px;">\n\t\t\t<a href="#event" style="text-decoration: none; color: #fff;">Events</a> | \n\t\t\t<a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a> | \n\t\t\t<a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a>\n\t\t</div>'''+html_body_email+html_foot+'\n\t</body>\n</html>'

        # Combine the HTML text together
        html_doc_email = html_head + html_body_email
        html_doc_wordpress = html_body_wordpress

        # Print the whole HTML out in 2 versions: email, wordpress
        soup_email = BeautifulSoup(html_doc_email, 'html.parser')
        soup_wordpress = BeautifulSoup(html_doc_wordpress, 'html.parser')
        result_email = soup_email.prettify()
        result_wordpress = soup_wordpress.prettify()
        output_path = input('Please enter output path of email HTML: ')
        f = open(output_path, 'w', encoding='windows-1252', errors='ignore')
        f.write(html_doc_email)                 # Without prettify, symbol will be removed by the beautifysoup
        f.close()
        output_path = input('Please enter output path of WordPress HTML: ')
        f = open(output_path, 'w', encoding='windows-1252', errors='ignore')
        f.write(html_doc_wordpress)             # Without prettify, or <br> will be generated by WP
        f.close()

    except FileNotFoundError as err:
        print('Cannot find the file.')
        print(err)

    except OSError as err:
        print('Error: An error occurred trying to read the file.')
        print(err)

    except ValueError as err:
        print('Error: Unicode error occurs when reading the file.')
        print(err)

    except Exception as err:  # an exception was raised, but not IOError or ValueError
        print('An error occurred.')
        print(err)

# Search content in dictionary
def search(myDict, searchFor):
    for row in myDict:
        values = row.values()
        if searchFor in values:
            return True
    return False

# Find the content needed and write HTML
def read_content(csv_content):
    content_html = ''
    event_html = '\n\t\t<section id="event" style="margin: 0 20px;">\n\t\t\t<h1 class="news-title" style="font-weight:400; color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Event</h1>'
    event_html_wp = '[tab title="Upcoming Events"]'
    funding_html = '\n\t\t<section id="funding" class="offset" style="margin: 0 20px;">\n\t\t\t<h1 class="news-title" style="font-weight:500; color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Funding</h1>'
    funding_html_wp = '[tab title="Funding Opportunities"]'
    funding_abstract_html = '<section id="funding-list" class="offset" style="margin: 0 20px;">'
    associate_html = '\n\t\t<section id="associate" class="offset" style="margin: 0 20px;">\n\t\t\t<h1 class="news-title" style="font-weight:500; color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Our Associates</h1>'
    associate_html_wp = '[tab title="Our Associates" active="active"]'
    other_html = '\n\t\t<section id="other" class="offset" style="margin: 0 20px;">\n\t\t\t<h1 class="news-title" style="font-weight:500; color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Our Trainees</h1>'

    # Read CSV
    for row in csv_content:
        id_content = row['ID']
        title_content = row['event_title']
        institution_content = row['institution']
        inst_url_content = row['inst_url']
        location_content = row['location']
        post_date_content = row['post_date']
        dead_url_content = row['dead_url']
        dead_date_content = row['dead_date']
        apply_date_content = row['apply_date']
        dead_time_content = row['dead_time']
        event_date_content = row['event_date']
        event_end_content = row['event_end']
        post_url_content = row['post_url']
        category_content = row['category']
        award_amt_content = row['award_amt']
        final_txt_content = row['final_txt']
        img_url_content = row['img_url']

        # Determine if we want to hide the information of this row
        if category_content == 'Event':
            mydate = datetime.strptime(event_end_content, '%m/%d/%y').date()
            if mydate <= date.today():
                # break current loop
                continue
            else:
                # Add div
                div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                # Add title
                title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                # Add date
                date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_date_content + '</h3>'

                # Add location or award
                location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">' + location_content + '</h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '\n\t\t\t\t<span>\n\t\t\t\t\t<img src="' + img_url_content + '"  style="max-width: 33%; min-width:auto; max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;">\n\t\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t</span>'

                # Add div
                div_down_html = '\n\t\t\t</div>\n\t\t\t<div style="padding-top: 1em; border-top: #D9D9D9 1px solid; clear: both;"></div>'

                # Combine events together
                event_html = event_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                event_html_wp  = event_html_wp + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Funding':
            if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                mydate = datetime.strptime(dead_date_content, '%m/%d/%y').date()
                if mydate < date.today():
                # break current loop
                    continue

            if final_txt_content != '':
                # Add div
                div_top_html = '\n\t\t\t\t<div class="' + id_content + '">'

                # Add title
                title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none;  color: #56a0d3; ">' + title_content + '</a></h1>'

                # Add date
                date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">Deadline: ' + apply_date_content + '  '+ dead_time_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color:#56a0d3;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Register Now</a></h3>'

                # Add location or award
                location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400; margin: 0 0 0.5em 0; font-size: 1.1em;">Funding: ' + award_amt_content + '</h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '\n\t\t\t\t<span>\n\t\t\t\t\t<img src="' + img_url_content + '"  style="max-width: 33%; min-width:auto;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;">\n\t\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t</span>'

                # Add div
                div_down_html = '\n\t\t\t</div>\n\t\t\t<div style="padding-top: 1em; border-top: #D9D9D9 1px solid; clear: both;"></div>'

                # Combine events together
                funding_html = funding_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                funding_html_wp = funding_html_wp + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Funding Abstract':
            if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                mydate = datetime.strptime(dead_date_content, '%m/%d/%y').date()
                if mydate < date.today():
                # break current loop
                    continue

            global funding_inst
            # Add div
            div_top_html = '\n\t\t\t<div class="' + id_content + '">'

            if institution_content == funding_inst:
                # Add funding abstract
                abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em; margin:0;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + apply_date_content + '  '+ dead_time_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Register Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                # Add div
                div_down_html = '\n\t\t\t</div>'

                # Combine funding list together
                funding_abstract_html = funding_abstract_html + div_top_html + abstract_html + div_down_html
            else:
                # Add title
                title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400; margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + inst_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + institution_content + '</a></h1>'

                # Add funding abstract
                abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300; line-height: 1.5em; margin:0;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + apply_date_content + '  ' + dead_time_content + '<a target="_blank" href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Register Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                # Add div
                div_down_html = '\n\t\t\t</div>'

                # Combine funding list together
                funding_abstract_html = funding_abstract_html + div_top_html + title_html + abstract_html + div_down_html

            funding_inst = institution_content

        elif category_content == 'Associates':
            mydate = datetime.strptime(post_date_content, '%m/%d/%y').date()
            if mydate < date.today() - timedelta(days=16):
                # break current loop
                continue
            else:
                # Add div
                div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                # Add title
                title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400;margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a></h1>'

                # Add date
                date_html = '\n\t\t\t\t<h3 class="date" style="font-weight: 400;margin: 0.5em 0 0.5em 0; font-size: 1.1em;">Posted on: ' + post_date_content + '</h3>'

                # Add location or award
                location_award_html = '\n\t\t\t\t<h3 class="location-award" style="font-weight: 400;margin: 0 0 0.5em 0; font-size: 1.1em;">Institution: <a target="_blank" href="'+ inst_url_content +'" style="text-decoration: none; color: #56a0d3;">' + institution_content + '</a></h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '\n\t\t\t\t<span>\n\t\t\t\t\t<img src="' + img_url_content + '"  style="max-width: 33%; min-width:auto;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;">\n\t\t\t\t\t<p class="abstract" style="font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t</span>'

                # Add div
                div_down_html = '\n\t\t\t</div>\n\t\t\t<div style="padding-top: 1em; border-top: #D9D9D9 1px solid; clear: both;"></div>'

                # Combine events together
                associate_html = associate_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html
                associate_html_wp = associate_html_wp + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Trainees':
            if post_date_content != '':
                mydate = datetime.strptime(post_date_content, '%m/%d/%y').date()
                if mydate < date.today() - timedelta(days=0):
                    # break current loop
                    continue
                else:
                    # Add div
                    div_top_html = '\n\t\t\t<div class="' + id_content + '">'

                    # Add title
                    title_html = '\n\t\t\t\t<h1 class="title" style="font-weight: 400;margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a target="_blank" href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add image and abstract
                    if img_url_content == '':
                        abstract_html = '\n\t\t\t\t<p class="abstract" style="font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p>'
                    else:
                        abstract_html = '\n\t\t\t\t<span>\n\t\t\t\t\t<img src="' + img_url_content + '"  style="max-width: 33%; min-width:auto;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;">\n\t\t\t\t\t<p class="abstract" style="font-weight: 300;line-height: 1.5em">' + final_txt_content + '</p>\n\t\t\t\t</span>'

                    # Add div
                    div_down_html = '\n\t\t\t</div>\n\t\t\t<div style="padding-top: 1em; border-top: #D9D9D9 1px solid; clear: both;"></div>'

                    # Combine events together
                    other_html = other_html + div_top_html + title_html + abstract_html + div_down_html

    # Hide Other section if there is no content
    hide_html = ''
    if not search(csv_content, 'Trainees'):
        hide_html = '\n\t<style> #other{display: none;} </style>'

    # Add </section>
    event_html = event_html + '\n\t\t</section>'
    event_html_wp = event_html_wp +'[/tab]'
    funding_html = funding_html + '\n\t\t</section>'
    funding_abstract_html = funding_abstract_html + '\n\t\t</section>'
    associate_html = associate_html + '\n\t\t</section>'
    associate_html_wp = associate_html_wp +'[/tab]'
    other_html_email=other_html + '\n\t\t</section>' + hide_html

    # Combine html together
    content_html = associate_html + event_html + funding_html + funding_abstract_html + other_html_email
    content_html_WP = '[tabs class="cher-newsletter"]' + associate_html_wp + event_html_wp + funding_html_wp + funding_abstract_html + '''[/tab][/tabs]\n<p style="vertical-align: top;margin: 20px" class="news-label">Subscribe CHER Newsletter to keep posted on our recent news!</p>\n[heels_custom_div class="newsletter-sub"][gravityform id="7" title="false" description="false"][/heels_custom_div]'''

    # Return content
    return content_html,content_html_WP


main()
