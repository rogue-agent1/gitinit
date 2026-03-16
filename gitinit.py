#!/usr/bin/env python3
"""gitinit - Initialize projects with templates and best practices."""
import os, argparse, subprocess, time

GITIGNORES = {
    'python': '__pycache__/\n*.py[cod]\n*$py.class\n*.egg-info/\ndist/\nbuild/\n.venv/\nvenv/\n*.egg\n.env\n',
    'node': 'node_modules/\ndist/\nbuild/\n.env\ncoverage/\n*.log\n',
    'go': 'bin/\n*.exe\n*.test\n*.out\nvendor/\n',
    'rust': 'target/\nCargo.lock\n',
    'general': '.DS_Store\n*.swp\n*.swo\n*~\n.env\n.idea/\n.vscode/\n',
}

TEMPLATES = {
    'python': {
        'main.py': '#!/usr/bin/env python3\n"""{{name}} - TODO: description."""\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()\n',
        'requirements.txt': '',
        'tests/__init__.py': '',
        'tests/test_main.py': 'import unittest\n\nclass TestMain(unittest.TestCase):\n    def test_placeholder(self):\n        self.assertTrue(True)\n\nif __name__ == "__main__":\n    unittest.main()\n',
    },
    'node': {
        'index.js': '// {{name}}\nconsole.log("Hello from {{name}}");\n',
        'package.json': '{\n  "name": "{{name}}",\n  "version": "1.0.0",\n  "main": "index.js",\n  "scripts": {"test": "echo \\"no tests\\"", "start": "node index.js"}\n}\n',
    },
    'go': {
        'main.go': 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("Hello from {{name}}")\n}\n',
        'go.mod': 'module {{name}}\n\ngo 1.21\n',
    },
    'cli': {
        '{{name}}.py': '#!/usr/bin/env python3\n"""{{name}} - TODO."""\nimport argparse\n\ndef main():\n    p = argparse.ArgumentParser(description="{{name}}")\n    args = p.parse_args()\n\nif __name__ == "__main__":\n    main()\n',
    },
}

def create_project(name, template, path=None, git=True, remote=False):
    base = path or name
    os.makedirs(base, exist_ok=True)
    
    # Files
    files = TEMPLATES.get(template, TEMPLATES['python'])
    for fpath, content in files.items():
        fpath = fpath.replace('{{name}}', name)
        content = content.replace('{{name}}', name)
        full = os.path.join(base, fpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w') as f: f.write(content)
        print(f"  + {fpath}")
    
    # .gitignore
    gi_content = GITIGNORES.get(template, GITIGNORES['general'])
    with open(os.path.join(base, '.gitignore'), 'w') as f:
        f.write(GITIGNORES['general'] + gi_content)
    print(f"  + .gitignore")
    
    # README
    with open(os.path.join(base, 'README.md'), 'w') as f:
        f.write(f"# {name}\n\nTODO: description\n\n## Usage\n\n```bash\n# TODO\n```\n")
    print(f"  + README.md")
    
    # LICENSE
    with open(os.path.join(base, 'LICENSE'), 'w') as f:
        f.write(f"MIT License\n\nCopyright (c) {time.strftime('%Y')}\n\nPermission is hereby granted...\n")
    print(f"  + LICENSE")
    
    # Git
    if git:
        subprocess.run(['git', 'init', '-q'], cwd=base)
        subprocess.run(['git', 'add', '-A'], cwd=base)
        subprocess.run(['git', 'commit', '-q', '-m', f'Initial commit: {name}'], cwd=base)
        print(f"  ✓ git initialized")

def main():
    p = argparse.ArgumentParser(description='Project scaffold generator')
    p.add_argument('name', help='Project name')
    p.add_argument('-t', '--template', choices=list(TEMPLATES.keys()), default='python')
    p.add_argument('-p', '--path', help='Custom path')
    p.add_argument('--no-git', action='store_true')
    p.add_argument('--list', action='store_true', help='List templates')
    args = p.parse_args()

    if args.list:
        for t, files in TEMPLATES.items():
            print(f"  {t}: {', '.join(files.keys())}")
        return

    print(f"Creating {args.name} ({args.template}):")
    create_project(args.name, args.template, args.path, not args.no_git)
    print(f"\n✓ Project {args.name} created!")

if __name__ == '__main__':
    main()
