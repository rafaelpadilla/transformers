# coding=utf-8
# Copyright 2023 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from transformers import is_torch_available, is_torchvision_available
from transformers.bounding_box_utils import transform_box_format, BoundingBoxFormat
from transformers.testing_utils import require_torch


if is_torch_available():
    import torch

if is_torchvision_available():
    # TODO: (Rafa) GOOD RESOURCE
    # Using torchvision as reference
    # >>> box_convert(boxes_xywh, in_fmt="xywh", out_fmt="xywh")
    from torchvision.ops.boxes import box_convert

_EPS = 1e-8


samples = {"xywh": [[387, 441,  44,  9], [134,  57, 434, 383], [306, 274,  36, 154], [ 22, 252, 479,  56], [498, 349, 120,  79]],
           "xyxy": [[387, 441, 431, 450.], [134,  57, 568, 440.], [306, 274, 342, 428.], [ 22, 252, 501, 308.], [498, 349, 618, 428]],
           "xcycwh": [[409., 445.5,  44., 9.], [351., 248.5, 434., 383.], [324., 351.,  36., 154.], [261.5, 280., 479.,  56.], [558., 388.5, 120., 79.]],
           "relative_xywh": [[0.6047, 0.9587, 0.0688 , 0.0196], [0.2094, 0.1239, 0.6781, 0.8326], [0.4781, 0.5957, 0.05625 , 0.3348], [0.0344, 0.5478, 0.7484, 0.1217],[0.7781, 0.7587, 0.1875, 0.1717]],
           "relative_xcycwh": [[0.6391,0.9685,0.0688,0.0196], [0.5484,0.5402,0.6781,0.8326], [0.5063,0.7630,0.0563,0.3348], [0.4086,0.6087,0.7484,0.1217], [0.8719,0.8446,0.1875,0.1717]]
           }
original_img_shape = [460, 640] 

rel_formats = ("relative_xywh", "relative_xcycwh")

for origin_format, bboxes in samples.items():
    origin_format = BoundingBoxFormat(origin_format)
    bboxes = torch.Tensor(bboxes)
    
    for dest_format, expected_bboxes in samples.items():
        dest_format = BoundingBoxFormat(dest_format)
        expected_bboxes = torch.Tensor(expected_bboxes)
        img_shape = None
        if dest_format in rel_formats or origin_format in rel_formats:
            img_shape = original_img_shape
        
        result = transform_box_format(bboxes, orig_format=origin_format, dest_format=dest_format, img_shape=img_shape)
        print(torch.allclose(result, expected_bboxes, atol=1e-4))
    
@require_torch
class UtilBoundingBoxConverters(unittest.TestCase):
    def generate_rand_xy(self, image_height, image_width, total_samples, init_val=0):
        # Random generated starting points (X, Y) for the bounding boxes
        x = torch.randint(init_val, image_width, (total_samples, 1))
        y = torch.randint(init_val, image_height, (total_samples, 1))
        return x, y

    def generate_rand_xywh(self, image_height, image_width, total_samples):
        # Get x and y
        x, y = self.generate_rand_xy(image_height, image_width, total_samples)
        # Random generated widths and heights for the bounding boxes
        w = torch.zeros(total_samples, 1, dtype=torch.int)
        h = torch.zeros(total_samples, 1, dtype=torch.int)
        for idx, (x_val, y_val) in enumerate(zip(x, y)):
            w[idx] = torch.randint(image_width - x_val.item(), (1,))
            h[idx] = torch.randint(image_height - y_val.item(), (1,))
        # Concatenate them to get the bounding boxes
        bboxes = torch.cat((x, y, w, h), dim=1)
        # guarantees that boxes are within image boundaries
        self.assertTrue(torch.all(bboxes[..., 0] + bboxes[..., 2] < image_width))
        self.assertTrue(torch.all(bboxes[..., 1] + bboxes[..., 3] < image_width))
        return bboxes

    def generate_rand_xyxy(self, image_height, image_width, total_samples):
        # Get x and y
        x, y = self.generate_rand_xy(image_height, image_width, total_samples)
        # Random generated x2 and y2 for the bounding boxes
        x2 = torch.zeros(total_samples, 1, dtype=torch.int)
        y2 = torch.zeros(total_samples, 1, dtype=torch.int)
        for idx, (x_val, y_val) in enumerate(zip(x, y)):
            x2[idx] = torch.randint(x_val.item(), image_width, (1,))
            y2[idx] = torch.randint(y_val.item(), image_height, (1,))
        # Concatenate them to get the bounding boxes
        bboxes = torch.cat((x, y, x2, y2), dim=1)
        # guarantees that boxes are within image boundaries
        self.assertTrue(torch.all(bboxes[..., 2] < image_width))
        self.assertTrue(torch.all(bboxes[..., 3] < image_height))
        return bboxes

    def generate_rand_xcycwh(self, image_height, image_width, total_samples):
        # Random generate center points (Xc, Yc) for the bounding boxes
        # Making init_val=1 ensures that the boxes will have a width and height
        xc, yc = self.generate_rand_xy(image_height, image_width, total_samples, init_val=1)
        # Randomly generated widths and heights ensuring they don't exceed twice the distance from center to image borders
        w = torch.zeros(total_samples, 1, dtype=torch.int)
        h = torch.zeros(total_samples, 1, dtype=torch.int)
        for idx, (x_val, y_val) in enumerate(zip(xc, yc)):
            x_val, y_val = x_val.item(), y_val.item()
            w[idx] = 1 + torch.randint(1, 1 + min(x_val, image_width - x_val), (1,))
            h[idx] = 1 + torch.randint(1, 1 + min(y_val, image_height - y_val), (1,))  # add 1 to be inclusive
        bboxes = torch.cat((xc, yc, w, h), dim=1)
        # guarantees that boxes are within image boundaries
        self.assertTrue(torch.all(bboxes[..., 0] < image_width))  # xc lays within image width
        self.assertTrue(torch.all(bboxes[..., 1] < image_height))  # yc lays within image height
        self.assertTrue(torch.all(bboxes[..., 2] <= image_width))  # box width is le than image width
        self.assertTrue(torch.all(bboxes[..., 3] <= image_height))  # box height is le than image height
        return bboxes

    def generate_rand_relxywh(self, image_height, image_width, total_samples):
        # create xywh
        bboxes = self.generate_rand_xywh(image_height, image_width, total_samples)
        # make it relative
        img_shape = torch.tensor((image_width, image_height, image_width, image_height))
        bboxes = bboxes.add_(_EPS).divide(img_shape)
        return bboxes

    def test_converters_xywh(self):
        # Assuming 10 bounding boxes are within an image of size 640x480
        (image_width, image_height) = 640, 480
        total_samples = 10
        # Create bounding boxes in the format XYWH
        bboxes_xywh = self.generate_rand_xywh(image_height, image_width, total_samples)
        # Apply transformation
        transf_boxes_xywh = transform_box_format(bboxes_xywh, orig_format="xywh", dest_format="xywh")
        transf_boxes_xyxy = transform_box_format(
            bboxes_xywh,
            orig_format="xywh",
            dest_format="xyxy",
        )
        transf_boxes_xcycwh = transform_box_format(
            bboxes_xywh,
            orig_format="xywh",
            dest_format="xcycwh",
        )
        # Test transformations
        self.assertTrue(torch.equal(bboxes_xywh, transf_boxes_xywh))
        self.assertFalse(torch.equal(bboxes_xywh, transf_boxes_xyxy))
        self.assertFalse(torch.equal(bboxes_xywh, transf_boxes_xcycwh))
        # Test with torch transformations
        torch_transf_boxes_xywh = box_convert(bboxes_xywh, out_fmt="xywh", in_fmt="xywh")
        torch_transf_boxes_xyxy = box_convert(bboxes_xywh, out_fmt="xyxy", in_fmt="xywh")
        torch_transf_boxes_xcycwh = box_convert(bboxes_xywh, out_fmt="cxcywh", in_fmt="xywh")
        assert torch.equal(transf_boxes_xywh, torch_transf_boxes_xywh)
        assert torch.equal(transf_boxes_xyxy, torch_transf_boxes_xyxy)
        assert torch.equal(transf_boxes_xcycwh, torch_transf_boxes_xcycwh)

    def test_converters_xyxy(self):
        # Assuming 10 bounding boxes are within an image of size 640x480
        (image_width, image_height) = 640, 480
        total_samples = 10
        # Create bounding boxes in the format XYXY
        bboxes_xyxy = self.generate_rand_xyxy(image_height, image_width, total_samples)
        # Apply transformation
        transf_boxes_xyxy = transform_box_format(bboxes_xyxy, orig_format="xyxy", dest_format="xyxy")
        transf_boxes_xywh = transform_box_format(
            bboxes_xyxy,
            orig_format="xyxy",
            dest_format="xywh",
        )
        transf_boxes_xcycwh = transform_box_format(
            bboxes_xyxy,
            orig_format="xyxy",
            dest_format="xcycwh",
        )
        # Test transformations
        self.assertTrue(torch.equal(bboxes_xyxy, transf_boxes_xyxy))
        self.assertFalse(torch.equal(bboxes_xyxy, transf_boxes_xywh))
        self.assertFalse(torch.equal(bboxes_xyxy, transf_boxes_xcycwh))
        # Test with torch transformations
        torch_transf_boxes_xyxy = box_convert(bboxes_xyxy, out_fmt="xyxy", in_fmt="xyxy")
        torch_transf_boxes_xywh = box_convert(bboxes_xyxy, out_fmt="xywh", in_fmt="xyxy")
        torch_transf_boxes_xcycwh = box_convert(bboxes_xyxy, out_fmt="cxcywh", in_fmt="xyxy")
        assert torch.equal(transf_boxes_xywh, torch_transf_boxes_xywh)
        assert torch.equal(transf_boxes_xyxy, torch_transf_boxes_xyxy)
        assert torch.equal(transf_boxes_xcycwh, torch_transf_boxes_xcycwh)

    def test_converters_xcycwh(self):
        # Assuming 10 bounding boxes are within an image of size 640x480
        (image_width, image_height) = 640, 480
        total_samples = 10
        # Create bounding boxes in the format XCYCWH
        bboxes_xcycwh = self.generate_rand_xcycwh(image_height, image_width, total_samples)
        # Apply transformation
        transf_boxes_xcycwh = transform_box_format(bboxes_xcycwh, orig_format="xcycwh", dest_format="xcycwh")
        transf_boxes_xyxy = transform_box_format(bboxes_xcycwh, orig_format="xcycwh", dest_format="xyxy")
        transf_boxes_xywh = transform_box_format(bboxes_xcycwh, orig_format="xcycwh", dest_format="xywh")
        # Test transformations
        self.assertTrue(torch.equal(bboxes_xcycwh, transf_boxes_xcycwh))
        self.assertFalse(torch.equal(bboxes_xcycwh, transf_boxes_xyxy))
        self.assertFalse(torch.equal(bboxes_xcycwh, transf_boxes_xywh))
        # Test with torch transformations
        torch_transf_boxes_xcycwh = box_convert(bboxes_xcycwh, out_fmt="cxcywh", in_fmt="cxcywh")
        torch_transf_boxes_xyxy = box_convert(bboxes_xcycwh, out_fmt="xyxy", in_fmt="cxcywh")
        torch_transf_boxes_xywh = box_convert(bboxes_xcycwh, out_fmt="xywh", in_fmt="cxcywh")
        assert torch.equal(transf_boxes_xcycwh, torch_transf_boxes_xcycwh)
        assert torch.equal(transf_boxes_xyxy, torch_transf_boxes_xyxy)
        assert torch.equal(transf_boxes_xywh, torch_transf_boxes_xywh)

a = 123
a = UtilBoundingBoxConverters()
image_height = 460
image_width = 640
c = 123

boxes_xywh = torch.Tensor(samples["xywh"])