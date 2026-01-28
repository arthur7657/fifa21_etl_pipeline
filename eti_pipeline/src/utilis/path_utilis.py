import os
import sys

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#Path construction logic
def setup_project_path() -> str:
    """Get absolute path to project root directory"""
    current_file = os.path.abspath(__file__)
    utilis_dir = os.path.dirname(current_file)
    src_dir = os.path.dirname(utilis_dir)
    eti_pipeline_dir = os.path.dirname(src_dir)
    project_root = os.path.dirname(eti_pipeline_dir)

    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root

# Auto-setup when imported
PROJECT_ROOT = setup_project_path()

#Optional: Test When run directly

if __name__ == "__main__":
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Python Path includes project root : {PROJECT_ROOT in sys.path}")

    


