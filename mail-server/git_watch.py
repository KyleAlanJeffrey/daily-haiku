# Check for any changes in the git repository and publish them to the server
import os
from pathlib import Path
import subprocess

curr_dir = Path(__file__).resolve().parent
# Define the path to your git repository
repo_path = curr_dir
commit_message = lambda s: f"Auto-commit: {s}"

# Change the current working directory to the repo
print(f"Changing working directory to {repo_path}")
os.chdir(repo_path)


# Function to run a shell command and get output
def run_command(command):
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )
    return result.stdout.strip(), result.stderr.strip()


# Check if there are any changes
status_output, _ = run_command("git status --porcelain")
print(f"Git status: {status_output}")
if status_output:
    # Stage all changes
    print("Staging changes...")
    run_command("git add .")

    # Commit the changes
    print(f"Committing changes with message: {commit_message(status_output)}")
    run_command(f'git commit -m "{commit_message(status_output)}"')

    # Push the changes to the remote repository
    push_output, push_error = run_command("git push")

    if push_error:
        print(f"Error pushing changes: {push_error}")
    else:
        print("Changes committed and pushed successfully.")
else:
    print("No changes detected.")
