_base_ = ['../_base_/default_runtime.py']

dataset_type = 'ScanNetMVDataset'
data_root = './data/scannet-mv/'
class_names = ('cabinet', 'bed', 'chair', 'sofa', 'table', 'door', 'window',
               'bookshelf', 'picture', 'counter', 'desk', 'curtain',
               'refrigerator', 'showercurtrain', 'toilet', 'sink', 'bathtub',
               'garbagebin')
img_norm_cfg = dict(
    mean=[103.530, 116.280, 123.675], std=[1.0, 1.0, 1.0], to_rgb=False)

load_from = "work_dirs/fcaf3d_svFF/latest.pth"

evaluator_mode = 'slice_num_constant'
num_slice = 1
len_slice = 5

model = dict(
    evaluator_mode=evaluator_mode,
    num_slice=num_slice,
    len_slice=len_slice)

model = dict(
    type='Model3DETR_SepView',
    evaluator_mode=evaluator_mode,
    num_slice=num_slice,
    len_slice=len_slice,
    train_cfg=dict(),
    test_cfg=dict(nms_pre=300, nms_pre_merge=1000, iou_thr=.5, iou_thr_merge=.5, score_thr=.02))


train_pipeline = [
    dict(
        type='LoadAdjacentViewsFromFiles',
        coord_type='DEPTH',
        num_frames=8,
        shift_height=False,
        use_color=True,
        use_dim=[0, 1, 2, 3, 4, 5],
        ),
    dict(type='LoadAnnotations3D'),
    dict(
        type='MultiImgsAug',
        img_scales=[(1333, 480), (1333, 504), (1333, 528), (1333, 552),
                   (1333, 576), (1333, 600)],
        #img_scales=[(1333, 640), (1333, 672), (1333, 704), (1333, 736),
        #           (1333, 768), (1333, 800)],
        #img_scales=(300, 400),
        transforms=[
            dict(
                type='Resize',
                multiscale_mode='value',
                keep_ratio=True),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32)
        ]
        ),
    dict(
        type='RandomFlip3D',
        sync_2d=False,
        flip_ratio_bev_horizontal=0.5,
        flip_ratio_bev_vertical=0.5),
    dict(
        type='GlobalRotScaleTrans',
        rot_range=[-0.02, 0.02],
        scale_ratio_range=[.9, 1.1],
        translation_std=[.1, .1, .1],
        shift_height=False),
    dict(type='NormalizePointsColor', color_mean=None),
    dict(type='MultiViewFormatBundle3D', class_names=class_names),
    dict(type='Collect3D', keys=['points', 'modal_box','modal_label', 'amodal_box_mask', 
                                'gt_bboxes_3d', 'gt_labels_3d', 'img'])
    # dict(type='Collect3D', keys=['points', 'gt_bboxes_3d', 'gt_labels_3d', 'img'])
]
# need to confirm parameters
test_pipeline = [
    dict(
        type='LoadAdjacentViewsFromFiles',
        coord_type='DEPTH',
        num_frames=-1,
        shift_height=False,
        use_color=True,
        use_dim=[0, 1, 2, 3, 4, 5],
        ),
    dict(
        type='MultiScaleFlipAug3D',
        img_scale=(1333, 600),
        pts_scale_ratio=1,
        flip=False,
        transforms=[
            dict(type='NormalizePointsColor', color_mean=None),
            dict(
                type='MultiViewFormatBundle3D',
                class_names=class_names,
                with_label=False),
            dict(type='Collect3D', keys=['points'])
        ])
]




data = dict(
    samples_per_gpu=4,
    workers_per_gpu=4,
    train=dict(
        type='RepeatDataset',
        times=10,
        dataset=dict(
            type=dataset_type,
            data_root=data_root,
            ann_file=data_root + 'scannet_mv_infos_train.pkl',
            pipeline=train_pipeline,
            filter_empty_gt=True,
            classes=class_names,
            box_type_3d='Depth')),
    val=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file=data_root + 'scannet_mv_infos_val.pkl',
        pipeline=test_pipeline,
        classes=class_names,
        test_mode=True,
        box_type_3d='Depth',
        evaluator_mode=evaluator_mode,
        num_slice=num_slice,
        len_slice=len_slice),
    test=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file=data_root + 'scannet_mv_infos_val.pkl',
        pipeline=test_pipeline,
        classes=class_names,
        test_mode=True,
        box_type_3d='Depth',
        evaluator_mode=evaluator_mode,
        num_slice=num_slice,
        len_slice=len_slice))

optimizer = dict(type='AdamW', lr=0.001, weight_decay=0.0001)
optimizer_config = dict(grad_clip=dict(max_norm=10, norm_type=2))
lr_config = dict(policy='step', warmup=None, step=[8, 11])
runner = dict(type='EpochBasedRunner', max_epochs=12)
custom_hooks = [dict(type='EmptyCacheHook', after_iter=True)]
