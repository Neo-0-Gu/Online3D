import MinkowskiEngine as ME

from mmdet.models import DETECTORS
from mmdet3d.models import build_backbone, build_head
from mmdet3d.core import bbox3d2result
from .base import Base3DDetector
import numpy as np
import pdb
import torch


@DETECTORS.register_module()
class SingleStageSparse3DDetector(Base3DDetector):
    def __init__(self,
                backbone,
                neck_with_head,
                voxel_size,
                pretrained=False,
                evaluator_mode=None,
                num_slice=None,
                len_slice=None,
                train_cfg=None,
                test_cfg=None):
        super(SingleStageSparse3DDetector, self).__init__()
        self.backbone = build_backbone(backbone)
        neck_with_head.update(train_cfg=train_cfg)
        neck_with_head.update(test_cfg=test_cfg)
        self.neck_with_head = build_head(neck_with_head)
        self.voxel_size = voxel_size
        self.train_cfg = train_cfg
        self.test_cfg = test_cfg
        self.evaluator_mode=evaluator_mode
        self.num_slice=num_slice
        self.len_slice=len_slice
        self.init_weights()

    def init_weights(self, pretrained=None):
        self.backbone.init_weights()
        self.neck_with_head.init_weights()

    def extract_feat(self, points, img_metas):
        """Extract features from points."""
        coordinates, features = ME.utils.batch_sparse_collate(
            [(p[:, :3] / self.voxel_size, p[:, 3:] / 255.) for p in points],
            device=points[0].device)
        x = ME.SparseTensor(coordinates=coordinates, features=features)
        x = self.backbone(x)
        x = self.neck_with_head(x)
        return x


    def view_model_param(self):
        total_param = 0
        print("MODEL DETAILS:\n")
        #print(model)
        for param in self.parameters():
            # print(param.data.size())
            total_param += np.prod(list(param.data.size()))
        print('MODEL/Total parameters:', total_param)
        
        # 假设每个参数是一个 32 位浮点数（4 字节）
        bytes_per_param = 4
        
        # 计算总字节数
        total_bytes = total_param * bytes_per_param
        
        # 转换为兆字节（MB）和千字节（KB）
        total_megabytes = total_bytes / (1024 * 1024)
        total_kilobytes = total_bytes / 1024

        print("Total parameters in MB:", total_megabytes)
        print("Total parameters in KB:", total_kilobytes)

        return total_param



    def forward_train(self,
                      points,
                      gt_bboxes_3d,
                      gt_labels_3d,
                      img_metas):
        x = self.extract_feat(points, img_metas)
        losses = self.neck_with_head.loss(*x, gt_bboxes_3d, gt_labels_3d, img_metas)
        return losses

    def simple_test(self, points, img_metas, imgs=None, rescale=False):
        """Test function without augmentaiton."""
        # self.view_model_param()

        timestamps = []
        if self.evaluator_mode == 'slice_len_constant':
            i=1
            while i*self.len_slice<len(points[0]):
                timestamps.append(i*self.len_slice)
                i=i+1
            timestamps.append(len(points[0]))
        else:
            num_slice = min(len(points[0]),self.num_slice)
            for i in range(1,num_slice):
                timestamps.append(i*(len(points[0])//num_slice))
            timestamps.append(len(points[0]))

        # Process
        bbox_results = [[]]
        depth2img = img_metas[0]['depth2img']

        for i in range(len(timestamps)):
            if i == 0:
                ts_start, ts_end = 0, timestamps[i]
            else:
                ts_start, ts_end = timestamps[i-1], timestamps[i]
                

            points_new = [points[0][ts_start:ts_end,:,:].reshape(-1,points[0].shape[-1])]
            x = self.extract_feat(points_new, img_metas)
            bbox_list = self.neck_with_head.get_bboxes(*x, img_metas, rescale=rescale)
            bboxes, scores, labels = bbox_list[0]
            for j in range(ts_start, ts_end):
                bbox_results[0].append(bbox3d2result(bboxes, scores, labels))
                
        return bbox_results

    def aug_test(self, points, img_metas, imgs=None, rescale=False):
        pass