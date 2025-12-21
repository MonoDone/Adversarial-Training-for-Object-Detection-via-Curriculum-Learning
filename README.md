<div align="center">
  <h3></h3>
</div>

<h2 id="quick-start">Quick Start</h2>

<h3>Preparation</h3>

```sh
conda create -n oddefense python=3.10
conda activate oddefense

conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia

pip install -U openmim
mim install mmcv-full==1.7.0
pip install mmdet==2.28.0
pip install -r requirements.txt
````

> 说明：请按需准备对应 backbone / detector 的预训练权重与数据集路径，并在配置或脚本中正确指向。

<h3>Train and Evaluate</h3>

#### 1) Training

```bash
bash run_baseline.sh # 训练baseline
bash run_processing.sh # 训练ours
```

#### 2) Evaluation

```bash
bash test_baseline.sh # 测试baseline干净样本性能
bash test_processing.sh # 测试ours干净样本性能
bash test_pure_baseline.sh # 测试baseline白盒性能 
bash test_pure_processing.sh # 测试ours白盒性能
```

<h2 id="weights">Weights</h2>

下表提供不同架构对应的权重文件（Processing/Ours）：

| **File**                  | **Link**                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| dndetr_r50_processing.pth | [https://pan.baidu.com/s/1KSvhnZi5vBAtArGKZG8yVg?pwd=mono](https://pan.baidu.com/s/1KSvhnZi5vBAtArGKZG8yVg?pwd=mono) |
| dndetr_xt_processing.pth  | [https://pan.baidu.com/s/1loF2patFlFa3yv9G6LnzTg?pwd=mono](https://pan.baidu.com/s/1loF2patFlFa3yv9G6LnzTg?pwd=mono) |
| frcnn_r50_processing.pth  | [https://pan.baidu.com/s/16sd36NU4s2J-q8z2Ll1Qgw?pwd=mono](https://pan.baidu.com/s/16sd36NU4s2J-q8z2Ll1Qgw?pwd=mono) |
| frcnn_xt_processing.pth   | [https://pan.baidu.com/s/1GhGN2FrfxwremHRJdcwNXA?pwd=mono](https://pan.baidu.com/s/1GhGN2FrfxwremHRJdcwNXA?pwd=mono) |
| fcos_r50_processing.pth   | [https://pan.baidu.com/s/1-gwIxvq7rnjtXxPlh37QNg?pwd=mono](https://pan.baidu.com/s/1-gwIxvq7rnjtXxPlh37QNg?pwd=mono) |
| fcos_xt_processing.pth    | [https://pan.baidu.com/s/1NY96g-TY_hQVYqm9wjOZMA?pwd=mono](https://pan.baidu.com/s/1NY96g-TY_hQVYqm9wjOZMA?pwd=mono) |

<h3>Acknowledgement</h3>

致谢：本项目参考并改造自开源仓库 [https://github.com/thu-ml/oddefense](https://github.com/thu-ml/oddefense) 。


