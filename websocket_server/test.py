import sys
import os

# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add the parent directory to the Python path)

sys.path.append(parent_dir)

print(sys.path)
