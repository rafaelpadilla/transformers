# coding=utf-8
# Copyright 2023 Facebook AI Research and The HuggingFace Inc. team. All rights reserved.
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
""" RT_DETR model configuration"""


from ...configuration_utils import PretrainedConfig
from ...utils import logging


logger = logging.get_logger(__name__)

RT_DETR_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "rafaelpadilla/porting_rt_detr": "https://huggingface.co/rafaelpadilla/porting_rt_detr/raw/main/config.json",
}


class RTDetrConfig(PretrainedConfig):
    r"""
    This is the configuration class to store the configuration of a [`RTDetrModel`]. It is used to instantiate a
    RT_DETR model according to the specified arguments, defining the model architecture. Instantiating a configuration
    with the defaults will yield a similar configuration to that of the RT_DETR
    [checkpoing/todo](https://huggingface.co/checkpoing/todo) architecture.

    Configuration objects inherit from [`PretrainedConfig`] and can be used to control the model outputs. Read the
    documentation from [`PretrainedConfig`] for more information.

    Args:
        initializer_range (`float`, *optional*, defaults to 0.02):
            The standard deviation of the truncated_normal_initializer for initializing all weight matrices.
        backbone (`str`, *optional*, defaults to `"resnet50d"`):
            Name of convolutional backbone to use.
        out_indices (`List[int]`, *optional*, defaults to `[2, 3, 4]`):
            List of indices of features to output. Can be any of 0, 1, 2, etc. (depending on how many stages the
            backbone has).
        freeze_batch_norm_2d (`bool`, *optional*, defaults to `True`):
            If True, all `BatchNorm2d` and `SyncBatchNorm` layers of the backbone will be replaced by
            `FrozenBatchNorm2d`.
        in_channels (`List[int]`, *optional*, defaults to `[512, 1024, 2048]`):
            List of input channel sizes to be used in each block of the backbone's convolutional layers.
        feat_strides (`List[int]`, *optional*, defaults to `[8, 16, 32]`):
            Strides used in each feature map.
        hidden_dim (`int`, *optional*, defaults to 256):
            Dimension for hidden states in transformer encoder and decoder.
        num_head (`int`, *optional*, defaults to 8):
            Number of attention heads for each attention layer in the transformer encoder and decoder.
        dim_feedforward (`int`, *optional*, defaults to 1024):
            Dimension for feedforward network layer in transformer encoder and decoder.
        dropout (`float`, *optional*, defaults to 0.0):
            The ratio for all dropout layers.
        enc_act (`str`, *optional*, defaults to `"gelu"`):
            Activation function of the encoder used in the `TransformerEncoderLayer`.
        use_encoder_idx (`List[int]`, *optional*, defaults to `[2]`):
            Indexes of the projected layers to be used in the encoder.
        num_encoder_layers (`int`, *optional*, defaults to 1):
            Total of layers to be used by the encoder.
        pe_temperature (`int`, *optional*, defaults to 10000):
            The temperature parameter used to create the positional encodings.
        expansion (`float`, *optional*, defaults to 1.0):
            Expansion factor used by the `CSPRepLayer` module.
        depth_mult (`float`, *optional*, defaults to 1.0):
            Depth multiplicator factor used to create the `CSPRepLayer` module.
        act_encoder (`str`, *optional*, defaults to `"silu"`):
            Activation function of the encoder used in the top-down Feature Pyramid Network and the bottom-up Path
            Aggregation Network.
        eval_size (`Tuple[int, int]`, *optional*):
            Height and width used to computes the effective height and width of the position embeddings after taking
            into account the stride.
        num_classes (`int`, *optional*, defaults to 80):
            Number of target classes or labels used by the detector.
        num_queries (`int`, *optional*, defaults to 300):
            Number of object queries.
        position_embed_type (`str`, *optional*, defaults to `"sine"`):
            A string indicating the type of positional embedding to use. Supported values ["sine", "learned"]
        feat_channels (`List[int]`, *optional*, defaults to `[256, 256, 256]`):
            A list of integers representing the number of feature channels at various layers or stages of the network
        num_levels (`int`, *optional*, defaults to 3):
            The number of feature levels used by the `RTDetrTransformers`.
        num_decoder_points (`int`, *optional*, defaults to 4):
            Number of points used by the `TransformerDecoderLayer`.
        num_decoder_layers (`int`, *optional*, defaults to 6):
            Number of layers of the decoder.
        act_decoder (`str`, *optional*, defaults to `"relu"`):
            Activation function used by the decoder.
        num_denoising (`int`, *optional*, defaults to 100):
            The total number of denoising tasks or queries to be used for contrastive denoising.
        label_noise_ratio (`float`, *optional*, defaults to 0.5):
            The fraction of denoising labels to which random noise should be added.
        box_noise_scale (`float`, *optional*, defaults to 1.0):
            Scale or magnitude of noise to be added to the bounding boxes.
        learnt_init_query (`bool`, *optional*, defaults to `False`):
            Indicates whether the initial query embeddings for the decoder should be learned during training
        eval_spatial_size (`Tuple[int, int]`, *optional*, defaults to `[640, 640]`):
            Height and width used during evaluation to generate the bounding box anchors.
        eval_idx (`int`, *optional*, defaults to -1):
            Id of the decoder layer used to obtain the logits and bounding boxes.
        eps (`float`, *optional*, defaults to 0.01):
            A small positive value used to define the valid range for anchor coordinates.
        matcher_alpha (`float`, *optional*, defaults to 0.25):
            Parameter alpha used by the Hungarian Matcher.
        matcher_gamma (`float`, *optional*, defaults to 2.0):
            Parameter gamma used by the Hungarian Matcher.
        matcher_class_cost (`float`, *optional*, defaults to 2.0):
            The relative weight of the class loss used by the Hungarian Matcher.
        matcher_bbox_cost (`float`, *optional*, defaults to 5.0):
            The relative weight of the bounding box loss used by the Hungarian Matcher.
        matcher_giou_cost (`float`, *optional*, defaults to 2.0):
            The relative weight of the giou loss of used by the Hungarian Matcher.
        use_focal_loss (`bool`, *optional*, defaults to `True`):
            Parameter informing if focal focal should be used.
        aux_loss (`bool`, *optional*, defaults to `True`):
            Parameter informing if auxiliar focal should be used.
        focal_loss_alpha (`float`, *optional*, defaults to 0.75):
            Parameter alpha used to compute the focal loss.
        focal_loss_gamma (`float`, *optional*, defaults to 2.0):
            Parameter gamma used to compute the focal loss.
        weight_loss_vfl (`float`, *optional*, defaults to 1.0):
            Relative weight of the varifocal loss in the object detection loss.
        weight_loss_bbox (`float`, *optional*, defaults to 5.0):
            Relative weight of the L1 bounding box loss in the object detection loss.
        weight_loss_giou (`float`, *optional*, defaults to 2.0):
            Relative weight of the generalized IoU loss in the object detection loss.
        eos_coefficient (`float`, *optional*, defaults to 0.1):
            Relative classification weight of the 'no-object' class in the object detection loss.

    Examples:

    ```python
    >>> from transformers import RTDetrConfig, RTDetrModel

    >>> # Initializing a RT_DETR checkpoing/todo style configuration
    >>> configuration = RTDetrConfig()

    >>> # Initializing a model (with random weights) from the checkpoing/todo style configuration
    >>> model = RTDetrModel(configuration)

    >>> # Accessing the model configuration
    >>> configuration = model.config
    ```"""
    model_type = "rt_detr"
    keys_to_ignore_at_inference = ["past_key_values"]
    attribute_map = {
        "hidden_size": "d_model",
        "num_attention_heads": "encoder_attention_heads",
    }

    def __init__(
        self,
        # General
        initializer_range=0.02,
        # Backbone
        backbone="resnet50d",
        out_indices=[2, 3, 4],
        freeze_batch_norm_2d=True,
        # encoder HybridEncoder
        in_channels=[512, 1024, 2048],
        feat_strides=[8, 16, 32],
        hidden_dim=256,
        num_head=8,
        dim_feedforward=1024,
        dropout=0.0,
        enc_act="gelu",
        use_encoder_idx=[2],
        num_encoder_layers=1,
        pe_temperature=10000,
        expansion=1.0,
        depth_mult=1.0,
        act_encoder="silu",
        eval_size=None,
        # decoder RTDetrTransformer
        num_classes=80,
        num_queries=300,
        position_embed_type="sine",
        feat_channels=[256, 256, 256],
        num_levels=3,
        num_decoder_points=4,
        num_decoder_layers=6,
        act_decoder="relu",
        num_denoising=100,
        label_noise_ratio=0.5,
        box_noise_scale=1.0,
        learnt_init_query=False,
        eval_spatial_size=[640, 640],
        eval_idx=-1,
        eps=1e-2,
        # Loss
        matcher_alpha=0.25,
        matcher_gamma=2.0,
        matcher_class_cost=2.0,
        matcher_bbox_cost=5.0,
        matcher_giou_cost=2.0,
        use_focal_loss=True,
        aux_loss=True,
        focal_loss_alpha=0.75,
        focal_loss_gamma=2.0,
        weight_loss_vfl=1.0,
        weight_loss_bbox=5.0,
        weight_loss_giou=2.0,
        eos_coefficient=0.1,
        **kwargs,
    ):
        # num_labels: number of object categories, omitting the special no-object category
        # eos_coef: relative classification weight applied to the no-object category

        self.initializer_range = initializer_range
        # backbone
        self.backbone = backbone
        self.out_indices = out_indices
        self.freeze_batch_norm_2d = freeze_batch_norm_2d
        # encoder
        self.in_channels = in_channels
        self.feat_strides = feat_strides
        self.hidden_dim = hidden_dim
        self.num_head = num_head
        self.dim_feedforward = dim_feedforward
        self.dropout = dropout
        self.enc_act = enc_act
        self.use_encoder_idx = use_encoder_idx
        self.num_encoder_layers = num_encoder_layers
        self.pe_temperature = pe_temperature
        self.expansion = expansion
        self.depth_mult = depth_mult
        self.act_encoder = act_encoder
        self.eval_size = eval_size
        # decoder
        self.num_classes = num_classes
        self.num_queries = num_queries
        self.position_embed_type = position_embed_type
        self.feat_channels = feat_channels
        self.num_levels = num_levels
        self.num_decoder_points = num_decoder_points
        self.num_decoder_layers = num_decoder_layers
        self.act_decoder = act_decoder
        self.num_denoising = num_denoising
        self.label_noise_ratio = label_noise_ratio
        self.box_noise_scale = box_noise_scale
        self.learnt_init_query = learnt_init_query
        self.eval_spatial_size = eval_spatial_size
        self.eval_idx = eval_idx
        self.eps = eps
        self.aux_loss = aux_loss
        # Loss
        self.matcher_alpha = matcher_alpha
        self.matcher_gamma = matcher_gamma
        self.matcher_class_cost = matcher_class_cost
        self.matcher_bbox_cost = matcher_bbox_cost
        self.matcher_giou_cost = matcher_giou_cost
        self.use_focal_loss = use_focal_loss
        self.focal_loss_alpha = focal_loss_alpha
        self.focal_loss_gamma = focal_loss_gamma
        self.weight_loss_vfl = weight_loss_vfl
        self.weight_loss_bbox = weight_loss_bbox
        self.weight_loss_giou = weight_loss_giou
        self.eos_coefficient = eos_coefficient
        super().__init__(**kwargs)