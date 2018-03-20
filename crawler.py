# Script crawler

from urllib.request import urlopen
from urllib import parse
import re
import string
import io


INDEX_KEY_LIST = ['#']
INDEX_KEY_LIST.extend(string.ascii_lowercase)


def create_url(letter: str):
    return 'http://www.imsdb.com/alphabetical/' + letter


def get_page(url: str):
    response = urlopen(url)
    return str(response.read())


def absolute_path(relative: str):
    return 'http://www.imsdb.com' + parse.quote_plus(relative, '/')


def sanitize(dirty: str):
    return dirty.replace('\\r\\n', '\r\n')\
                .replace('\\n', '\r\n') \
                .replace('\\r', '\r\n')\
                .replace('\\', '')


def url_to_script(url: str):
    info_page = get_page(url)

    info_table_matches = re.findall('<b>IMSDb opinion</b>([\s\S]*?)</td>', info_page)

    if len(info_table_matches) is not 1:
        print("%s has incorrect format" % url)
        return

    info_table = info_table_matches[0]

    links = re.findall('<a href="(.*?)"', info_table)

    script_url = absolute_path(links[len(links) - 1])

    script_page = get_page(script_url)

    return sanitize(re.findall('<td class="scrtext">([\s\S]*?)</pre><br>', script_page)[0])


def find_links(letter: str):
    content = sanitize(get_page(create_url(letter)))

    # matches = re.findall('<p><a[^>]*?title="([^"]*?)[\s,]*((The Script)|(Script))?"[^>]*>.*?<i>Written by (.*?)</i>', content)
    matches = re.findall('<p><a\s*[^>]*?href="(.*?)"[^>]\s*title="([^"]*?)[\s,]*((The Script)|(Script))?"[^>]*>.*?<i>Written by (.*?)</i>', content)

    movies = []

    for match in matches:
        movies.append({'title': match[1], 'url': absolute_path(match[0]), 'authors': match[5].split(',')})

    return movies


def count_links(letter: str):
    return len(find_links(letter))


def count_all():
    count = 0

    for letter in INDEX_KEY_LIST:
        link_count = count_links(letter)
        count += link_count

    return count


def movies_as_text(movies):
    return '\n'.join(str(movie) for movie in movies)


def create_movies_arr():
    movies = []

    for letter in INDEX_KEY_LIST:
        sub = find_links(letter)
        movies.extend(sub)

    return movies


def dump_movies():
    movies = create_movies_arr()

    dump_file = io.open('movies', 'w')

    dump_file.write(movies_as_text(movies))
    dump_file.close()


def download_scripts():
    print('Script download mode')

    movies = create_movies_arr()

    print('Indexed %d movies' % len(movies))

    for movie in movies:
        try:
            script = url_to_script(movie['url'])
            print("Downloaded %s successfully" % movie['title'])

            file = io.open(movie['title'] + '.html', 'w')
            file.write(script)
            file.close()
        except:
            print('Skipping %s because of failure' % movie['url'])


def main():
    valid_options = ['0', '1']
    option = ''

    while option not in valid_options:
        option = input('Please enter 0 for dumping movies to the movies.dat, 1 for downloading all the scripts\n')

    if option is '1':
        download_scripts()
    else:
        dump_movies()


main()
