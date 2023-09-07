<!--Copyright 2023 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
-->

# BLIVA

## Overview

The BLIVA model was proposed in [BLIVA: A Simple Multimodal LLM for Better Handling of Text-Rich Visual Questions](https://arxiv.org/abs/2308.09936)  by Wenbo Hu, Yifan Xu, Yi Li, Weiyue Li, Zeyuan Chen, Zhuowen Tu. <INSERT SHORT SUMMARY HERE>

The abstract from the paper is the following:

*Vision Language Models (VLMs), which extend Large Language Models (LLM) by incorporating visual understanding capability, have demonstrated significant advancements in addressing open-ended visual question-answering (VQA) tasks. However, these models cannot accurately interpret images infused with text, a common occurrence in real-world scenarios. Standard procedures for extracting information from images often involve learning a fixed set of query embeddings. These embeddings are designed to encapsulate image contexts and are later used as soft prompt inputs in LLMs. Yet, this process is limited to the token count, potentially curtailing the recognition of scenes with text-rich context. To improve upon them, the present study introduces BLIVA: an augmented version of InstructBLIP with Visual Assistant. BLIVA incorporates the query embeddings from InstructBLIP and also directly projects encoded patch embeddings into the LLM, a technique inspired by LLaVA. This approach assists the model to capture intricate details potentially missed during the query decoding process. Empirical evidence demonstrates that our model, BLIVA, significantly enhances performance in processing text-rich VQA benchmarks (up to 17.76\% in OCR-VQA benchmark) and in undertaking typical VQA benchmarks (up to 7.9\% in Visual Spatial Reasoning benchmark), comparing to our baseline InstructBLIP. BLIVA demonstrates significant capability in decoding real-world images, irrespective of text presence. To demonstrate the broad industry applications enabled by BLIVA, we evaluate the model using a new dataset comprising YouTube thumbnails paired with question-answer sets across 13 diverse categories. For researchers interested in further exploration, our code and models are freely accessible at https://github.com/mlpc-ucsd/BLIVA.git*

Tips:

<INSERT TIPS ABOUT MODEL HERE>

This model was contributed by [rafaelpadilla](<https://huggingface.co/rafaelpadilla). The original code can be found [here](https://github.com/mlpc-ucsd/BLIVA.git).

## BlivaConfig

[[autodoc]] BlivaConfig


## BlivaTokenizer

[[autodoc]] BlivaTokenizer
    - build_inputs_with_special_tokens
    - get_special_tokens_mask
    - create_token_type_ids_from_sequences
    - save_vocabulary


## BlivaTokenizerFast

[[autodoc]] BlivaTokenizerFast


## BlivaModel

[[autodoc]] BlivaModel
    - forward


## BlivaForConditionalGeneration

[[autodoc]] BlivaForConditionalGeneration
    - forward


## BlivaForSequenceClassification

[[autodoc]] BlivaForSequenceClassification
    - forward


## BlivaForQuestionAnswering

[[autodoc]] BlivaForQuestionAnswering
    - forward


## BlivaForCausalLM

[[autodoc]] BlivaForCausalLM
    - forward


