import subprocess
import sys
from pathlib import Path


def main():
    changed_files: list = sys.argv[1:]

    projects_to_test: set = set()
    for file_path in changed_files:
        parts = Path(file_path).parts
        if len(parts) > 1:
            project_dir = Path(parts[0])
            if (project_dir / "tests").is_dir():
                projects_to_test.add(project_dir)

    for project in sorted(projects_to_test):
        subprocess.run([sys.executable, "-m", "pytest"], cwd=project)


if __name__ == "__main__":
    main()
