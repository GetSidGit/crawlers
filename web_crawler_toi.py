import urllib2
from bs4 import BeautifulSoup
from time import  sleep

# Provide base url which is ideally list of pages of articles in base_url , define start_page as starting page number and end_page as ending page number - script will crawl through all these pages, recursively read articles and writes creates data_dump.txt
start_page = 2
end_page = 14
website_url = 'https://timesofindia.indiatimes.com'
base_url = website_url + '/sports/cricket/ipl/'
dump_file_name_with_path = "/Users/Sid/PycharmProjects/NLP_ThePositiveIndia/toi/sports/toi_sports_data_dump.txt"
links_list = []



# for some reason function is not returing BS datatype through return - not using userdefined function for now

links_page_count = 0
skipped_articles = 0
for page_num in range(start_page, end_page + 1):

    sleep(10)

    page_url = base_url + str(page_num)
    page = urllib2.urlopen(page_url)
    page_html = page.read()
    page.close()
    page_soup_links = BeautifulSoup(page_html, "html.parser")

    links_list_data = page_soup_links.findAll("span", {"class": "w_tle"})

    for span in links_list_data:
        links = span.findAll('a')
        for link in links:
            if link['href'].endswith(".cms") and link['href'].startswith("/" + base_url.split("/")[-4]):
                links_list.append(website_url + link['href'])

    print "Initiating search on link page number :" + str(links_page_count)
    links_page_count += 1
    url_counter = 0

    for url_ip in links_list:

        sleep(20)
        print "reading article number :" + str(url_counter)
        url_counter += 1
        page = urllib2.urlopen(url_ip)
        page_html = page.read()
        page.close()
        page_soup = BeautifulSoup(page_html, "html.parser")

        # pick heading here

        containers = page_soup.findAll("h1", {"class": "heading1"})
        if len(containers) == 0 :
            skipped_articles += 1
        else :
            heading = containers[0].text.strip()

            # pick body here

            containers = page_soup.findAll("div", {"class": "Normal"})

            # remove unnecessary div tags

            for div in containers[0].findAll('div'):
                div.decompose()

            article = containers[0].text

            text = heading + "|" + article
            text = text.replace('\n', ' ')
            text = text.replace('\'', ' ')

            # type cast utf 16 characterset

            text = text.encode('utf-8')

            # write to a file
            print "writing to file"

            f = open(dump_file_name_with_path, "a")
            f.write(text + '\n')
            f.close()



print "Crawler completed, skipped : " + str(skipped_articles) + " articles"











