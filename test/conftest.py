import sys
import os


project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        'src',
        'stump_data_pipeline',
    )
)

print(project_root)

sys.path.append(project_root)
