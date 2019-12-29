import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import json
import os
np.set_printoptions(threshold=np.inf)

# 用于记录label的连通性
label_dict = [int(i) for i in np.zeros(600)]


def find(label) -> int:
    global label_dict
    while 0 != label_dict[label]:
        label = label_dict[label]
    return label


def union(root, slave) -> None:
    global label_dict
    root_label = find(root)
    slave_label = find(slave)
    if slave_label != root_label:
        label_dict[slave_label] = root_label


def bwlabel(binary_image):
    global label_dict
    pading_image = np.pad(binary_image, ((1, 0), (1, 0)), 'constant', constant_values=(0, 0))
    w = np.size(binary_image, 0)
    h = np.size(binary_image, 1)
    label = 1
    #  first pass
    for cow in range(1, h + 1):
        for col in range(1, w + 1):
            if pading_image[cow][col] != 0:
                left_pixel = pading_image[cow][col - 1]
                up_pixel = pading_image[cow - 1][col]

                if left_pixel == 0 and up_pixel == 0:
                    pading_image[cow][col] = label
                    label += 1

                if left_pixel != 0 and up_pixel != 0:
                    smaller = left_pixel if left_pixel < up_pixel else up_pixel
                    bigger = left_pixel if left_pixel > up_pixel else up_pixel
                    pading_image[cow][col] = smaller
                    union(smaller, bigger)

                if up_pixel != 0 and left_pixel == 0:
                    pading_image[cow][col] = up_pixel

                if up_pixel == 0 and left_pixel != 0:
                    pading_image[cow][col] = left_pixel

    # second pass
    for cow in range(1, h + 1):
        for col in range(1, w + 1):
            root = find(pading_image[cow][col])
            pading_image[cow][col] = root

    output = pading_image[1:, 1:]
    return output


# 存储目录
path = "D:/SCNU/list2017/"
# 寻找标注文件
for i in range(0, 1):
    # nii_filename = "segmentation-0.nii"
    nii_filename = os.path.join(path, "segmentation-%d.nii" % i)
    # nii元文件
    nii_img = nib.load(nii_filename)
    # nii元文件长、宽、厚度
    width, height, queue = nii_img.dataobj.shape
    # nii数组
    nii_data = nii_img.get_data()
    nii_data = nii_data.astype(np.int16)
    # 复制nii数组
    # new_data = nii_data.copy()
    # 复制nii元信息
    # affine = nii_img.affine.copy()
    # hdr = nii_img.header.copy()
    # json字典
    rec_json = {'liver': {}, 'tumour': {}}
    # 遍历nii每层
    for j in range(0, queue):
        # 寻找有标注的层
        if (nii_data[:, :, j] > 0).any():
            # 挑出肝脏，去除肿瘤标记
            new_liver_data = nii_data[:, :, j].copy()
            new_liver_data[new_liver_data == 2] = 0

            # 挑出肿瘤，去除肝脏标记
            new_tumour_data = nii_data[:, :, j].copy()
            new_tumour_data[new_tumour_data == 1] = 0
            # label_dict = [int(i) for i in np.zeros(600)]
            # 标记肝脏连通域
            # link_liver = bwlabel(new_liver_data)
            # 肝脏连通域个数
            # max_label = np.max(label_dict)
            # 层json字典
            layer_json = {j: {}}
            # 遍历肝脏连通域
            # rec_number = 0
            # for k in range(1, max_label + 1):
                # 肝脏连通域索引条件
                # label_liver = link_liver[:, :] == k
                # 某个肝脏连通域的行列二维索引数组
                # label_liver_arr = np.nonzero(label_liver)
                # 部分层不存在标注
                # if label_liver_arr[0].size > 0:
                #     rec_number = rec_number + 1
                    # 寻找肝脏连通域边界框
                    # y_min = np.min(label_liver_arr[0])
                    # y_max = np.max(label_liver_arr[0])
                    # x_min = np.min(label_liver_arr[1])
                    # x_max = np.max(label_liver_arr[1])
                    # 填充肝脏连通域
                    # new_data[x_min:x_max + 1, y_min:y_max + 1, j] = 1
                    # 生成json数据
            label_liver_arr = np.nonzero(new_liver_data)
            y_min = np.min(label_liver_arr[0])
            y_max = np.max(label_liver_arr[0])
            x_min = np.min(label_liver_arr[1])
            x_max = np.max(label_liver_arr[1])
            layer_json[j].update({1: [int(x_min), int(x_max), int(y_min), int(y_max)]})
            if layer_json[j]:
                rec_json['liver'].update(layer_json)
            label_dict = [int(i) for i in np.zeros(600)]
            # 标记肿瘤连通域
            link_tumour = bwlabel(new_tumour_data)
            # 肿瘤连通域个数
            max_label = np.max(label_dict)
            # 遍历肿瘤连通域
            layer_json = {j: {}}
            rec_number = 0
            for k in range(1, max_label + 1):
                # 肿瘤连通域索引条件
                label_tumour = link_tumour[:, :] == k
                # 某个肿瘤连通域的行列二维索引数组
                label_tumour_arr = np.nonzero(label_tumour)
                # 部分层只存在肝脏标注而不存在肿瘤标注
                if label_tumour_arr[0].size > 0:
                    rec_number = rec_number + 1
                    # 寻找肿瘤连通域边界框
                    y_min = np.min(label_tumour_arr[0])
                    y_max = np.max(label_tumour_arr[0])
                    x_min = np.min(label_tumour_arr[1])
                    x_max = np.max(label_tumour_arr[1])
                    # 填充肿瘤连通域
                    # new_data[x_min:x_max + 1, y_min:y_max + 1, j] = 2
                    # 生成json数据
                    layer_json[j].update({rec_number: [int(x_min), int(x_max), int(y_min), int(y_max)]})
            if layer_json[j]:
                rec_json['tumour'].update(layer_json)
    # 生成nii元文件
    # new_nii = nib.Nifti1Image(new_data, affine, hdr)
    # 保存路径
    path_save = os.path.join("D:/SCNU/list2017/", "rec-segmentation-%d.json" % i)
    # 保存
    # nib.save(new_nii, path_save)
    print(rec_json)
    with open(path_save, "w") as f:
        json.dump(rec_json, f)
    print("转换完%d个" % i)