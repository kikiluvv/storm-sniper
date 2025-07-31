import os

project_structure = {
    'app': {
        '__init__.py': '',
        'main.py': '"""Entrypoint for OpenRedirectHunter PyQt5 GUI app."""\n\n',
        'ui': {
            '__init__.py': '',
            'main_window.py': '"""MainWindow UI and logic."""\n\n',
            'components.py': '"""Reusable UI components/widgets."""\n\n',
        },
        'core': {
            '__init__.py': '',
            'storm.py': '"""Storm mode: bulk fast fuzzing logic."""\n\n',
            'snipe.py': '"""Snipe mode: detailed focused fuzzing logic."""\n\n',
            'payloads.py': '"""Payloads and payload management."""\n\n',
            'detector.py': '"""Redirect detection logic."""\n\n',
        },
        'workers': {
            '__init__.py': '',
            'fuzz_worker.py': '"""Async QThread worker for fuzzing tasks."""\n\n',
        },
        'utils': {
            '__init__.py': '',
            'logging.py': '"""Logging helpers and custom handlers."""\n\n',
        },
        'config.py': '"""App-wide configuration constants and defaults."""\n\n',
    },
    'tests': {
        '__init__.py': '',
        'test_storm.py': '"""Tests for storm mode logic."""\n\n',
    },
    'requirements.txt': '# PyQt5, aiohttp, tqdm, etc.\n',
    'README.md': '# OpenRedirectHunter\n\nA PyQt5 GUI tool for finding open redirect vulnerabilities.\n',
    '.gitignore': '__pycache__/\n*.pyc\n.env\n',
    'setup.py': '# Setup script for packaging\n',
}

def create_files(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_files(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == '__main__':
    create_files('.', project_structure)
    print("Scaffold complete! Folders and files created.")
