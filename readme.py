import os
import requests
import re

def description(filename):
    s = find_between(requests.get(f"https://raw.githubusercontent.com/marconivr/2020-2022-T-CI/18576/{filename}/docs/README.md").text, "Description", "#").replace("\r\n", " ").replace("\n", " ").replace("\t", "").replace("    ", "").replace("- ", "; ").replace(":;", ":").replace(": ;", ":")
    while s[0] == " ": s = s[1:]
    while s[-1] == "\n": s = s[:-1:]
    print('\r' in s)
    return str(s)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_readme():
    file_content = '# :octocat: Lavori di Castellani Davide (18576) :octocat:\n![](https://www.castellanidavide.it/assets/img/main-covers/main.jpg)\n'
    for i in sorted([x for x in os.listdir('./') if not x[0] == '.' and os.path.isdir(x)]):
        file_content += f' - [{i}](https://github.com/$GITHUB_REPOSITORY/blob/18576/{i}/docs/README.md): {description(i)}\n'

    file_content += '\n---\nMade by Castellani Davide \nIf you have any problem please contact me:\n - help@castellanidavide.it\n'
    print(file_content)
    return file_content

if __name__ == "__main__":
    open('README2.md', 'w+').write(str(get_readme()))
