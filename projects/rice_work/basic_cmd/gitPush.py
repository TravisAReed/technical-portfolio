import subprocess
import argparse

parser = argparse.ArgumentParser(description="Push this repository to github")
# parser.add_argument("-f", required=True, help="Write the directory you want to push to Github")
parser.add_argument("-f", default="../../..", help="root directory of what's being pushed")
parser.add_argument("-n", default="default_commit", help="name of commmit")



# try:
#     args = parser.parse_args()
#     root = args.f
#     print('No inputs were given in argument')
# except:
#     # inp = '../move/nucleus1_80.cndb'
#     # inp = '/home/treed777/cluster_runs/collapsed/traj_chr10_0.cndb'
#     root = ''


args = parser.parse_args()

subprocess.run(f"git add {args.f}",shell=True, check=True)
subprocess.run(f"git commit -m {args.n}",shell=True, check=True)
subprocess.run(f"git push -u origin main",shell=True, check=True)

# git add .
# git commit -m "poker bot"
# git push -u origin main