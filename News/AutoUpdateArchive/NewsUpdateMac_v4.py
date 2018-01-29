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
    html_head = '<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="Stylesheet" href="http://fonts.googleapis.com/css?family=Lato:100,300,400"><style>@media only screen and (max-width: 50em) {li[style] {font-size:0.8em !important; display: block !important; margin-bottom: 0 !important;} .header-image[style] {background-image: url("https://cher.unc.edu/files/2015/05/About-Us-photo-small-2.jpg") !important;}.news-title[style] {font-size: 1em !important;} .title[style],	.date[style],.location-award[style],.abstract[style]{font-size: 0.8em !important;font-weigth:300 !important;} .cher-socialmedia div p[style] {font-size:0.6em !important;} .cher-socialmedia div[style] {float:none !important;text-align: center !important;}.contact-info[style] {display: none !important;}}</style></head>'
    html_foot = '<footer style="margin-top: 15px;"><ul class="newsletter-ul" style ="margin:0; width: 100%; background-color: rgba(86,160,211,1); margin-bottom: 0; padding-left: 0; text-align: center;"><li style="display:inline-block; margin:1em 2em;"><a href="#event" style="text-decoration: none; color: #fff;">Event</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a></li></ul><div class="cher-socialmedia" style="background-color: #333;width:100%; height:250px;"><div style="float: left;padding-left: 5%;padding-top:20px;"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/CHER_logo.png" style="width: 200px; margin-bottom:5%;"><br><a href="https://www.facebook.com/cher.unc.edu"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/facebook.png"></a><a href="https://twitter.com/uncCHER"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/twitter.png"></a><a href="https://plus.google.com/u/0/113618129434863244332"><img alt="UNC CHER" src="https://cher.unc.edu/files/2016/09/google.png"></a><p style="clear:both; font-size: 14px; color: #fff;margin-bottom:0;">&copy; 2016 UNC Center for Health Equity Research</p></div><div class="contact-info" style="float:right;padding-top:20px;padding-right:5%;color:#fff;"><h2 style="line-height: 1.2em;margin-top:0;">VISIT OUR CENTER</h2><p style="line-height: 1.2em;margin:0;">Center for Health Equity Research</p><p style="line-height: 1.2em;margin:0;">323 MacNider Hall</p><p style="line-height: 1.2em;margin:0;">Campus Box 7240</p><p style="line-height: 1.2em;margin:0;">333 South Columbia Street</p><p style="line-height: 1.2em;margin:0;">Chapel Hill, NC 27599-7240</p><p style="line-height: 1.2em;margin-bottom:0;">&#9742; 919.843.8271</p><p style="line-height: 1.2em;margin:0;">&#9993; cher@unc.edu</p></div></div></footer></html>'
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
            html_body_email = '''<body style="margin:0; font:400 1em/2em 'Lato', 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; color:#666; text-decoration: none;"><div style="text-align: center; margin: 10px;"><a href="https://cher.unc.edu/"><img class="image-inline" title="" alt="" src="https://cher.unc.edu/files/2014/03/cher-logo.jpg"></a></div><ul style ="margin:0; width: 100%; background-color: rgba(86,160,211,1); margin-bottom: 0; padding-left: 0; text-align: center;"><li style="display:inline-block; margin:1em 2em;"><a href="#event" style="text-decoration: none; color: #fff;">Events</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a></li></ul><div class="header-image" style="background-image: url('https://cher.unc.edu/files/2015/05/About-Us-photo.jpg'); background-size:cover; width:100%; height:400px;margin:0;"></div>'''+html_body_email+'</body>'
            html_body_wordpress = '''<ul class="newsletter-ul" style ="margin:0; width: 100%; background-color: rgba(86,160,211,1); margin-bottom: 0; padding-left: 0; text-align: center;"><li style="display:inline-block; margin:1em 2em;"><a href="#event" style="text-decoration: none; color: #fff;">Events</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a></li></ul>''' + html_body_wordpress

        # Combine the HTML text together
        html_doc_email = html_head + html_body_email + html_foot
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
    event_html = '<section id="event" style="margin: 0 20px;"><h1 class="news-title" style="color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Event</h1>'
    funding_html = '<section id="funding" style="margin: 0 20px;"><h1 class="news-title" style="color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Funding</h1>'
    funding_abstract_html = '<section id="funding-list" style="margin: 0 20px;">'
    associate_html = '<section id="associate" style="margin: 0 20px;"><h1 class="news-title" style="color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Our Associates</h1>'
    other_html = '<section id="other" style="margin: 0 20px;"><h1 class="news-title" style="color: #fff; font-size: 2em; margin-top: 0; margin-bottom: 0.5em; margin-left: -20px; margin-right: -20px; padding: 0.5em; background-color: rgba(86,160,211,0.5);">Our Trainees</h1>'

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
            if mydate < date.today():
                # break current loop
                continue
            else:
                # Add div
                div_top_html = '<div class="' + id_content + '">'

                # Add title
                title_html = '<h1 class="title" style="margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                # Add date
                date_html = '<h3 class="date" style="margin: 0 0 0.5em 0; font-size: 1.1em;">' + event_date_content + '</h3>'

                # Add location or award
                location_award_html = '<h3 class="location-award" style="margin: 0 0 0.5em 0; font-size: 1.1em;">Location: ' + location_content + '</h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '<p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '<span><img src="' + img_url_content + '"  style="max-width: 33%; min-width:200px; max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;"><p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p></span>'

                # Add div
                div_down_html = '</div><div style="padding-top: 1em; border-top: #D9D9D9 2px solid; clear: both;"></div>'

                # Combine events together
                event_html = event_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Funding':
            if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                mydate = datetime.strptime(dead_date_content, '%m/%d/%y').date()
                if mydate < date.today():
                # break current loop
                    continue

            if final_txt_content != '':
                # Add div
                div_top_html = '<div class="' + id_content + '">'

                # Add title
                title_html = '<h1 class="title" style="margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a href="' + post_url_content + '" style="text-decoration: none;  color: #56a0d3; ">' + title_content + '</a></h1>'

                # Add date
                date_html = '<h3 class="date" style="margin: 0 0 0.5em 0; font-size: 1.1em;">Deadline: ' + apply_date_content + '  '+ dead_time_content + '<a href="' + dead_url_content + '" style="text-decoration: none; color=#56a0d3;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Register Now</a></h3>'

                # Add location or award
                location_award_html = '<h3 class="location-award" style="margin: 0 0 0.5em 0; font-size: 1.1em;">Funding: ' + award_amt_content + '</h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '<p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '<span><img src="' + img_url_content + '"  style="max-width: 33%; min-width:200px;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;"><p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p></span>'

                # Add div
                div_down_html = '</div><div style="padding-top: 1em; border-top: #D9D9D9 2px solid; clear: both;"></div>'

                # Combine events together
                funding_html = funding_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Funding Abstract':
            if dead_date_content != 'Rolling' and dead_date_content != 'Not Given' and dead_date_content != 'Check website for details.':
                mydate = datetime.strptime(dead_date_content, '%m/%d/%y').date()
                if mydate < date.today():
                # break current loop
                    continue

            global funding_inst
            # Add div
            div_top_html = '<div class="' + id_content + '">'

            if institution_content == funding_inst:
                # Add funding abstract
                abstract_html = '<p class="abstract" style="line-height: 1.5em; margin:0;"><a href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + apply_date_content + '  '+ dead_time_content + '<a href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Register Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                # Add div
                div_down_html = '</div>'

                # Combine funding list together
                funding_abstract_html = funding_abstract_html + div_top_html + abstract_html + div_down_html
            else:
                # Add title
                title_html = '<h1 class="title" style="margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a href="' + inst_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + institution_content + '</a></h1>'

                # Add funding abstract
                abstract_html = '<p class="abstract" style="line-height: 1.5em; margin:0;"><a href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a>&nbsp;&nbsp;&nbsp;Deadline: ' + apply_date_content + '  ' + dead_time_content + '<a href="' + dead_url_content + '" style="text-decoration: none; color: #56a0d3;">&nbsp;&nbsp;&nbsp;Register Now</a>&nbsp;&nbsp;&nbsp;Funding: ' + award_amt_content + '</p>'

                # Add div
                div_down_html = '</div>'

                # Combine funding list together
                funding_abstract_html = funding_abstract_html + div_top_html + title_html + abstract_html + div_down_html

            funding_inst = institution_content

        elif category_content == 'Associates':
            mydate = datetime.strptime(post_date_content, '%m/%d/%y').date()
            if mydate < date.today() - timedelta(days=30):
                # break current loop
                continue
            else:
                # Add div
                div_top_html = '<div class="' + id_content + '">'

                # Add title
                title_html = '<h1 class="title" style="margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3;">' + title_content + '</a></h1>'

                # Add date
                date_html = '<h3 class="date" style="margin: 0.5em 0 0.5em 0; font-size: 1.1em;">Post on: ' + post_date_content + '</h3>'

                # Add location or award
                location_award_html = '<h3 class="location-award" style="margin: 0 0 0.5em 0; font-size: 1.1em;">Institution: <a href="'+ inst_url_content +'" style="text-decoration: none; color: #56a0d3;">' + institution_content + '</a></h3>'

                # Add image and abstract
                if img_url_content == '':
                    abstract_html = '<p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p>'
                else:
                    abstract_html = '<span><img src="' + img_url_content + '"  style="max-width: 33%; min-width:200px;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;"><p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p></span>'

                # Add div
                div_down_html = '</div><div style="padding-top: 1em; border-top: #D9D9D9 2px solid; clear: both;"></div>'

                # Combine events together
                associate_html = associate_html + div_top_html + title_html + date_html + location_award_html + abstract_html + div_down_html

        elif category_content == 'Trainees':
            if post_date_content != '':
                mydate = datetime.strptime(post_date_content, '%m/%d/%y').date()
                if mydate < date.today() - timedelta(days=0):
                    # break current loop
                    continue
                else:
                    # Add div
                    div_top_html = '<div class="' + id_content + '">'

                    # Add title
                    title_html = '<h1 class="title" style="margin: 0.5em 0 0.5em 0; clear: both; font-size:1.5em;"><a href="' + post_url_content + '" style="text-decoration: none; color: #56a0d3; ">' + title_content + '</a></h1>'

                    # Add image and abstract
                    if img_url_content == '':
                        abstract_html = '<p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p>'
                    else:
                        abstract_html = '<span><img src="' + img_url_content + '"  style="max-width: 33%; min-width:200px;max-height: 200px; float: left; margin-bottom: 1em; margin-right: 1em;"><p class="abstract" style="line-height: 1.5em">' + final_txt_content + '</p></span>'

                    # Add div
                    div_down_html = '</div><div style="padding-top: 1em; border-top: #D9D9D9 2px solid; clear: both;"></div>'

                    # Combine events together
                    other_html = other_html + div_top_html + title_html + abstract_html + div_down_html

    # Hide Other section if there is no content
    hide_html = ''
    if not search(csv_content, 'Trainees'):
        hide_html = '<style> #other{display: none;} </style>'

    # Add </section>
    event_html = event_html + '</section>'
    funding_html = funding_html + '</section>'
    funding_abstract_html = funding_abstract_html + '</section>'
    associate_html = associate_html + '</section>'
    other_html_email=other_html + '</section>' + hide_html
    other_html_WP= '</section><div style="margin-bottom:-20px;margin-top:15px"><ul class="newsletter-ul" style ="margin:0; width: 100%; background-color: rgba(86,160,211,1); margin-bottom: 0; padding-left: 0; text-align: center;"><li style="display:inline-block; margin:1em 2em;"><a href="#event" style="text-decoration: none; color: #fff;">Events</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#associate" style="text-decoration: none; color: #fff;">Our Associates</a></li><li style="display:inline-block; margin:1em 2em;"><a href="#funding" style="text-decoration: none; color: #fff;">Funding Opportunities</a></li></ul></div>'

    # Combine html together
    content_html = associate_html + event_html + funding_html + funding_abstract_html + other_html_email
    content_html_WP = associate_html + event_html + funding_html + funding_abstract_html + other_html_WP

    # Return content
    return content_html,content_html_WP


main()
