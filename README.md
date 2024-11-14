# RedTE
A MARL-based distributed traffic engineering system


# 环境准备

查看requirements.txt

选择拓扑： GEANT（23，36） 和 Abi(12, 15);
如何选择：
当更换拓扑时，只需要修改训练（train.sh）和推理(valid.sh)脚本的${topoName} 即可。



# 训练

## 批量运行

bash train.sh  （train.sh会循环调用run_train.sh）

1）后台运行

2）运行的log信息存储在../train_abi_log/中

3）训练的中间结果（performance ratio）保存在 ```../log/log/hyper1-hyper2-hyper3..-hyperx``` 文件夹中, 由run_train.sh的--stamp_type参数控制



# 推理

## 批量运行

bash valid.sh (valid.sh会不断循环run_valid.sh)

除了上述训练中所用到的参数，还会引入一个参数，ckpt_idx来遍历每组参数的所有ckpoint。

test性能结果保存在../DRLTE/log/validRes/， 由run_test.sh的--stamp_type参数控制.

另外，test_epoch=1, test_episode=500 用来控制总的推理test的步数。


# input 文件介绍

输入文件都在DRLTE/inputs/中

* 文件一： 
  \${topoName}\_pf\_trueTM\_train4000.txt: 记录用线性规划求解得到的最优解（最大链路利用率）。 此值被用作计算reward的分母。 topoName指示拓扑名字，存储在当前topoName下，
  该文件需要在运行脚本中指定: lpPerformFile=../inputs/\${topoName}\_pf\_train4000.txt

* 文件二：
  \${topoName}\_train4000，记录候选路径和流量矩阵。 其中topoName指示拓扑名字，存储在当前topoName下，
  该文件也需要在运行脚本中指定:
  file_name=\${topoName}\_train4000

* 文件三： 拓扑文件 
  需要在运行脚本中指定：topoName=GEA


  
