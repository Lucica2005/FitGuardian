from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord
from mxnet import gluon, nd
import numpy as np

im_fname = "C:\\Users\\xusir\\Desktop\\college\\github\\Ultralight-SimplePose\\Ultralight-SimplePose\\data\\14.jpg"
model_json = 'C:\\Users\\xusir\\Desktop\\college\\github\\Ultralight-SimplePose\\Ultralight-SimplePose\\model\\Ultralight-Nano-SimplePose.json'
model_params = "C:\\Users\\xusir\\Desktop\\college\\github\\Ultralight-SimplePose\\Ultralight-SimplePose\\model\\Ultralight-Nano-SimplePose.params"

detector = model_zoo.get_model('yolo3_mobilenet1.0_coco', pretrained=True)
pose_net = gluon.SymbolBlock.imports(model_json,['data'],model_params)

detector.reset_class(["person"], reuse_weights=['person'])
x, img = data.transforms.presets.ssd.load_test(im_fname, short=512)
print('Shape of pre-processed image:', x.shape)
class_IDs, scores, bounding_boxs = detector(x)
pose_input, upscale_bbox = detector_to_simple_pose(img, class_IDs, scores, bounding_boxs)
predicted_heatmap = pose_net(pose_input)
pred_coords, confidence = heatmap_to_coord(predicted_heatmap, upscale_bbox)
ax = utils.viz.plot_keypoints(img, pred_coords, confidence,
                              class_IDs, bounding_boxs, scores,
                              box_thresh=0.5, keypoint_thresh=0.2)
plt.show()
