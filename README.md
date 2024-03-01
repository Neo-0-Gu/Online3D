# Memory-based Adapters for Online 3D Scene Perception

## Introduction

This repo contains PyTorch implementation for paper [Memory-based Adapters for Online 3D Scene Perception] based on [MMDetection3D](https://github.com/open-mmlab/mmdetection3d).

> Memory-based Adapters for Online 3D Scene Perception
> [Xiuwei Xu](https://xuxw98.github.io/), Chong Xia, [Ziwei Wang](https://ziweiwangthu.github.io/), Linqing Zhao, Yueqi Duan,[Jie Zhou](https://scholar.google.com/citations?user=6a79aPwAAAAJ&hl=en&authuser=1), [Jiwen Lu](http://ivg.au.tsinghua.edu.cn/Jiwen_Lu/)
>

![teaser](./images/teaser2.png)

## News
- [2023/3/x]: Code release.
- [2023/2/27]: Our paper is accepted by CVPR 2024.

## Method
Overall pipeline of our work:

![overview](./images/over-arch.png)


## Getting Started
For data preparation and environment setup:
- [Installation](docs/install.md) 
- [Prepare Dataset](docs/data.md)

For training and evaluation:
- [Train and Eval](docs/run.md)


## Main Results
We provide the checkpoints for quick reproduction of the results reported in the paper. 

3D semantic segmentation results on ScanNet and SceneNN datasets are as follows:

 Method | Type | Dataset | mIou | mAcc | Downloads 
 | :--------------: | :----: | :----: | :----: |:----: |:----: |
 MkNet | Offline | ScanNet |71.6 | 80.4 | -
 MkNet-SV | Online | ScanNet |68.8 | 77.7 | [model](https://cloud.tsinghua.edu.cn/f/e80eeea97e684a75af05/?dl=1)
 MkNet-SV + Ours | Online | ScanNet |72.7 | 84.1 | [model](https://cloud.tsinghua.edu.cn/f/e271e43d2a934a4da490/?dl=1)
 MkNet-SV | Online | SceneNN |48.4 | 61.2 | [model](https://cloud.tsinghua.edu.cn/f/e80eeea97e684a75af05/?dl=1)
 MkNet-SV + Ours | Online | SceneNN |56.7 | 70.1 | [model](https://cloud.tsinghua.edu.cn/f/e271e43d2a934a4da490/?dl=1)

3D object detection results on ScanNet dataset are as follows:
 Method | Type |  mAP@25 | mAP@50 | Downloads 
 | :--------------: |  :----: | :----: |:----: |:----: |
 FCAF3D | Offline | 70.7 | 56.0 | -
 FCAF3D-SV | Online | 41.9 | 20.6 | [model](https://cloud.tsinghua.edu.cn/f/ff974cb9c4764b19bda6/?dl=1)
 FCAF3D-SV + Ours | Online |70.5 | 49.9 | [model](https://cloud.tsinghua.edu.cn/f/8c9647fad3bd4ee99bcc/?dl=1)

 3D instance segmentation results on ScanNet dataset are as follows:
 Method | Type |  mAP@25 | mAP@50 | Downloads 
 | :--------------: | :----: | :----: |:----: |:----: |
 TD3D | Offline |81.3 | 71.1 | -
 TD3D-SV | Online|53.7 | 36.8 | [model](https://cloud.tsinghua.edu.cn/f/0666d3cf263941d8b3e5/?dl=1)
 TD3D-SV + Ours | Online | 71.3 | 60.5 | [model](https://cloud.tsinghua.edu.cn/f/d95e96f55c93494ea14b/?dl=1)


 Here is the performance of different 3D scene perception methods on ScanNet online benchmark. We report mIoU / mAcc, mAP@25 /
mAP@50 and mAP@25 / mAP@50 for semantic segmentation, object detection and instance segmentation respectively.
And NS means the number of sequence, while LS means the length of Sequence.

 Task | Method | Type | NS 1 | NS 5 | NS 10| LS 5 | LS 10 | LS 15 
 | :----: | :----: | :----: | :----: |:----: |:----: |:----: |:----: |:----: |
 Semseg | MkNet | Offline | 63.7/73.5 | 62.7/72.8 | 58.9/69.4|59.3/69.8|63.0/73.0|63.5/73.7
 Semseg | MkNet-SV | Online | 63.3/74.3 | 63.3/74.3 | 63.3/74.3 |63.3/74.3 |63.3/74.3 |63.3/74.3 
  Semseg | MkNet-SV + Ours | Online | 69.1/82.2 | 66.8/80.0 | 65.9/79.2|65.9/79.3|66.8/80.1|67.1/80.4
 Detection | FCAF3D | Offline | 57.0/40.6 | 41.1/25.2 | 34.6/19.3|28.4/15.2|33.9/19.4|37.7/22.8
 Detection | FCAF3D-SV | Online | 41.9/20.6 | 29.8/13.3 | 27.0/11.5|24.4/10.1|26.2/11.0|27.6/12.1
 Detection | FCAF3D-SV + Ours | Online | 70.5/49.9 | 58.7/37.7 | 56.2/34.3|53.1/31.2|54.9/33.8|56.1/35.6
 Insseg | TD3D | Offline | 64.0/50.8 | 61.6/49.7 | 59.4/48.4|59.0/47.9|61.4/49.8|61.7/49.8
 Insseg | TD3D-SV | Online | 53.7/36.8 | 54.2/41.6 | 57.0/46.3|56.4/45.5|53.9/40.9|52.6/39.5
 Insseg | TD3D-SV + Ours  | Online | 71.3/60.5 | 64.7/55.2 | 64.2/55.0|64.0/54.7|64.6/55.1|63.9/54.3






 


Visualization results on ScanNet:

![vis](./images/vis.png)


## Acknowledgement
We thank a lot for the flexible codebase of [FCAF3D](https://github.com/SamsungLabs/fcaf3d) and valuable datasets provided by [ScanNet](https://github.com/ScanNet/ScanNet) and [SceneNN](https://github.com/hkust-vgd/scenenn).


## Bibtex
If this work is helpful for your research, please consider citing the following BibTeX entry.

```
@article{xu2023dsp, 
      title={DSPDet3D: Dynamic Spatial Pruning for 3D Small Object Detection}, 
      author={Xiuwei Xu and Zhihao Sun and Ziwei Wang and Hongmin Liu and Jie Zhou and Jiwen Lu},
      journal={arXiv preprint arXiv:2305.03716},
      year={2023}
}
```
