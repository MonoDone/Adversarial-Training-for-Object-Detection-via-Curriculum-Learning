_base_ = '../configs/fcos/fcos_r50_caffe_fpn_gn-head_1x_coco.py'


checkpoint_at = "/root/anaconda3/oddefense/ckpts/resnet50_linf_eps4_pure.pth"
model = dict(
    backbone=dict(
        norm_cfg=dict(type='BN', requires_grad=False),
        style='pytorch',
        init_cfg=dict(
            type='Pretrained',
            checkpoint=checkpoint_at)),
    bbox_head=dict(
        num_classes=20,
        norm_on_bbox=True,
        centerness_on_reg=True,
        dcn_on_last_conv=False,
        center_sampling=True,
        conv_bias=True,
        loss_bbox=dict(type='GIoULoss', loss_weight=1.0)),
    # training and testing settings
    test_cfg=dict(nms=dict(type='nms', iou_threshold=0.6)),
    train_cfg=dict(clip=6))

dataset_type = 'VOCDataset'
data_root = '/root/anaconda3/oddefense/datasets/voc/VOCdevkit/'
work_dir = "/root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models/fcos_r50_baseline"

# adversarial trainging and eval config
free_m = 4
times = 2


# full version

adv_cfg = dict(
    adv_flag=True,
    adv_type="all", # assert in ["all", "mtd", "cwa"]
    free_m=free_m,
    epsilon=8)


test_adv_cfg = dict(
    adv_flag=True,
    adv_type="cls", # assert in ["cls", "reg", "cwa"]
    step_size=2,
    epsilon=8,
    num_steps=10,
)

evaluation = dict(interval=1, metric='mAP', save_best='mAP')


img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(1000, 600), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(1000, 600), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]

lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=int(500/free_m),
    warmup_ratio=0.001,
    step=[times*8//free_m, times*10//free_m])
runner = dict(type='AdvEpochBasedRunner', max_epochs=times*12//free_m)

optimizer = dict(
    _delete_=True,
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.0001,
    paramwise_cfg=dict(
        custom_keys={'backbone': dict(lr_mult=0.1, decay_mult=1.0)}
    )
)

optimizer_config = dict(type='AdvOptimizerHook',
                    grad_clip=dict(max_norm=100, norm_type=2)) # ignore previous setting

data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type='RepeatDataset', times=3, dataset=dict(
            type=dataset_type,
            ann_file=[
                data_root + 'VOC2007/ImageSets/Main/trainval.txt',
                data_root + 'VOC2012/ImageSets/Main/trainval.txt'
            ],
            img_prefix=[data_root + 'VOC2007/', data_root + 'VOC2012/'],
            pipeline=train_pipeline)),
    val=dict(
        type=dataset_type,
        pipeline=test_pipeline,
        ann_file=data_root + 'VOC2007/ImageSets/Main/test.txt',
        img_prefix=data_root + 'VOC2007/',),
    test=dict(
        type=dataset_type,
        pipeline=test_pipeline,
        ann_file=data_root + 'VOC2007/ImageSets/Main/test.txt',
        img_prefix=data_root + 'VOC2007/',)
)

log_config = dict(
    interval=200,
    hooks=[
        dict(type='TextLoggerHook'),
        # dict(type='TensorboardLoggerHook')
    ])

auto_scale_lr = dict(enable=False, base_batch_size=16)