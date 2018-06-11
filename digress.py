"""digress.py: a CLI tool with functionality related to the ButIDigress project
"""
from datetime import datetime
import os
import re
import shutil
from subprocess import run, CompletedProcess, PIPE
from typing import (
    Text, Dict, Union, List, Tuple, Match, Pattern, Callable, Optional
)

import click
import profilehooks

try:
    import ujson as json
except ImportError:
    import json

# Typing Stuff
PathType = Text
EntriesDict = Dict[str, Union[str, Dict[str, int], int]]
WordCountsDict = Dict[PathType, int]
WordCountsTup = List[Tuple[PathType, int]]
RowsTup = Tuple[PathType, int, int]
ArgsType = List[Union[PathType, str]]
SortFnType = Callable[[RowsTup], Union[str, int]]
SortFnRet = Tuple[SortFnType, bool]
WhichType = Optional[PathType]

# regex used to find word count in texcount output
WORDS_RE: Pattern[str] = re.compile(r'Words in text: (\d+)')

HERE: PathType = os.path.split(os.path.abspath(__file__))[0]
LOG_FILE: PathType = os.path.join(HERE, 'counts.json')

DT_FMT: Text = '{0:%Y-%m-%d %H:%M:%S}'
STRP_FMT: Text = DT_FMT[3:-1]
DT_LEN: int = len('YYYY-MM-DD HH:MM:SS')

tex_dir: PathType = os.path.join('C:\\', 'texlive', '2017', 'bin', 'win32')
lualatex_exe: WhichType = shutil.which(os.path.join(tex_dir, 'lualatex.exe'))
biber_exe: WhichType = shutil.which(os.path.join(tex_dir, 'biber.exe'))

sumatra_exe: WhichType = shutil.which(os.path.join(
    os.environ['PROGRAMFILES'], 'SumatraPDF', 'SumatraPDF.exe'))
if sumatra_exe is None:
    sumatra_exe: WhichType = shutil.which(os.path.join(
        os.environ['PROGRAMFILES(X86)'], 'SumatraPDF', 'SumatraPDF.exe'))

output_dir = 'build'

latexopts: List[str] = [
    '-interaction=nonstopmode',
    '-synctex=1',
    '--output-directory={0}'.format(output_dir),
    '--shell-escape',
]
biber_opts: List[str] = ['--output-directory={0}'.format(output_dir)]


def latex_build(base_name: str) -> Optional[PathType]:
    tex_file: PathType = os.path.abspath(base_name + '.tex')
    if not os.path.isfile(tex_file):
        raise click.Abort('{0} not found'.format(tex_file))

    tex_args: ArgsType = [lualatex_exe] + latexopts + [tex_file]
    biber_args: ArgsType = [biber_exe] + biber_opts + [base_name]

    # First Latex Compile
    c: CompletedProcess = run(tex_args, shell=True)

    # Run Biber
    c: CompletedProcess = run(biber_args, shell=True)

    # Second Latex Compile
    c: CompletedProcess = run(tex_args, shell=True)

    # Third Latex Compile
    c: CompletedProcess = run(tex_args, shell=True)

    out_file = os.path.join(os.path.abspath(output_dir), base_name + '.pdf')
    return out_file if os.path.exists(out_file) else None


def save_log(entry: EntriesDict) -> Union[bool, int]:
    """Saves the log file, overwrites existing entry from today with input"""
    now: datetime = datetime.utcnow()
    entry['datetime'] = DT_FMT.format(now)
    if not os.path.isfile(LOG_FILE):
        log_cts: List[EntriesDict] = []
    else:
        log_cts: List[EntriesDict] = get_log()

    if log_cts:
        last_ent: datetime = datetime.strptime(
            log_cts[-1]['datetime'], STRP_FMT
        )
        if last_ent.day == now.day:
            log_cts.pop()
    log_cts.append(entry)

    with open(LOG_FILE, 'wt') as f:
        json.dump(log_cts, f, indent=4)
    return os.path.isfile(LOG_FILE) and os.path.getsize(LOG_FILE)


def get_log() -> List[EntriesDict]:
    """Fetch log file contents"""
    with open(LOG_FILE, 'rt') as f:
        return json.load(f)


def wc(file: PathType, verbose: bool = False) -> int:
    """Run texcount on the input file

    file: path to a latex file (hopefully)
    verbose: print status commands
    """
    if verbose:
        click.secho(
            'running texcount on: {0} --- '.format(file), fg='green', nl=False
        )
    args: ArgsType = ['texcount', file]
    s: CompletedProcess = run(args, shell=True, stdout=PIPE)
    res: Match[str] = WORDS_RE.search(s.stdout.decode())
    ret: int = 0 if not res else int(res.group(1))
    if verbose:
        click.secho(str(ret), fg='green')

    return ret


def find_tex_files(path: PathType) -> List[PathType]:
    """Walks the given path and returns files with the extension .tex"""
    tex_files: List[PathType] = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    return tex_files


def word_counts(path: PathType) -> WordCountsDict:
    """Runs texcount on all LaTex files in the given path"""
    counts: WordCountsDict = {}
    for file in find_tex_files(path):
        counts[file] = wc(file)
    return counts


def ls_log(rows: List[RowsTup]):
    """The logging function run by the ls command"""
    entry: EntriesDict = {'files': {}}
    total: int = 0
    for name, _, count in rows:
        entry['files'][name] = count
        total += count
    entry['total'] = total
    save_log(entry)


_sort_opts: List[str] = ['name', 'mdate', 'wc']


def _choose_sort_fn(sort: str) -> SortFnRet:
    """Generates a sort function from a given option"""
    sort = sort.lower()
    assert sort in _sort_opts
    if sort == 'name':

        def _sort_fn(e: RowsTup) -> str:
            return e[0]

        reverse = False
    elif sort == 'mdate':

        def _sort_fn(e: RowsTup) -> int:
            return os.path.getmtime(e[0])

        reverse = True
    else:

        def _sort_fn(e: RowsTup) -> int:
            return e[2]

        reverse = True
    return _sort_fn, reverse


@click.group()
def cli():
    """digress.py"""
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
    '--sort',
    '-s',
    type=click.Choice(_sort_opts),
    default='mdate',
    help='sort rows by column',
)
def ls(path: PathType, sort: str):
    """Print out TeX files"""
    click.clear()
    tex_files: List[PathType] = find_tex_files(path)
    longest: int = len(max(tex_files, key=lambda x: len(x)))

    col_1: str = 'File Name'
    col_2: str = 'Last Mod. Date'
    col_3: str = 'Word Count'
    hdr: str = '\n{0}{1} --- {2}{3} --- {4}'.format(
        col_1,
        ' ' * (longest - len(col_1) - 2),
        col_2,
        ' ' * (DT_LEN - len(col_2)),
        col_3
    )

    _sort_fn, reverse = _choose_sort_fn(sort)

    rows: List[RowsTup] = sorted(
        (
            [
                os.path.relpath(p),
                datetime.fromtimestamp(os.path.getmtime(p)),
                wc(p, True),
            ]
            for p in tex_files
        ),
        key=_sort_fn,
        reverse=reverse,
    )
    total_wc: int = 0
    p_rows: List[str] = []
    for elem in rows:
        pad: str = ' ' * (longest - len(elem[0]))
        msg: str = '{0}{2} --- {1:%Y-%m-%d %H:%M:%S} --- {3}'.format(
            elem[0], elem[1], pad, elem[2]
        )
        total_wc += elem[2]
        p_rows.append(msg)
    click.secho(hdr, fg='red')
    click.echo('-' * len(hdr))
    for row in p_rows:
        click.echo(row)
    click.secho('\nTotal Word Count: {0}'.format(total_wc), fg='blue')
    ls_log(rows)


@cli.command()
@click.option(
    '--file',
    '-f',
    type=click.Path(),
    default=LOG_FILE,
    help='path to the output file',
)
def log(file: PathType):
    """Save all word counts to a log"""
    counts: WordCountsDict = word_counts('.')
    entry: EntriesDict = {'files': counts}
    entry['total'] = sum(counts.values())
    save_log(entry)


@cli.command()
@click.option(
    '--path',
    '-f',
    default='.',
    type=click.Path(),
    help='the path to search for LaTeX files',
)
@click.option(
    '--linter',
    '-l',
    type=click.Choice(['lacheck', 'chktex']),
    default='lacheck',
)
def check(path: PathType, linter: str):
    """Run lacheck on all files"""
    exe: Optional[PathType] = shutil.which(linter)
    if exe is None:
        click.secho('{0} not found on PATH'.format(linter), err=True, fg='red')
        return -1

    ret: int = 0
    for file in find_tex_files(path):
        s: CompletedProcess = run([exe, file], stdout=PIPE)
        if s.stdout:
            click.secho(os.path.relpath(file), fg='blue')
            click.echo(s.stdout.decode())
        ret &= s.returncode
    return ret


@cli.command()
@click.option('--base-name', type=str, default='butidigress')
@click.option('--view/--no-view', default=True)
def build(base_name: str, view: bool):
    """Build butidigress.pdf (assumes a lot)"""
    if lualatex_exe is None:
        click.secho(
            '{0} not found, aborting'.format(lualatex_exe), fg='red', err=True
        )
        return -1

    if biber_exe is None:
        click.secho(
            '{0} not found, aborting'.format(biber_exe), fg='red', err=True
        )
        return -1
    out_file: Optional[PathType] = latex_build(base_name)
    if out_file is not None and view:
        if sumatra_exe is not None:
            from subprocess import Popen
            Popen([sumatra_exe, '-reuse-instance', out_file], shell=True)
    else:
        click.secho('Failed to create output file', fg='red', err=True)


if __name__ == '__main__':
    cli()
