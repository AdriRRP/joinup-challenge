import sys
from pathlib import Path


# Add lib and app folders to path
LIBS_DIR = (Path(__file__).resolve()
            .parent  # ../django_project
            .parent  # ../django_project
            .parent  # ../infrastructure
            .parent  # ../challenge
            .parent  # ../app
            .parent  # ../{root}
            )
sys.path.append(str(LIBS_DIR))
