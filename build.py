import os


if __name__ == '__main__':
    texlive_dir = os.path.realpath('C:\\texlive\\2017\\bin\\win32')
    latex_exe = os.path.join(texlive_dir, 'lualatex.exe')
    biber_exe = os.path.join(texlive_dir, 'biber.exe')
    print(os.path.isfile(latex_exe))
    print(os.path.isfile(biber_exe))
    lualatexopts = '-interaction=nonstopmode -synctex=1 --shell-escape'
    bibercmd = 'C:\\texlive\\2017\\bin\\win32\\biber.EXE'
