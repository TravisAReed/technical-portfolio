import subprocess
import argparse

parser = argparse.ArgumentParser(description="Push this repository to github")
parser.add_argument("-f", default="../../..", help="root directory of what's being pushed")
parser.add_argument("-n", default="default_commit", help="name of commmit")


args = parser.parse_args()

subprocess.run(f"git add {args.f}",shell=True, check=True)
subprocess.run(f"git commit -m {args.n}",shell=True, check=True)
subprocess.run(f"git push -u origin main",shell=True, check=True)

# git add .
# git commit -m "poker bot"
# git push -u origin main