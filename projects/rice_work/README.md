# Chromatin simulation of radiation-induced breaks

Python for OpenMiChroM simulations of how chromosome structure responds to low-dose radiation, plus post-processing that builds Hi-C contact maps, metrics, and plots. Two smaller folders hold generic shell and process-pool helpers.

## Context

I did this as a Research Intern at Rice University, Center for Theoretical Biological Physics, Jun 2025 to Aug 2025.

The project simulated chromosome structural response to low-dose radiation (radiation-induced breaks) using OpenMiChroM on Rice's NOTS HPC cluster. Multiple simulation jobs ran via Slurm, and scripts were further parallelized with Python multiprocessing. Post-processing was automated to generate Hi-C contact maps, quantitative metrics, and visualizations. Results were compared against literature baselines. I presented the work as a research poster at the Center for Theoretical Biological Physics Undergraduate Research Day.

The homepage's chromatin project points at `projects/rice_work`. The analysis code is under `wsl_copies/`. It reads multi-replica trajectories of two chains (`nucleus0_<sim>.cndb` and `nucleus1_<sim>.cndb`), with a run id taken from `masterVars.csv` or a `--split` argument. Plot titles and one collapsed-trajectory filename refer to chromosome 10. Several scripts compare four split indexes hardcoded in the plotting loops: 1356, 1722, 2012, and 2363. Those indexes are break points.

`basic_cmd/` and `local_parallel/` are a shell snippet, two git wrappers, and a local process pool. A comment in `gitPush.py` mentions a poker-bot commit message.

The analysis scripts choose a data directory from the machine they run on, with one layout on a workstation and another on the cluster. This page describes the files they expect and omits machine-specific paths.

## What I built

Trajectory side, all under `wsl_copies/`:

- Load `.cndb` trajectories with OpenMiChroM's `cndbTools`, look up a bead's XYZ, and measure Euclidean distance (`xyzFuncs.py`).
- Stack both chains' bead coordinates for the selected replicas, pass that array to `traj2HiC`, and save contact maps. Difference maps subtract a log-scaled reference map (the collapsed chromosome trajectory, frames 50–99 in `newHiCplotter.py`) and draw a lime cross at a split index. Default `traj2HiC` arguments in these files are `mu=3.22` and `rc=1.78`.
- Read per-replica `statistics.txt` files, average the radius of gyration, and plot it (`RgFuncs.py`). A value above 1000 is recorded as an "exploded" replica.
- Measure distance between the two chains' centers of mass, and distance between an endpoint of chain 0 and the first bead of chain 1. Write per-frame CSVs and overlay plots (`sepFuncs.py`, `center_of_mass.py`).
- Copy replica statistics and `.cndb` files into local folders (`locStats.py`, `locTrajs.py`).
- `split_runner.py` shells out to `ndb2pdb_mod.py`, `chop.py`, `pdb2ndb_mod.py`, and `split.py` to cut one chromosome structure into two `.ndb` files. Those four programs are not in this repository.
- `cmd_runner.py` copies figure files off the cluster with `scp`, and can convert an image with ImageMagick `convert`.

Helpers:

- `basic_cmd/runCmd.py` runs one shell command from Python.
- `basic_cmd/gitPush.py` and `basic_cmd/gitRm.py` add or untrack a path, commit, and push.
- `local_parallel/multiprocess.py` starts a list of `multiprocessing.Process` objects with a cap, and `multiprocessTest.py` times a serial loop against that pool.

`back_scripts/` also contains earlier copies of the Hi-C plotter (`BackupHiCplotter.py`, `v1.0_frame_by_frame_HiC_plotter.py`, `frame_by_frame_HiC_plotter.py`, `HiCAnalysis.py`, `newHiCout.py`) and a scratch file, `testing.py`.

## Tech stack

Used by the analysis scripts that are more than a shell wrapper:

- Python standard library: `os`, `subprocess`, `argparse`, `time`, `multiprocessing`
- [OpenMiChroM](https://open-michrom.readthedocs.io/) `CndbTools` (load trajectories, `traj2HiC`)
- NumPy, SciPy (`scipy.spatial.distance`), Matplotlib, pandas

`cmd_runner.py` also calls `scp` and ImageMagick `convert`. `split_runner.py` calls external Python scripts that are not checked in. `xyzFuncs.py` reads `masterVars.csv` from the script directory. That CSV is not in the repository.

The helper scripts use only the standard library (`subprocess`, `argparse`, `os`, `multiprocessing`, `time`).

## How it works

`xyzFuncs.defTrajs` fills a global dict `trajs[sim][chain]` from `locTrajs<id>/nucleus{0,1}_<sim>.cndb`. Hi-C plotters stack both chains' coordinates for a frame, pass that array to `cndbTools.traj2HiC`, and save a TIFF under a figures directory. Difference plots use `log` after lifting values below `1e-5`, with a seismic colormap clipped at ±12, and a cross at the split index.

Radius-of-gyration code treats one report row in `statistics<sim>.txt` as the Rg at that step. With `frames = 1000` and `pow = 5`, the step stride is `10**5 / 1000`. The same stride is used as the x-axis when plotting separation (`(frame + 1) * 10**(pow - 3)`).

Endpoint separation writes, for each frame, the coordinates of one bead on each chain and the distance between them, then averages that distance across replicas. Center-of-mass separation averages all bead coordinates in each chain per frame and takes the Euclidean distance between those two means.

Most of these files do the work at import time. Running the file is the job. There is no shared command-line interface across the folder. `RgFuncs.py`, `sepFuncs.py`, `center_of_mass.py`, and `newHiCplotter.py` accept an optional `--split` value and otherwise take the id from `masterVars.csv`.

`split_runner.splitChromosome` runs the four external converters, deletes intermediate files, and moves `C1.ndb` and `C2.ndb` into a `move/` directory. `splitMult` repeats that cut, naming the pieces `Chr1.ndb`, `Chr2.ndb`, and so on. The length used to place an automatic cut is parsed as four characters from line 7 of the input file. The call at the bottom of the file passes an explicit cut index instead.

`runProcesses` keeps at most `os.cpu_count() - 3` processes alive, then joins whatever is still alive. `newHiCplotter.py` halves that cap again before starting.

## How to run

Running the chromatin scripts needs inputs this checkout does not have. Importing `xyzFuncs.py` opens `masterVars.csv`, which is absent. The trajectory files (`.cndb`, `.ndb`, `.pdb`) and figure outputs (`.tiff`) are gitignored at the repository root. The scripts that run on import look for those files on a machine path outside the repo, and `split_runner.py` calls converters that live outside this folder. `cmd_runner.py` starts an `scp` as soon as it is executed.

Two helpers run locally with the standard library:

```bash
python3 projects/rice_work/basic_cmd/runCmd.py
```

That prints `hello_world`.

```bash
cd projects/rice_work/local_parallel
python3 multiprocessTest.py
```

Run that one from `local_parallel/` so `import multiprocess` loads the sibling file. The checked-in test sleeps one second, twenty times, first in a loop and then through the pool. A busy loop in the same file is commented out.

`gitPush.py` and `gitRm.py` also run, and they change git state. `gitPush.py` defaults to `git add` on `../../..`, commits with message `default_commit`, and runs `git push -u origin main`. `gitRm.py` requires `-f PATH`, then `git rm -r --cached`, a commit, and `git push`.

## Repo contents

| File | What it does |
|---|---|
| `basic_cmd/runCmd.py` | Runs `echo hello_world` through `subprocess`. |
| `basic_cmd/gitPush.py` | `git add` a path (default `../../..`), commit, and `git push -u origin main`. |
| `basic_cmd/gitRm.py` | `git rm -r --cached` a required path, commit, and push. |
| `local_parallel/multiprocess.py` | Starts a list of processes, capped by CPU count minus 3, then joins the ones still running. |
| `local_parallel/multiprocessTest.py` | Times 20 serial one-second sleeps against the same work submitted to `runProcesses`. |
| `wsl_copies/split_runner.py` | Calls external converters to split one chromosome file at a bead index into two `.ndb` chains. Runs a split as soon as the file is executed. |
| `wsl_copies/back_scripts/xyzFuncs.py` | Loads `.cndb` trajectories, reads the run id from `masterVars.csv`, and returns bead coordinates and distances. |
| `wsl_copies/back_scripts/newHiCplotter.py` | Builds Hi-C and Hi-C-difference TIFFs for selected frames. On execution, plots frames 0, 100, and 999 with subtraction. |
| `wsl_copies/back_scripts/frame_by_frame_HiC_plotter.py` | Earlier interactive-style Hi-C plotter. The prompts are commented out and replaced with a fixed trajectory folder, all frames, difference maps on, parallel off. |
| `wsl_copies/back_scripts/v1.0_frame_by_frame_HiC_plotter.py` | Older Hi-C plotter. Prompts on stdin for the trajectory folder, sims, frames, step size, and whether to draw difference maps in parallel. Optional flags `--mu`, `--rc`, `--endFrames`, and `--initTraj`. Expects `chain0sim<n>.cndb` names. |
| `wsl_copies/back_scripts/BackupHiCplotter.py` | Older Hi-C plotter. On execution, calls `plotHiCs` for every frame with subtraction. |
| `wsl_copies/back_scripts/HiCAnalysis.py` | Partial copy of the Hi-C helpers (`findMaxNotOnDiag`, a printed window, probability-versus-distance, `plotHiC`). No import lines. |
| `wsl_copies/back_scripts/newHiCout.py` | Loads trajectories, writes a bead-coordinate window to `boxVals.txt`, builds Hi-C matrices for frames 0 and 15, and writes an 11-row comparison against `av0.txt`, `av15.txt`, and `difflog.txt` into `CompareHiCAvgs.txt`. |
| `wsl_copies/back_scripts/RgFuncs.py` | Averages radius of gyration from `statistics` files and plots it. On execution, overlays four split ids from cluster CSV paths. |
| `wsl_copies/back_scripts/sepFuncs.py` | Writes endpoint-separation CSVs and plots averages. On execution, overlays four split ids from `SepAvgs.csv`. |
| `wsl_copies/back_scripts/center_of_mass.py` | Loads trajectories and plots the mean center-of-mass distance between the two chains. Runs that plot on execution. |
| `wsl_copies/back_scripts/locStats.py` | Copies `sim<n>/statistics.txt` into `locStats<id>/`. On execution, copies 100 replicas. |
| `wsl_copies/back_scripts/locTrajs.py` | Copies `nucleus_0.cndb` and `nucleus_1.cndb` into `locTrajs<id>/` as `nucleus0_<sim>.cndb` and `nucleus1_<sim>.cndb`. On execution, copies 100 replicas. |
| `wsl_copies/back_scripts/cmd_runner.py` | `scp` figure TIFFs off the cluster for a hardcoded split id and frame list. Also has an ImageMagick convert helper. |
| `wsl_copies/back_scripts/testing.py` | Scratch file. Prints `testing`, then builds a small NumPy array and prints a window of it. Most of the file is commented out. |
| `wsl_copies/back_scripts/CompareHiCAvgs.txt` | Output of `newHiCout.py`: 11-row windows for frames 0 and 15, the log-difference, and the comparison text, interleaved. |
| `wsl_copies/back_scripts/boxVals.txt` | Output of `newHiCout.py`: bead coordinates in a window around the split, frames 0 and 15, simulations 1–3. |

## Notes / limitations

The comparison to literature baselines and the poster are noted above. This folder does not include the poster, a literature citation, or a measured outcome. Plot titles, the four break-point indexes, and the chromosome-10 filename are what the scripts contain.

The analysis scripts are tied to one directory layout: per-replica `sim<n>/` folders, a `locTrajs<id>/` copy, a `locStats<id>/` copy, and output under `Figs<id>/`. Several files assume 1000 frames. Some use 100 replicas on the cluster and 3 replicas in the workstation layout.

`findXYZ` returns `traj.cndb[frame][bead - 1]`. Endpoint code calls it with `-1` for chain 0 and `1` for chain 1. The comment at the call says those are the last bead and the first bead.

`HiCAnalysis.py` uses NumPy and Matplotlib names and contains no import lines. `newHiCplotter.init_HiC` has a bare `p` expression after a `return`, which is unreachable. The comment on `plotSeps` mentions `RgAvgs.csv`; the function reads `SepAvgs.csv`.

`runProcesses` can compute a non-positive cap when the machine has fewer than three CPUs. The copy inside `newHiCplotter.py` then divides that cap by two, so the cap becomes a float.

`CompareHiCAvgs.txt` and `boxVals.txt` are raw numeric output sitting next to the scripts. The root gitignore already excludes `*.csv`, `*.cndb`, `*.ndb`, `*.pdb`, and `*.tiff`, which is why the inputs these scripts expect are absent while these two text dumps are present.

<!-- TODO(Travis): Which scripts should a recruiter treat as the project, and which are scratch? The four split indexes are break points — what is each index specifically? Is chromosome 10 the system you want named? What was your part versus the lab's existing OpenMiChroM pipeline? Should the two text dumps stay in the public repo? Any specific finding you want quoted is still open. -->

**[TODO: What is each break-point index? Which scripts are the project versus scratch? Is chromosome 10 the system to name? What was your part versus the lab pipeline? Should the two text dumps stay public? Any finding to quote?]**
