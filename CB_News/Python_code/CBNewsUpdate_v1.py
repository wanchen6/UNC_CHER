# -*- coding: utf-8 -*-

import csv, os
from datetime import date
from datetime import timedelta
from datetime import datetime

def main():
    # Initiate HTML
    html_head = '''<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">\n\t\t<title>Welcome to Center For Bioethics</title>\n\t\t<link rel="Stylesheet" href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600">\n\t\t<style>\n\t\t\tbody {\n\t\t\t\tfont-family: 'Open Sans', sans-serif;\n\t\t\t\tfont-weight: 300;\n\t\t\t\tbackground-color: #7bafd4;\n\t\t\t\tmargin-right: 0px;\n\t\t\t\tmargin-left: 0px;\n\t\t\t\tmargin-bottom: 0px;\n\t\t\t\tmargin-top: 0px;\n\t\t\t\twidth: 100%;\n\t\t\t\theight: 100%;}\n\t\t\th1, h2, h3, h4, h5 {\n\t\t\t\tcolor: #2F5597;\n\t\t\t\tmargin: 5px 0;}\n\t\t\th1 {\n\t\t\t\tfont-size: 20px;\n\t\t\t\tline-height: 30px;\n\t\t\t\tfont-style:italic;\n\t\t\t\tfont-weight: 500;\n\t\t\t\tmargin: 10px 0 10px 0;}\n\t\t\th2 {\n\t\t\t\tfont-weight: 500;\n\t\t\t\tfont-size: 18px;\n\t\t\t\tline-height: 25px;}\n\t\t\th3 {\n\t\t\t\tfont-weight: 500;\n\t\t\t\tfont-size: 16px;\n\t\t\t\tline-height: 22px;}\n\t\t\th4 {\n\t\t\t\tfont-size: 14px;\n\t\t\t\tline-height: 18px;\n\t\t\t\t	font-style:italic;\n\t\t\t\tfont-weight: 300;}\n\t\t\th5,p {\n\t\t\t\tfont-size: 12px;\n\t\t\t\tline-height: 18px;\n\t\t\t\t}\n\t\t\tp {\n\t\t\t\tmargin-top: 10px;\n\t\t\t\tcolor: #4f4f4f;}\n\t\t\ta {\n\t\t\t\tcolor: #2F5597;\n\t\t\t\ttext-decoration: none;}\n\t\t\ta:hover {\n\t\t\t\tcolor: #56a0d3;}\n\t\t\ttable {\n\t\t\t\tborder: 0;\n\t\t\t\tmax-width: 600px;\n\t\t\t\tbackground-color: #fff;\n\t\t\t\tborder-collapse: collapse;}\n\t\t\ttd {\n\t\t\t\tpadding: 5px 10px;\n\t\t\t\tvertical-align: top;}\n\t\t\t.section-title, .events-title {\n\t\t\t\tborder-bottom: 1px #2F5597 solid;\n\t\t\t\tbackground-color: #fff;\n\t\t\t\tmargin: 0;\n\t\t\t\tpadding: 10px 10px;\n\t\t\t\twidth: 580px;\n\t\t\t\ttext-align: left;}\n\t\t\t.events-title {\n\t\t\t\tbackground-color: #F2F2F2;}\n\t\t\t.title {\n\t\t\t\tmargin: 0;}\n\t\t\t.personnel {\n\t\t\t\tmargin: 0;}\n\t\t\timg:hover {\n\t\t\t\topacity: 0.8;}\n\t\t\t.cb-browser-link {\n\t\t\t\tbackground-color: #F2F2F2;}\n\t\t\t.cb-browser-link td {\n\t\t\t\tpadding: 5px;\n\t\t\t\ttext-align: center;}\n\t\t\t.cb-browser-link td p {\n\t\t\t\tmargin: 0;}\n\t\t\t.cb-header {\n\t\t\t\tbackground-color: #CCECFF;}\n\t\t\t.cb-header td{\n\t\t\t\twidth: 50%;}\n\t\t\t.share {\n\t\t\t\tfont-style:normal;\n\t\t\t\tmargin-top: 5px;}\n\t\t\t.cb-logo {\n\t\t\t\twidth: 250px;\n\t\t\t\ttext-align: center;\n\t\t\t\tpadding: 15px;}\n\t\t\t.social-logo {\n\t\t\t\twidth: 40px;\n\t\t\t\tpadding: 0 5px;}\n\t\t\t.cb-navbar {\n\t\t\t\tbackground-color: #2F5597;\n\t\t\t\ttext-align: center;\n\t\t\t\t}\n\t\t\t.cb-navbar td h3 a {\n\t\t\t\tcolor: #fff;}\n\t\t\t.cb-navbar td h3 a:hover {\n\t\t\t\tcolor: #56a0d3;}\n\t\t\t#cb-nav {\n\t\t\t\tcolor: #fff;\n\t\t\t\tmargin: 0;}\n\t\t\t.event-left {\n\t\t\t\twidth: 33%;}\n\t\t\t.event-right {\n\t\t\t\twidth: 67%;}\n\t\t\t.speaker-img {\n\t\t\t\tmax-height: 150px;\n\t\t\t\twidth: auto;\n\t\t\t\tmargin-top: 5px;}\n\t\t\t#cb-events table tbody{\n\t\t\t\tbackground-color: #F2F2F2;}\n\t\t\t.news-left {\n\t\t\t\twidth: 67%;}\n\t\t\t.news-right {\n\t\t\t\twidth: 33%;\n\t\t\t\ttext-align: center;}\n\t\t\t.news-img {\n\t\t\t\tmargin: 5px;\n\t\t\t\tmax-height: 150px;\n\t\t\t\twidth: auto;\n\t\t\t\tmax-width: 150px;}\n\t\t\t#cb-publications table tbody tr td p {\n\t\t\t\tmargin:0;}\n\t\t\t.cb-footer {\n\t\t\t\tmax-width: 600px;\n\t\t\t\tbackground-color: #CCECFF;\n\t\t\t\ttext-align: center;\n\t\t\t\tpadding-bottom: 5px;}\n\t\t\t.social-media {\n\t\t\t\tpadding-top: 10px;\n\t\t\t\tpadding-bottom: 10px;}\n\t\t\t.social-media.social-logo {\n\t\t\t\tmargin: 10px;}\n\t\t\t.contact{\n\t\t\t\tmargin-top: 18px;}\n\t\t\t.footer-button div {\n\t\t\t\tbox-shadow: 1px 2px 2px #4f4f4f;\n\t\t\t\tborder-radius: 3px;\n\t\t\t\tbackground-color: #F2F2F2;\n\t\t\t\tdisplay: inline-block;\n\t\t\t\tpadding: 5px;}\n\t\t\t.footer-button div:hover {\n\t\t\t\tbackground-color: #2F5597;}\n\t\t\t.footer-button a {\n\t\t\t\tcolor: #4f4f4f;}\n\t\t\t.footer-button a:hover {\n\t\t\t\tcolor: #fff;}\n\t\t\t@media only screen and (max-width: 480px){\n\t\t\t\t.cb-header td {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\twidth: calc(100% - 20px);\n\t\t\t\t\ttext-align: center;}\n\t\t\t\t.event-right,\n\t\t\t\t.event-left, \n\t\t\t\t.news-right, \n\t\t\t\t.news-left {\n\t\t\t\t\tdisplay: block;\n\t\t\t\t\twidth: calc(100% - 20px);}\n\t\t\t\t.event-left {\n\t\t\t\t\ttext-align: center;}\n\t\t\t\t.speaker-img {\n\t\t\t\t\twidth: calc(100% - 20px);\n\t\t\t\t\theight: auto;\n\t\t\t\t\tmax-height: none;}\n\t\t\t\t.news-img {\n\t\t\t\t\tmax-width: calc(100% - 20px);\n\t\t\t\t\theight: auto;\n\t\t\t\t\tmax-height: none;}\n\t\t\t\t.section-title,\n\t\t\t\t.events-title {\n\t\t\t\t\twidth: calc(100% - 20px);}\n\t\t\t\t}\n\t\t\t@media only screen and (min-width: 1500px){\n\t\t\t\ttable {\n\t\t\t\t\tmax-width: 900px;}\n\t\t\t\t.cb-footer {\n\t\t\t\t\tmax-width: 900px;}\n\t\t\t\t.section-title, \n\t\t\t\t.events-title {\n\t\t\t\t\twidth: 880px;}\n\t\t\t\ttd {\n\t\t\t\t\tpadding: 5px 50px;}\n\t\t\t\t}\n\t\t\t</style>\n\t\t</head>'''
    html_foot = '''\n\t\t\t<footer class="cb-footer">\n\t\t\t\t<div class="social-media">\n\t\t\t\t\t<a target="_blank" href="https://www.facebook.com/bioethicsunc/"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/facebook_circle.png"></a>\n\t\t\t\t\t<a target="_blank" href="https://twitter.com/unc_bioethics"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/twitter_circle.png"></a>\n\t\t\t\t\t<a target="_blank" href="https://www.linkedin.com/in/uncbioethics"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/linkedin_circle.png"></a>\n\t\t\t\t</div>\n\t\t\t\t<div class="slogan">\n\t\t\t\t\t<h3>UNC Center For Bioethics</h3>\n\t\t\t\t\t<h4>Advancing bioethics as collaborative craft in an interdependent world</h4>\n\t\t\t\t\t<h4 class="contact">Contact Us</h4>\n\t\t\t\t</div>\n\t\t\t\t<div class="footer-button">\n\t\t\t\t\t<div><a target="_blank" href="https://www.google.com/maps/dir//333+S+Columbia+St+MacNider+Hall,+University+of+North+Carolina+at+Chapel+Hill,+Chapel+Hill,+NC+27514/@35.905524,-79.0525199,17z/data=!4m16!1m7!3m6!1s0x89acc2ef82ab01f1:0x975f2c135dd7543a!2s333+S+Columbia+St+MacNider+Hall,+Chapel+Hill,+NC+27514!3b1!8m2!3d35.905524!4d-79.0525199!4m7!1m0!1m5!1m1!1s0x89acc2ef82ab01f1:0x975f2c135dd7543a!2m2!1d-79.0525199!2d35.905524">Map Direction</a></div>\n\t\t\t\t\t<div><a target="_blank" href="https://bioethics.unc.edu/request/">Consultation</a></div>\n\t\t\t\t\t<p>&copy;2016 UNC Center for Bioethics</p>\n\t\t\t\t</div>\n\t\t\t</footer>'''
    # Locate the CSV and read it
    file = str(input('Please enter your CSV path: '))
    filepath = os.path.abspath(file)

    # Call read_content
    try:
        with open(filepath, 'r', newline='', encoding='windows-1252') as csvfile:
            csv_content = csv.DictReader(csvfile)
            html_body_email = read_content(csv_content)
        csvfile.close()
        if html_body_email == None:
            html_body_email = '<body></body>'
            #html_body_wordpress = '<body></body>'
        else:
            html_body_email = '''\n\t<body>\n\t\t<center>\n\t\t\t<header>\n\t\t\t\t<table>\n\t\t\t\t\t<tbody>\n\t\t\t\t\t\t<tr class="cb-browser-link">\n\t\t\t\t\t\t\t<td colspan="2"><p>This message contains graphics. If you do not see the graphics, <a target="_blank" href="*|ARCHIVE|*">click here to view</a></p></td>\n\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t<tr class="cb-header">\n\t\t\t\t\t\t\t<td><img class="cb-logo" src="https://bioethics.unc.edu/files/2016/11/cb-logo.png"></td>\n\t\t\t\t\t\t\t<td class="header-right">\n\t\t\t\t\t\t\t\t<h2>UNC Center For Bioethics</h2>\n\t\t\t\t\t\t\t\t<h4>Advancing bioethics as collaborative craft in an interdependent world</h4>\n\t\t\t\t\t\t\t\t<h4 class="share">\n\t\t\t\t\t\t\t\t\t<a target="_blank" href="https://www.facebook.com/bioethicsunc/"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/facebook_circle.png"></a>\n\t\t\t\t\t\t\t\t\t<a target="_blank" href="https://twitter.com/unc_bioethics"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/twitter_circle.png"></a>\n\t\t\t\t\t\t\t\t\t<a target="_blank" href="https://www.linkedin.com/in/uncbioethics"><img class="social-logo" src="https://bioethics.unc.edu/files/2016/12/linkedin_circle.png"></a>\n\t\t\t\t\t\t\t\t</h4>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t<tr class="cb-navbar">\n\t\t\t\t\t\t\t<td colspan="2"><h3 id="cb-nav"><a href="#cb-news">News</a> | <a href="#cb-events">Events</a> | <a href="#cb-publications">Publications</a></h3></td>\n\t\t\t\t\t\t</tr>\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t</header>'''+html_body_email+html_foot+'\n\t\t</center>\n\t</body>\n</html>'

        # Combine the HTML text together
        html_doc_email = html_head + html_body_email
        #html_doc_wordpress = html_body_wordpress

        # Print the whole HTML out in 2 versions: email, wordpress
        output_path = input('Please enter output path of email HTML: ')
        f = open(output_path, 'w', encoding='windows-1252', errors='ignore')
        f.write(html_doc_email)
        f.close()
        #output_path = input('Please enter output path of WordPress HTML: ')
        #f = open(output_path, 'w', encoding='windows-1252', errors='ignore')
        #f.write(html_doc_wordpress)
        #f.close()

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
    event_html = '''\n\t\t\t<section id="cb-events">\n\t\t\t\t<h1 class="events-title">Upcoming Events</h1>\n\t\t\t\t<table>\n\t\t\t\t\t<tbody>'''
    #event_html_wp = '[tab title="Upcoming Events"]'
    news_html = '''\n\t\t\t<section id="cb-news">\n\t\t\t\t<h1 class="section-title">Center News</h1>\n\t\t\t\t<table>\n\t\t\t\t\t<tbody>'''
    #news_html_wp = '[tab title="Center News"]'
    publication_html = '''\n\t\t\t<section id="cb-publications">\n\t\t\t\t<h1 class="section-title">Center Publication</h1>\n\t\t\t\t<table>\n\t\t\t\t\t<tbody>'''
    #publication_html_wp = '[tab title="Center Publications" active="active"]'

    # Read CSV
    for row in csv_content:
        id_content = row['ID']
        title_content = row['Title']
        #subtitle_content = row['Subtitle']
        post_url_content = row['Post_URL']
        post_date_content = row['Post_Date']
        associate_content = row['Associate']
        category_content = row['Category']
        speaker_content = row['Event_Speaker']
        event_date_content = row['Event_Date']
        event_time_content = row['Event_Time']
        location_content = row['Event_Loc']
        pub_type_content = row['Pub_Type']
        pub_journal_content = row['Pub_Journal']
        pub_date_content = row['Pub_Date']
        pub_author_content = row['Pub_Author']
        #pub_doi_content = row['Pub_DOI']
        pub_url_content = row['Pub_URL']
        pub_publisher_content = row['Pub_Publisher']
        final_txt_content = row['Final_Text']
        img_url_content = row['Post_Image']

        # Determine if we want to hide the information of this row
        if category_content == 'Event':
            event_date = datetime.strptime(event_date_content, '%m/%d/%y').date()
            if event_date <= date.today():
                # break current loop
                continue
            else:
                # Add title
                title_html = '\n\t\t\t\t\t\t<tr class="'+id_content+'">\n\t\t\t\t\t\t\t<td colspan="2">\n\t\t\t\t\t\t\t\t<h3 class="title"><a target="_blank" href="'+post_url_content+'">'+title_content+'</a></h3>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>'

                # Add speaker (left)
                speaker_html = '\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<td class="event-left">\n\t\t\t\t\t\t\t\t<h4 class="personnel">'+speaker_content+'</h4>\n\t\t\t\t\t\t\t\t<a target="_blank" href="'+post_url_content+'"><img class="speaker-img" src="'+img_url_content+'"></a>\n\t\t\t\t\t\t\t</td>'

                # Add event content (right)
                event_date = event_date.strftime('%A, %B %d %Y')
                event_content_html = '\n\t\t\t\t\t\t\t<td class="event-right">\n\t\t\t\t\t\t\t\t<h5>'+event_date+', '+event_time_content+'</h5>\n\t\t\t\t\t\t\t\t<h5>'+location_content+'</h5>\n\t\t\t\t\t\t\t\t<p>'+final_txt_content+'</p>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>'

                # Combine events together
                event_html = event_html + title_html + speaker_html + event_content_html
                #event_html_wp  = event_html_wp + title_html + speaker_html + event_content_html

        elif category_content == 'News':
            if post_date_content != '':
                post_date = datetime.strptime(post_date_content, '%m/%d/%y').date()
                if post_date < date.today() - timedelta(days=30):
                    # break current loop
                    continue
                else:
                    # Add title
                    title_html = '\n\t\t\t\t\t\t<tr class="'+id_content+'">\n\t\t\t\t\t\t\t<td colspan="2">\n\t\t\t\t\t\t\t\t<h3 class="title"><a target="_blank" href="'+post_url_content+'">'+title_content+'</a></h3>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>'

                    # Add news content (left)
                    news_content_html = '\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<td class="news-left">\n\t\t\t\t\t\t\t\t<h4 class="personnel">'+associate_content+'</h4>\n\t\t\t\t\t\t\t\t<p>'+final_txt_content+'<a target="_blank" href="'+post_url_content+'"><em><i>READ MORE...</i></em></a></p>\n\t\t\t\t\t\t\t</td>'

                    # Add image (right)
                    img_html ='\n\t\t\t\t\t\t\t<td class="news-right">\n\t\t\t\t\t\t\t\t<a target="_blank" href="'+post_url_content+'"><img class="news-img" src="'+img_url_content+'"></a>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t</tr>'

                    # Combine newss together
                    news_html = news_html + title_html + news_content_html + img_html
            else:
                print('Please enter the post date for news ',id_content, ' in Newsletter.xlsx')

        elif category_content == 'Publication':
            if post_date_content != '':
                post_date = datetime.strptime(post_date_content, '%m/%d/%y').date()
                if post_date < date.today() - timedelta(days=60):
                    # break current loop
                    continue
                else:
                    # Add title
                    title_html = '\n\t\t\t\t\t\t<tr class="'+id_content+'">\n\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t<h3 class="title"><a target="_blank" href="'+post_url_content+'">'+title_content+'</a></h3>'

                    # Add quotation information
                    pub_date_content = datetime.strptime(pub_date_content, '%m/%d/%y')
                    if pub_type_content =='Journal Article' or pub_type_content =='Book Section':
                        quotation_html = '\n\t\t\t\t\t\t\t\t<h4 class="personnel">'+pub_author_content+' | '+str(pub_date_content.year)+' | '+pub_journal_content+'</h4>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t\t</tr>'
                    else:
                        quotation_html = '\n\t\t\t\t\t\t\t\t<h4 class="personnel">'+pub_author_content+' | '+str(pub_date_content.year)+' | '+pub_publisher_content+'</h4>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t\t</tr>'

                    # Add publication content
                    publication_content_html = '\n\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t<p>'+final_txt_content+'<a target="_blank" href="'+pub_url_content+'"><em><i>READ FULL ARTICLE...</i></em></a></p>\n\t\t\t\t\t\t\t</td>\n\t\t\t\t\t\t\t\t</tr>'

                    # Combine newss together
                    publication_html = publication_html + title_html + quotation_html + publication_content_html
            else:
                print('Please enter the post date for the publication ',id_content, ' in Newsletter.xlsx')


    # Add </section>
    event_html = event_html + '\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t</section>'
    #event_html_wp = event_html_wp +'[/tab]'
    news_html = news_html + '\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t</section>'
    publication_html = publication_html + '\n\t\t\t\t\t</tbody>\n\t\t\t\t</table>\n\t\t\t</section>'
    #publication_html_wp = publication_html_wp +'[/tab]'

    # Combine html together
    content_html = news_html + event_html + publication_html
    #content_html_WP = '[tabs class="cher-newsletter"]' + publication_html_wp + event_html_wp + news_html_wp + '[/tab][/tabs]'

    # Return content
    return content_html


main()
