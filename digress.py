"""wc.py: a CLI tool with functionality about/around word counts in TeX files

TODO: save each word count to a JSON file
    - each entry would have a datetime and the word counts of each file
    - then we could, in some way, compare across runs
"""
from datetime import datetime
import os
import re
import shutil
import subprocess

# TODO: add type signatures
import typing

import click

try:
    import ujson as json
except ImportError:
    import json

# Typing Stuff
Path = typing.Text
EntriesDict = typing.Dict[str, typing.Dict[Path, int]]
WordCountsTup = typing.List[typing.Tuple[Path, int]]

# regex used to find word count in texcount output
WORDS_RE: typing.re = re.compile(r'Words in text: (\d+)')

HERE: Path = os.path.split(os.path.abspath(__file__))[0]
log_file: Path = os.path.join(HERE, 'counts.json')

DT_FMT: typing.Text = '{0:%Y-%m-%d %H:%M:%S}'
STRP_FMT: typing.Text = DT_FMT[3:-1]
DT_LEN: int = len('YYYY-MM-DD HH:MM:SS')

tex_dir: Path = os.path.join('C:\\', 'texlive', '2017', 'bin', 'win32')
lualatex_exe: Path = shutil.which(os.path.join(tex_dir, 'lualatex.exe'))
biber_exe: Path = shutil.which(os.path.join(tex_dir, 'biber.exe'))
latexopts = ['-interaction=nonstopmode', '-synctex=1', '--shell-escape']


def save_log(entries: EntriesDict) -> typing.Union[bool, int]:
    with open(log_file, 'wt') as f:
        json.dump(entries, f, indent=4)
    return os.path.isfile(log_file) and os.path.getsize(log_file)


def get_log() -> EntriesDict:
    with open(log_file, 'rt') as f:
        return json.load(f)


def wc(file: Path) -> int:
    s = subprocess.run(['texcount', file], stdout=subprocess.PIPE)
    res = WORDS_RE.search(s.stdout.decode())
    if res:
        return int(res.group(1))

    return 0


def find_tex_files(path: Path) -> typing.List[Path]:
    tex_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    return tex_files


def word_counts(path: Path) -> WordCountsTup:
    counts = []
    for file in find_tex_files(path):
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
    type=click.Path(),
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
    '--file',
    '-f',
    type=click.Path(),
    default=log_file,
    help='path to the output file',
)
def log(file):
    """Save all word counts to a log"""
    now = datetime.utcnow()
    entry = {}
    entry['datetime'] = DT_FMT.format(now)
    entry['files'] = {}
    total = 0
    for file, count in word_counts('.'):
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


@cli.command()
@click.option(
    '--path',
    '-f',
    default='.',
    type=click.Path(),
    help='the path to search for LaTeX files',
)
def check(path):
    """Run lacheck on all files"""
    exe = shutil.which('lacheck')
    if exe is None:
        click.secho('lacheck not found on PATH', err=True, fg='red')
        return -1

    ret = 0
    for file in find_tex_files(path):
        s = subprocess.run([exe, file], stdout=subprocess.PIPE)
        if s.stdout:
            click.secho(os.path.relpath(file), fg='blue')
            click.echo(s.stdout.decode())
        ret &= s.returncode
    return ret


@cli.command()
@click.option('--base-name', type=str, default='butidigress')
@click.option('--view/--no-view', default=True)
@click.option('--pdf-viewer', type=click.Path(dir_okay=False))
def build(base_name, view, pdf_viewer):
    """Build butidigress.pdf (assumes a lot)"""
    # TODO: Convert all these asserts to more normal CLI stuff
    assert lualatex_exe is not None
    assert biber_exe is not None
    tex_file = os.path.abspath(base_name + '.tex')
    assert os.path.isfile(tex_file)

    tex_args = [lualatex_exe] + latexopts + [tex_file]

    # First Latex Compile
    c = subprocess.run(tex_args, shell=True)

    # Run Biber
    c = subprocess.run([biber_exe, base_name], shell=True)

    # Second Latex Compile
    c = subprocess.run(tex_args, shell=True)

    # Third Latex Compile
    c = subprocess.run(tex_args, shell=True)


_sort_opts = ['files', 'lines', 'blanks', 'code', 'comments']
_sort_help = 'sort languages based on a column'
_tokei_files_help = 'print out statistics on individual files'


@cli.command()
@click.option('--files', '-f', is_flag=True, help=_tokei_files_help)
@click.option('--sort', '-s', type=click.Choice(_sort_opts), help=_sort_help)
def tokei(files, sort):
    """Run tokei"""
    exe = shutil.which('tokei')
    if exe is None:
        click.secho(
            'tokei not found on PATH, install with `cargo install tokei`',
            err=True,
            fg='red',
        )
        return -1

    args = [exe]
    if files:
        args.append('--files')
    if sort:
        print(sort)
        args.extend(['--sort', sort])
    return subprocess.run(args).returncode


if __name__ == '__main__':
    cli()
