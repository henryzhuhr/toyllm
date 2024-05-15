---
lastUpdated: true
editLink: true
footer: true
outline: deep
---


# 项目使用文档

## 项目介绍
本项目是一个大模型的集成，计划完成包括对话交流、指令分解、文本实体抽取、文本生成等功能，目前项目处于早期阶段。

## 项目进展

- TODO: 引入更多大模型。聊天只是一个最基本的功能，利用大模型的理解能力和生成能力，才是真正要做的
- 「2024.04.28」 基于千文大模型(Qwen1.5)的模型导出和模型推理测试，并且完成了上下文对话的测试，能记录用户的对话历史
- 「2024.04.26」 项目启动
<!-- 
## 环境要求
本项目在以下环境中测试通过：

| 系统          | CPU       | GPU      |
| ------------- | --------- | -------- |
| Ubuntu 22.04  | i9-13900K | RTX 4090 |
| Sonoma 12.0.1 | M1 Pro    | M1 Pro   | -->

## 环境配置

### 获取源码
获取项目源码
::: code-group

```shell [HTTP]
git clone https://github.com/HenryZhuHR/toyllm
cd toyllm
```

```shell [SSH]
git clone git@github.com:HenryZhuHR/toyllm.git
cd toyllm
```

:::


### 文档本地启动

该项目的文档可以本地启动，运行
```shell
pnpm docs:dev
```

### 创建环境

确保安装了 conda ，如果没有安装，请从 [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) 下载，或者快速安装
  
```shell
# linux x64
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

运行脚本快速创建环境，会在当前目录下 `.env/toyllm` 创建环境，并安装依赖
```shell
bash scripts/init-env.sh
# zsh ...
```
> 默认 Python 版本为系统 Python 版本，如果希望指定版本，可以在脚本 `scripts/init-env.sh` 中取消注释 `CUSTOM_PYTHON_VERSION=3.10`，并修改为指定版本

手动激活该环境
```shell
conda activate .env/toyllm
```

## 项目使用说明

目前，仅实现了 **千问模型(Qwen1.5)** 的对话交流功能

### 导出模型

导出模型，运行
```shell
python3 export.py [--model_id MODEL_ID] [--quan_type MODEL_NAME]
```
- `--model_id`：huggingface 中的模型 id，默认为 `Qwen/Qwen1.5-1.8B-Chat`
- `--quan_type`：量化类型，支持 `fp16`/`int8`/`int4`，默认为 `int8`
- tokenizer 和模型会被一同默认导出到 `./weights` 目录下，不作区分，并估计 `model_id` 命名，因此

### 模型推理

对话交流模型功能，以及预设了部分对话，可以直接运行方面测试模型效果，运行
```shell
python3 infer-chat.py [--model_id MODEL_ID] [--model_path MODEL_PATH] [--device DEVICE]
```
- `--model_id`：huggingface 中的模型 id，默认为 `Qwen/Qwen1.5-1.8B-Chat`
- `--model_path`：模型路径，该参数为模型导出的路径

推理结果中可以看到，该模型可以记录用户的对话历史，并根据上下文进行对话


## 参考资料

- 🚀 千文大模型 [QwenLM/Qwen1.5](https://github.com/QwenLM/Qwen1.5?tab=readme-ov-file)


## 论文引用

千文大模型的技术报告
```bibtex
@article{qwen,
  title={Qwen Technical Report},
  author={Jinze Bai and Shuai Bai and Yunfei Chu and Zeyu Cui and Kai Dang and Xiaodong Deng and Yang Fan and Wenbin Ge and Yu Han and Fei Huang and Binyuan Hui and Luo Ji and Mei Li and Junyang Lin and Runji Lin and Dayiheng Liu and Gao Liu and Chengqiang Lu and Keming Lu and Jianxin Ma and Rui Men and Xingzhang Ren and Xuancheng Ren and Chuanqi Tan and Sinan Tan and Jianhong Tu and Peng Wang and Shijie Wang and Wei Wang and Shengguang Wu and Benfeng Xu and Jin Xu and An Yang and Hao Yang and Jian Yang and Shusheng Yang and Yang Yao and Bowen Yu and Hongyi Yuan and Zheng Yuan and Jianwei Zhang and Xingxuan Zhang and Yichang Zhang and Zhenru Zhang and Chang Zhou and Jingren Zhou and Xiaohuan Zhou and Tianhang Zhu},
  journal={arXiv preprint arXiv:2309.16609},
  year={2023}
}
```

<!-- ## License

本项目遵循 [GPL-3.0](https://opensource.org/licenses/GPL-3.0) 协议，请遵循协议使用本项目。 -->