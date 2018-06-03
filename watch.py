"""TODO: Make this watch the word counts among the respective files

Also, make this a sublime text plugin

word count command: `command: latex_word_count`
"""
import os
import re
import subprocess


if __name__ == '__main__':
    WORDS_RE = re.compile(r'Words in text: (\d+)')

    tex_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))

    sub = 'Words in text:'
    for file in tex_files:
        s = subprocess.run(['texcount', file], stdout=subprocess.PIPE)
        res = WORDS_RE.search(s.stdout.decode())
        if res:
            print(file)
            print(res.group(1))
