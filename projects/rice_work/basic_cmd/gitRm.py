import subprocess
import argparse

parser = argparse.ArgumentParser(description="Push this repository to github")
parser.add_argument("-f", required=True, help="root directory of what's being taken off the repository")


args = parser.parse_args()

subprocess.run(f"git rm -r --cached {args.f}",shell=True, check=True)
subprocess.run(f"git commit -m \"Stop tracking private folder\"",shell=True, check=True)
subprocess.run(f"git push",shell=True, check=True)


# git rm -r --cached .
# git commit -m "Stop tracking private folder"
# git push