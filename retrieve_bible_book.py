from bs4 import BeautifulSoup
import requests


def passage(book, chapter, version):
    if " " in book:
        book = book.replace(" ", "+")
    base_url = 'https://www.biblegateway.com/passage/?search='
    search_url = f'{book}+{chapter}&version={version}'

    source = requests.get(base_url + search_url).text
    soup = BeautifulSoup(source, 'lxml')

    # Convert the first h3 tag to text to see if it matches "No results found"
    h3tag = soup.find("h3")
    h3tag = h3tag.text

    if h3tag == 'No results found.':
        noresults = True
    else:
        noresults = False

    return noresults, soup


book = input("Book of the Bible: ")
chp = input("Chapter (0 = All): ")
version = input("Bible Translation: ").upper()

if chp == '0':
    chapter = 1
else:
    chapter = chp

noresults, soup = passage(book, chapter, version)

while noresults is not True:

    chp_all = soup.find('div', class_=f'version-{version}')
    # print(chapter.prettify())

    chp_title = chp_all.find('span', class_='passage-display-bcv').text
    print()
    print(chp_title)

    # chp_header = chapter.h3.span.text
    # print(chp_header)

    for chp_content in chp_all.find_all('p'):
        try:
            for verse_num in chp_content.find_all('sup', class_='versenum'):
                verse_num.replaceWith("")
            for verse_break in chp_content.find_all('br'):
                verse_break.replaceWith("\n")
            for chap_num in chp_content.find_all('span', class_='chapternum'):
                chap_num.replaceWith("")
            for footnote in chp_content.find_all('sup', class_='footnote'):
                footnote.replaceWith("")
        except:
            pass
        chp_content = chp_content.text
        print(chp_content)
        print()

    if chp == '0':
        chapter += 1
        noresults, soup = passage(book, chapter, version)
    else:
        noresults = True
