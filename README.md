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

> Note: Please prepare the required pretrained backbone / detector weights and dataset paths as needed, and make sure the configs or scripts point to the correct locations.

<h3>Train and Evaluate</h3>

#### 1) Training

```bash
bash run_baseline.sh # train baseline
bash run_processing.sh # train ours
```

#### 2) Evaluation

```bash
bash test_baseline.sh # evaluate baseline on clean samples
bash test_processing.sh # evaluate ours on clean samples
bash test_pure_baseline.sh # evaluate baseline under white-box setting
bash test_pure_processing.sh # evaluate ours under white-box setting
```

<h2 id="weights">Weights</h2>

The following table provides weights for different architectures (Processing/Ours):

| **File**                  | **Link**                                                                                                             |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| dndetr_r50_processing.pth | [https://pan.baidu.com/s/1KSvhnZi5vBAtArGKZG8yVg?pwd=mono](https://pan.baidu.com/s/1KSvhnZi5vBAtArGKZG8yVg?pwd=mono) |
| dndetr_xt_processing.pth  | [https://pan.baidu.com/s/1loF2patFlFa3yv9G6LnzTg?pwd=mono](https://pan.baidu.com/s/1loF2patFlFa3yv9G6LnzTg?pwd=mono) |
| frcnn_r50_processing.pth  | [https://pan.baidu.com/s/16sd36NU4s2J-q8z2Ll1Qgw?pwd=mono](https://pan.baidu.com/s/16sd36NU4s2J-q8z2Ll1Qgw?pwd=mono) |
| frcnn_xt_processing.pth   | [https://pan.baidu.com/s/1GhGN2FrfxwremHRJdcwNXA?pwd=mono](https://pan.baidu.com/s/1GhGN2FrfxwremHRJdcwNXA?pwd=mono) |
| fcos_r50_processing.pth   | [https://pan.baidu.com/s/1-gwIxvq7rnjtXxPlh37QNg?pwd=mono](https://pan.baidu.com/s/1-gwIxvq7rnjtXxPlh37QNg?pwd=mono) |
| fcos_xt_processing.pth    | [https://pan.baidu.com/s/1NY96g-TY_hQVYqm9wjOZMA?pwd=mono](https://pan.baidu.com/s/1NY96g-TY_hQVYqm9wjOZMA?pwd=mono) |

<h3>Acknowledgement</h3>

Acknowledgement: This project is adapted from the open-source repository [https://github.com/thu-ml/oddefense](https://github.com/thu-ml/oddefense) .

```
```
