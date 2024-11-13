# segments是分割的坐标点
segments = [
    scale_segments(im0.shape if retina_masks else im.shape[2:], x, im0.shape, normalize=True)
    for x in reversed(masks2segments(masks))]
new_segments = []  # 用来装反归一化后的坐标
image_list = []  # 切割的小图
im0_h, im0_w, im0_c = im0.shape
for k, seg_list in enumerate(segments):
    # 将归一化的点转换为坐标点
    new_seg_list = []
    for s_point in seg_list:
        pt1, pt2 = s_point
        new_pt1 = int(pt1 * im0_w)
        new_pt2 = int(pt2 * im0_h)
        new_seg_list.append([new_pt1, new_pt2])
    rect = cv2.minAreaRect(np.array(new_seg_list))  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    seg_bbox = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
    seg_bbox = np.int0(seg_bbox)
    if np.linalg.norm(seg_bbox[0] - seg_bbox[1]) < 5 or np.linalg.norm(seg_bbox[3] - seg_bbox[0]) < 5:
        continue

    # 坐标点排序
    box1 = sorted(seg_bbox, key=lambda x: (x[1], x[0]))
    # 将坐标点按照顺时针方向来排序，box的从左往右从上到下排序
    if box1[0][0] > box1[1][0]:
        box1[0], box1[1] = box1[1], box1[0]
    if box1[2][0] < box1[3][0]:
        box1[2], box1[3] = box1[3], box1[2]
    if box1[0][1] > box1[1][1]:
        box1[0], box1[1], box1[2], box1[3] = box1[1], box1[2], box1[3], box1[0]
    box1_list = [b.tolist() for b in box1]  # 坐标转换为list格式
    new_segments.append(box1_list)
    tmp_box = copy.deepcopy(np.array(box1)).astype(np.float32)
    partImg_array = image_crop_tools.get_rotate_crop_image(im0, tmp_box)
    image_list.append(partImg_array)
    # cv2.imwrite(str(k)+'.jpg', partImg_array)  # 保存小图

# 在原图上画出分割图像
# src_image = im0.copy()
# for ns_box in new_segments:
#     cv2.drawContours(src_image, [np.array(ns_box)], -1, (0, 255, 0), 2)
# cv2.imwrite('1.jpg', src_image)




