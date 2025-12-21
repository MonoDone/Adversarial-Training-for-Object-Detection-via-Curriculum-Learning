#  adapted from https://github.com/LYMDLUT/DN-DETR-mmdetection
_base_ = [
    '../configs/_base_/datasets/coco_detection.py', '../configs/_base_/default_runtime.py'
]
checkpoint_at = "/root/anaconda3/oddefense/ckpts/convnext_tiny_mmcls-linf-eps-4-advan.pth"
custom_imports = dict(imports=['mmcls.models'], allow_failed_imports=False)


model = dict(
    type='DABDETR',
    backbone=dict(
        type='mmcls.ConvNeXt',
        arch='tiny',
        out_indices=[3],
        drop_path_rate=0.0,
        frozen_stages=1,
        # norm_cfg=dict(type='LN2d', requires_grad=False),
        layer_scale_init_value=1.0,
        gap_before_final_norm=False,
        linear_pw_conv=True,
        init_cfg=dict(
            type='Pretrained', checkpoint=checkpoint_at)),
    bbox_head=dict(
        type='DNDETRHead',
        num_query=300,
        query_dim=4,
        random_refpoints_xy=False,
        bbox_embed_diff_each_layer=False,
        num_classes=20,
        in_channels=768,
        transformer=dict(
            type='DNTransformer',
            d_model=256,
            num_patterns=0,
            num_queries=300,
            encoder=dict(
                type='DABDetrTransformerEncoder',
                num_layers=6,
                d_model=256,
                transformerlayers=dict(
                    type='BaseTransformerLayer',
                    ffn_cfgs=dict(
                        type='FFN',
                        embed_dims=256,
                        feedforward_channels=2048,
                        num_fcs=2,
                        ffn_drop=0.0,
                        act_cfg=dict(type='ReLU'),
                    ),
                    attn_cfgs=[
                        dict(
                            type='MultiheadAttention',
                            embed_dims=256,
                            num_heads=8,
                            dropout=0.0)
                    ],
                    feedforward_channels=2048,
                    ffn_dropout=0.0,
                    operation_order=('self_attn', 'norm', 'ffn', 'norm'))),
            decoder=dict(
                type='DABDetrTransformerDecoder',
                return_intermediate=True,
                num_layers=6,
                d_model=256,
                query_dim=4,
                iter_update=True,
                keep_query_pos=False,
                query_scale_type='cond_elewise',
                modulate_hw_attn=True,
                bbox_embed_diff_each_layer=False,
                transformerlayers=dict(
                    type='DABDetrTransformerDecoderLayer',
                    ffn_cfgs=dict(
                        type='FFN',
                        embed_dims=256,
                        feedforward_channels=2048,
                        num_fcs=2,
                        ffn_drop=0.0,
                        act_cfg=dict(type='ReLU'),
                    ),
                    attn_cfgs=[
                        dict(
                        type='DFMultiheadAttention',
                        embed_dims=256,
                        num_heads=8,
                        dropout=0.0),
                        dict(
                        type='DPMultiheadAttention',
                        embed_dims=256,
                        num_heads=8,
                        dropout=0.0)],
                    feedforward_channels=2048,
                    ffn_dropout=0.0,
                    operation_order=('self_attn', 'norm', 'cross_attn', 'norm',
                                     'ffn', 'norm')),
            )),
        positional_encoding=dict(
            type='SinePositionalEncodingHW', temperatureH=10, temperatureW=10, num_feats=128, normalize=True),
        loss_cls=dict(
            type='FocalLoss',
            use_sigmoid=True,
            gamma=2.0,
            alpha=0.25,
            loss_weight=1.0),
        loss_bbox=dict(type='L1Loss', loss_weight=5.0),
        loss_iou=dict(type='GIoULoss', loss_weight=2.0)),
    # training and testing settings
    train_cfg=dict(
        assigner=dict(
            type='HungarianAssigner',
            cls_cost=dict(type='FocalLossCost', weight=2.0),
            reg_cost=dict(type='BBoxL1Cost', weight=5.0, box_format='xywh'),
            iou_cost=dict(type='IoUCost', iou_mode='giou', weight=2.0))),
    test_cfg=dict(max_per_img=300))

dataset_type = 'VOCDataset'
data_root = '/root/anaconda3/oddefense/datasets/voc/VOCdevkit/'
work_dir = "/root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models/dndetr_xt_processing"

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