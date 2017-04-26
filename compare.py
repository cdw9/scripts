"""pass two instance/client scripts as arguments
   scripts should have eggs listed,
   like https://gist.github.com/cdw9/c6d8ab6c28504d179b81856fb7a37e1d

   $ python compare.py file1 file2

   script will output version
   differences between the two files
"""

import re
from sys import argv

script, versions1, versions2 = argv


def filter_products(file):
    """ clean up the file so we end up with a list
        of the products and their versions
    """
    f = open(file)
    lines = (line.rstrip() for line in f)

    versions = {}
    write = False
    for line in [l for l in lines if l]:
        if write is False and line != 'sys.path[0:0] = [':
            continue
        elif line.strip() == ']':
            write = False
            continue
        else:
            write = True
        line = re.sub('(.*[\/])', '', line)
        line = re.sub('(-py.*$)', '', line)
        vkey = re.sub('(\-.*$)', '', line)
        vval = re.sub('(.*[\-])', '', line)
        versions[vkey] = vval
    return versions

f1v = filter_products(versions1)
f2v = filter_products(versions2)

output = ''

for product in f1v:
    if product not in f2v:
        output += "{0} > N/A\n".format(product)
        continue
    if f1v[product] == f2v[product]:
        continue
    output += "{0} {1} > {2}\n".format(product, f1v[product], f2v[product])

for product in f2v:
    if product not in f1v:
        output += "N/A > {0}\n".format(product)

print output
