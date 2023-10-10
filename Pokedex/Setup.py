import subprocess
libraries_to_install = [
    'requests',
    'beautifulsoup4',
    'pandas',
    'Pillow',
    'tk',
    're',
    'numpy',
    'matplotlib',
    'openpyxl'
]

def install_libraries():
    for library in libraries_to_install:
        try:
            subprocess.check_call(['pip', 'install', library])
            print(f'Successfully installed {library}')
        except subprocess.CalledProcessError:
            print(f'Failed to install {library}')

if __name__ == "__main__":
    install_libraries()