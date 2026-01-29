# Example of a safer approach (still needs thorough argument validation):
import subprocess
import shlex
import re
  
# Define allowed commands and their expected arguments/patterns
ALLOWED_COMMANDS = {
              "ls": {
                  "args_whitelist": ["-l", "-a", "-h", "--color=auto"],
                  "paths_regex": r"^[a-zA-Z0-9_\-./]+$" # Basic, needs refinement for security
              },
              "cat": {
                  "args_whitelist": [],
                  "paths_regex": r"^[a-zA-Z0-9_\-./]+\.txt$" # Only allow specific file types
              }
          }
  
def run_safe_command(command_name, user_args_string):
              if command_name not in ALLOWED_COMMANDS:
                  raise ValueError(f"Command '{command_name}' is not allowed.")
  
              allowed_config = ALLOWED_COMMANDS[command_name]
              args = shlex.split(user_args_string)
              validated_args = []
  
              for arg in args:
                  if arg.startswith('-'):
                      if arg not in allowed_config.get("args_whitelist", []):
                          raise ValueError(f"Argument '{arg}' not allowed for command '{command_name}'.")
                  elif "paths_regex" in allowed_config:
                      if not re.fullmatch(allowed_config["paths_regex"], arg):
                          raise ValueError(f"Path argument '{arg}' not valid for command '{command_name}'.")
                  else: # No path validation defined, potentially unsafe
                      raise ValueError(f"Argument '{arg}' type not handled for command '{command_name}'.")
                  validated_args.append(arg)
  
              full_command = [command_name] + validated_args
              try:
                  result = subprocess.run(full_command, capture_output=True, text=True, check=True)
                  return result.stdout, result.stderr
              except subprocess.CalledProcessError as e:
                  raise RuntimeError(f"Command failed: {e.stderr}") from e
              except FileNotFoundError:
                  raise RuntimeError(f"Command '{command_name}' not found.")