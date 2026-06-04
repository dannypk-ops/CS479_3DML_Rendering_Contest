# Team 15 — Hunyuan3D-2 Reproduction Guide

## Environment Setup

### 1. Create and activate conda environment

```bash
conda create -n hunyuan python=3.10 -y
conda activate hunyuan
```

### 2. Install CUDA Toolkit (required for building C++ extensions)

```bash
conda install -c nvidia/label/cuda-12.4.0 cuda-toolkit -y
export CUDA_HOME=$CONDA_PREFIX
```

### 3. Install PyTorch

```bash
pip install torch>=2.6.0 torchvision --index-url https://download.pytorch.org/whl/cu124
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 5. Build custom CUDA extensions (required for texture generation)

```bash
cd hy3dgen/texgen/custom_rasterizer
python setup.py install
cd ../../..

cd hy3dgen/texgen/differentiable_renderer
python setup.py install
```

---

## Models

We use two models from the [`tencent/Hunyuan3D-2`](https://huggingface.co/tencent/Hunyuan3D-2) HuggingFace repository. Both are downloaded automatically on first run.

| Model | HF Subfolder | Size | Role |
|---|---|---|---|
| Hunyuan3D-DiT-v2-0 | `hunyuan3d-dit-v2-0` | 1.1B | Image → bare mesh (shape generation) |
| Hunyuan3D-Paint-v2-0 | `hunyuan3d-paint-v2-0` | 1.3B | Mesh + image → textured mesh |

**Required VRAM:**
- Shape generation only: **6 GB**
- Shape + texture generation (full pipeline): **16 GB**

---

## Running Inference

### Input image

Sample images are provided in the `data/` directory:

```
data/
  nubjuki1.png
  nubjuki2.jpg
```

### Command

Run with the default image (`data/nubjuki1.png`):

```bash
conda activate hunyuan
cd Hunyuan3D-2
python team15_inference.py
```

Run with a custom image:

```bash
python team15_inference.py --image data/nubjuki1.png
```

Specify a custom output directory:

```bash
python team15_inference.py --image data/nubjuki1.png --output_dir my_output
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `--image` | `data/nubjuki1.png` | Path to input image |
| `--output_dir` | `output` | Directory to save output GLB files |

### Output

Two GLB files are saved to the output directory:

```
output/
  shape_only_{image_name}.glb      # bare mesh without texture
  final_textured_{image_name}.glb  # final textured 3D asset
```
