"""wc.py: a CLI tool with functionality about/around word counts in TeX files

TODO: save each word count to a JSON file
    - each entry would have a datetime and the word counts of each file
    - then we could, in some way, compare across runs
"""
from datetime import datetime
import os
import re
import subprocess

import click

try:
    import ujson as json
except ImportError:
    import json


WORDS_RE = re.compile(r'Words in text: (\d+)')

HERE = os.path.split(os.path.abspath(__file__))[0]
log_file = os.path.join(HERE, 'counts.json')

DT_FMT = '{0:%Y-%m-%d %H:%M:%S}'
STRP_FMT = DT_FMT[3:-1]
DT_LEN = len('YYYY-MM-DD HH:MM:SS')


def save_log(entries):
    with open(log_file, 'wt') as f:
        json.dump(entries, f, indent=4)
    return os.path.isfile(log_file) and os.path.getsize(log_file)


def get_log():
    with open(log_file, 'rt') as f:
        return json.load(f)


def wc(file: str) -> int:
    s = subprocess.run(['texcount', file], stdout=subprocess.PIPE)
    res = WORDS_RE.search(s.stdout.decode())
    if res:
        return int(res.group(1))

    return 0


def find_tex_files(path):
    tex_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    return tex_files


def word_counts():
    counts = []
    for file in find_tex_files():
        counts.append((file, wc(file)))
    return counts


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--path',
    '-f',
    default='.',
    type=str,
    help='the path to search for LaTeX files',
)
@click.option(
    '--word-count/--no-word-count', default=True, help='toggle word counting'
)
def ls(path, word_count):
    """Print out TeX files"""
    tex_files = sorted(
        find_tex_files(path), key=lambda p: os.path.getmtime(p), reverse=True
    )
    longest = len(max(tex_files, key=lambda x: len(x)))
    total_wc = 0
    msg_1, msg_2 = 'File Name', 'Last Mod. Date'
    msg = '{0}{1} --- {2}{3}'.format(
        msg_1,
        ' ' * (longest - len(msg_1) - 2),
        msg_2,
        ' ' * (DT_LEN - len(msg_2))
    )
    if word_count:
        msg_3 = ' --- Word Count'
        msg = msg + msg_3
    click.secho(msg, fg='red')
    click.echo('-' * len(msg))
    for elem in tex_files:
        pad = ' ' * (longest - len(elem))
        msg = '{0}{2} --- {1:%Y-%m-%d %H:%M:%S}'.format(
            os.path.relpath(elem),
            datetime.fromtimestamp(os.path.getmtime(elem)),
            pad,
        )
        if word_count:
            count = wc(elem)
            msg = msg + ' --- {0}'.format(count)
            total_wc += count
        click.echo(msg)
    if word_count:
        click.secho('\nTotal Word Count: {0}'.format(total_wc), fg='blue')


@cli.command()
@click.option(
    '--file', '-f', type=str, default=log_file, help='path to the output file'
)
def log(file):
    """Save all word counts to a log"""
    now = datetime.utcnow()
    entry = {}
    entry['datetime'] = DT_FMT.format(now)
    entry['files'] = {}
    total = 0
    for file, count in word_counts():
        entry['files'][file] = count
        total += count
    entry['total'] = total
    if not os.path.isfile(log_file):
        log_cts = []
    else:
        log_cts = get_log()
    if log_cts:
        last_ent = datetime.strptime(log_cts[-1]['datetime'], STRP_FMT)
        if last_ent.day == now.day:
            log_cts.pop()
    log_cts.append(entry)
    save_log(log_cts)


if __name__ == '__main__':
    cli()
