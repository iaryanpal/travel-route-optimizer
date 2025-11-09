"""
Project Structure Setup Script
Run this to create the complete directory structure for the Travel Route Optimizer
"""

import os

def create_project_structure():
    """Creates the complete project directory structure"""
    
    # Define the structure
    structure = {
        'backend': {
            'models': ['__init__.py', 'city.py', 'route.py', 'graph.py', 'trip.py'],
            'algorithms': ['__init__.py', 'dijkstra.py'],
            'data': ['cities.json', 'routes.json'],
            'tests': ['__init__.py', 'test_models.py', 'test_dijkstra.py'],
            'utils': ['__init__.py', 'data_loader.py'],
        },
        'frontend': {
            'static': {
                'css': ['style.css'],
                'js': ['app.js']
            },
            'templates': ['index.html']
        },
        'docs': ['architecture.md', 'api_documentation.md'],
    }
    
    # Root files
    root_files = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        'main.py'
    ]
    
    print("🚀 Setting up Travel Route Optimizer project structure...\n")
    
    # Create directories and files
    for folder, contents in structure.items():
        create_directory_structure(folder, contents)
    
    # Create root files
    for file in root_files:
        create_file(file)
    
    print("\n✅ Project structure created successfully!")
    print("\n📁 Project Structure:")
    print_tree(".", prefix="")

def create_directory_structure(base_path, structure, parent=""):
    """Recursively creates directories and files"""
    full_path = os.path.join(parent, base_path) if parent else base_path
    
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"📂 Created directory: {full_path}")
    
    if isinstance(structure, dict):
        for key, value in structure.items():
            create_directory_structure(key, value, full_path)
    elif isinstance(structure, list):
        for file in structure:
            file_path = os.path.join(full_path, file)
            create_file(file_path)

def create_file(file_path):
    """Creates an empty file if it doesn't exist"""
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            if file_path.endswith('.py'):
                f.write('"""\nTODO: Implementation pending\n"""\n')
        print(f"📄 Created file: {file_path}")

def print_tree(directory, prefix=""):
    """Prints a tree view of the directory structure"""
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return
    
    # Filter out unwanted files
    entries = [e for e in entries if not e.startswith('.') and e != '__pycache__' and e != 'venv']
    
    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = i == len(entries) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{entry}")
        
        if os.path.isdir(path):
            extension_prefix = "    " if is_last else "│   "
            print_tree(path, prefix + extension_prefix)

if __name__ == "__main__":
    create_project_structure()
