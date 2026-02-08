import subprocess
import shlex
import os

def run_command(user_input):
    """Run a shell command safely."""
    args = shlex.split(user_input)
    subprocess.call(args, shell=False)

API_KEY = os.environ.get("API_KEY")
