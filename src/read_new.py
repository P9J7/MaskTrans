import nibabel as nib
import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)

# volume-0.nii  segmentation-0.nii new_test.nii
nii_filename = "segmentation-84.nii"
# nii元文件
nii_img = nib.load(nii_filename)
# nii元文件长、宽、厚度
width, height, queue = nii_img.dataobj.shape
print(queue)
# nii数组
nii_data = nii_img.get_fdata()
# 遍历nii每层
 # 绘制图片
plt.imshow(nii_data[:, :, 507], cmap="gray")
plt.show()
# print(nii_data[:, :, 153])

            # # 肝脏标注的行列索引二维数组
            # label_liver = nii_data[:, :, j] == 1
            # label_liver_arr = np.nonzero(nii_data[:, :, j])
            # # 肿瘤标注的行列索引二维数组
            # label_tumour = nii_data[:, :, j] == 2
            # label_tumour_arr = np.nonzero(label_tumour)
            # # 寻找肝脏边界框
            # x_min = np.min(label_liver_arr[0])
            # x_max = np.max(label_liver_arr[0])
            # y_min = np.min(label_liver_arr[1])
            # y_max = np.max(label_liver_arr[1])
            # # 填充肝脏边界框
            # new_data[x_min:x_max + 1, y_min:y_max + 1, j] = 1
            # # 部分层只存在肝脏标注而不存在肿瘤标注
            # if label_tumour_arr[0].size > 0:
            #     # 寻找肿瘤边界框
            #     x_min = np.min(label_tumour_arr[0])
            #     x_max = np.max(label_tumour_arr[0])
            #     y_min = np.min(label_tumour_arr[1])
            #     y_max = np.max(label_tumour_arr[1])
            #     # 填充肿瘤边界框
            #     new_data[x_min:x_max + 1, y_min:y_max + 1, j] = 2