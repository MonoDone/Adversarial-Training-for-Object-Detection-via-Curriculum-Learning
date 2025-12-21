bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/frcnn_r50_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/frcnn_r50_processing/latest.pth 8 --eval mAP

bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/fcos_r50_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/fcos_r50_processing/latest.pth 8 --eval mAP

# bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/dndetr_r50_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/dndetr_r50_processing/latest.pth 8 --eval mAP

bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/frcnn_xt_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/frcnn_xt_processing/latest.pth 8 --eval mAP

bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/fcos_xt_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/fcos_xt_processing/latest.pth 8 --eval mAP

# bash tools/dist_test.sh /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/dndetr_xt_processing.py /root/anaconda3/raw2_oddefense/oddefense/pascal_voc/black_models_d3/dndetr_xt_processing/latest.pth 8 --eval mAP