import numpy as np
import nibabel as nib
np.set_printoptions(threshold=np.inf)
# import matplotlib.pyplot as plt

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


if __name__ == '__main__':
    logic_image = np.array([
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0]
    ])
    # volume-0.nii  segmentation-0.nii new_test.nii
    # nii_filename = "segmentation-0.nii"
    # # nii元文件
    # nii_img = nib.load(nii_filename)
    # # nii元文件长、宽、厚度
    # width, height, queue = nii_img.dataobj.shape
    # # nii数组
    # nii_data = nii_img.get_data()
    label_image = bwlabel(logic_image)
    print(label_dict)
    print(label_image)
    logic_image = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0]
    ])
    label_image = bwlabel(logic_image)
    print(label_dict)
    print(label_image)
    # im = plt.imshow(label_image, cmap='Blues', interpolation='none', vmin=0, vmax=1, aspect='equal')
    # plt.show()