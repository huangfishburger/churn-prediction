import subprocess
import os

files = [
    '01_test.ipynb',
    '02_get_dataset.ipynb',
    '03_feature_split.ipynb',
    '04_LSTM.ipynb'
]

def execute_file(file):
    if file.endswith('.py'):
        subprocess.run(['python', file])
    elif file.endswith('.ipynb'):
        py_file = file.replace('.ipynb', '.py')
        subprocess.run(['jupyter', 'nbconvert', '--to', 'script', file])
        subprocess.run(['python', py_file])
    else:
        print(f"Unsupported file format: {file}")


for file in files:
    try:
        print(f'Executing: {file}')
        execute_file(file)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {file}: {e}")
