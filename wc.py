"""TODO: Make this watch the word counts among the respective files

Also, make this a sublime text plugin

word count command: `command: latex_word_count`
"""
from datetime import datetime
import os
import re
import subprocess

import click

WORDS_RE = re.compile(r'Words in text: (\d+)')


def wc(file: str) -> int:
    s = subprocess.run(['texcount', file], stdout=subprocess.PIPE)
    res = WORDS_RE.search(s.stdout.decode())
    if res:
        return int(res.group(1))
    return 0


def word_counts():
    tex_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    counts = []
    for file in tex_files:
        counts.append((file, wc(file)))
    return counts


@click.group()
def cli():
    pass


@cli.command()
@click.option('--word-count/--no-word-count', default=True)
def ls(word_count):
    tex_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    longest = len(max(tex_files, key=lambda x: len(x)))
    tex_files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    total_wc = 0
    dt_len = len('YYYY-MM-DD HH:MM:SS')
    m1, m2 = 'File Name', 'Last Mod. Date'
    msg = '{0}{1}-- {2}{3} -- WC'.format(
        m1, ' ' * (longest - len(m1) - 1), m2, ' ' * (dt_len - len(m2))
    )
    click.secho(msg, fg='red')
    click.echo('-' * len(msg))
    for elem in tex_files:
        pad = ' ' * (longest - len(elem))
        msg = '{0}{2} -- {1:%Y-%m-%d %H:%M:%S}'.format(
            os.path.relpath(elem),
            datetime.fromtimestamp(os.path.getmtime(elem)),
            pad)
        if word_count:
            count = wc(elem)
            msg = msg + ' -- {0}'.format(count)
            total_wc += count
        click.echo(msg)
    if word_count:
        click.secho('\nTotal Word Count: {0}'.format(total_wc), fg='blue')


if __name__ == '__main__':
    cli()
