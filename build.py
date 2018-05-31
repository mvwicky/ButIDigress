import os
import subprocess


if __name__ == '__main__':
    base_name = 'butidigress'
    tex_file = base_name + '.tex'
    texlive_dir = os.path.realpath('C:\\texlive\\2017\\bin\\win32')
    latex_exe = os.path.join(texlive_dir, 'lualatex.exe')
    biber_exe = os.path.join(texlive_dir, 'biber.exe')
    print(os.path.isfile(latex_exe))
    print(os.path.isfile(biber_exe))
    lualatexopts = ['-interaction=nonstopmode', '-synctex=1', '--shell-escape']
    bibercmd = 'C:\\texlive\\2017\\bin\\win32\\biber.EXE'

    tex_args = [latex_exe] + lualatexopts + [tex_file]
    # First Latex Compile
    c = subprocess.run(tex_args, shell=True)

    # Run Biber
    c = subprocess.run([bibercmd, base_name], shell=True)

    # Second Latex Compile
    c = subprocess.run(tex_args, shell=True)

    # Third Latex Compile
    c = subprocess.run(tex_args, shell=True)
