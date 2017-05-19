import re
pattern = re.compile('za')
match = re.match(pattern,'dad')
print match.group()