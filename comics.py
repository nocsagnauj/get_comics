#!/usr/bin/env python3

"""
This file downloads comics images from gocomics.com
The script is done in 'for' loops

The date and comic names are written in solid in the code
Next steps are:
 - iterate all the comics from a list
 - read from a config file or CLI the comic name, the start and end dates
"""

import calendar
import urllib.request as urlrq

DEST_PATH="/tmp/comics/"
SITE_PATH="http://www.gocomics.com/"
comics_base=[("bignate","bignate"),("pearlsbeforeswine","pearls")]
comic_url_name=comics_base[0][0]
comic_name=comics_base[0][1]

#Creates the comic url in iterative way
if __name__ == "__main__":

    mycal=calendar.Calendar()
    for year in range(2014,2017):
        for month in range (1,13):
            if year==2014 and month<4:
                continue
            days=mycal.itermonthdays(year,month)
            for d in days:
                if d>0:
                    url_comic=SITE_PATH+comic_url_name+"/{0}/{1:02d}/{2:02d}".format(year,month,d)
                    print (url_comic)

                    html_comic=urlrq.urlopen(url_comic)
                    html_comic_str=str(html_comic.read())
                    point_line=html_comic_str.find("data-image=")
                    start_url_img=html_comic_str.find("\"",point_line)+1
                    end_url_img=html_comic_str.find("\"",start_url_img)
                    url_img=html_comic_str[start_url_img:end_url_img]
                    #print (url_img)

                    html_img=urlrq.urlopen(url_img)
                    header_html_img=html_img.getheader('Content-Disposition')
                    point_filename=header_html_img.find("filename=")
                    start_filename=header_html_img.find("\"",point_filename)+1
                    end_filename=header_html_img.find("\"",start_filename)
                    full_filename=header_html_img[start_filename:end_filename]
                    filename=comic_name+"20"+full_filename[2:] #rename the comic with comic name instead of 'bn' or 'pb'
                    print(filename)

                    urlrq.urlretrieve(url_img,DEST_PATH+filename)
