```markdown
# RedTE
A MARL-based distributed traffic engineering system

# Environment Setup

## Topology Selection
Choose topologies: GEANT (23, 36) and Abi (12, 15).
How to choose:
When changing the topology, simply modify the `${topoName}` in the training (train.sh) and inference (valid.sh) scripts.

# Training

## Batch Execution

Run the command:
```bash
bash train.sh  # (train.sh will loop call run_train.sh)
```

1) Run in the background.

2) Log information from the run is stored in `../train_abi_log/`.

3) Intermediate training results (performance ratio) are saved in the folder `../log/log/hyper1-hyper2-hyper3..-hyperx`, controlled by the `--stamp_type` parameter in run_train.sh.

# Inference

## Batch Execution

Run the command:
```bash
bash valid.sh  # (valid.sh will continuously loop run_valid.sh)
```

In addition to the parameters used in training, an extra parameter `ckpt_idx` will be introduced to traverse all checkpoints for each set of parameters.

Test performance results are saved in `../DRLTE/log/validRes/`, controlled by the `--stamp_type` parameter in run_test.sh.

Additionally, `test_epoch=1` and `test_episode=500` are used to control the total number of inference test steps.

# Input File Descriptions

All input files are located in `DRLTE/inputs/`.

* File One: 
  `\${topoName}\_pf\_trueTM\_train4000.txt`: Records the optimal solution (maximum link utilization) obtained from linear programming. This value is used as the denominator for calculating the reward. `topoName` indicates the topology name, stored under the current `topoName`.
  This file needs to be specified in the run script: `lpPerformFile=../inputs/\${topoName}\_pf\_train4000.txt`.

* File Two:
  `\${topoName}\_train4000`: Records candidate paths and traffic matrices. The `topoName` indicates the topology name, stored under the current `topoName`. 
  This file also needs to be specified in the run script: `file_name=\${topoName}\_train4000`.

* File Three: Topology file. 
  This needs to be specified in the run script: `topoName=GEA`.

# TBD
there are some codes which are lost in this version of RedTE, which latter maybe uploaded if founded.

```