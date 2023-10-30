import re

with open('reglement.md', 'r') as f:
    lines = f.readlines()

levels_counter = dict()
level_mapping = ['', 'Titre', 'Article']

markdown_title_regex = re.compile("^\s{0,3}(?P<level>#{1,6})(\s|\t)+(?P<content>.*?)((\s|\t)+#*)*(\s|\t)*$")
previous_numbering_regex = re.compile(f"({'|'.join(level_mapping)}) \d+ : (?P<true_content>.*)")

numbered_lines = []
for line in lines:
    if m := markdown_title_regex.match(line):
        level = len(m.group('level'))
        content = m.group('content')

        if r := previous_numbering_regex.match(content):
            content = r.group('true_content')

        if level != 1:
            numbering = f'{level_mapping[level-1]} {levels_counter.get(level, 1)}'

            line = f"{m.group('level')} {numbering} : {content}\n"

        levels_counter[level] = levels_counter.get(level, 1) + 1

    numbered_lines.append(line)

with open('reglement.md', 'w') as f:
    f.writelines(numbered_lines)
