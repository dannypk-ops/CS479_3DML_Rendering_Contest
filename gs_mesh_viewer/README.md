# 3DGS + Animated Mesh Viewer

A web-based viewer that renders a real-world 3DGS scene together with animated GLB meshes, with camera keyframe recording support.

---

## Pipeline

```
Image Capture → COLMAP (SfM) → 3DGS Training → PLY Compression → Web Viewer
```

---

## 1. COLMAP

Install on macOS:
```bash
brew install colmap
```

Run GUI and proceed with **all default options**:
```bash
colmap gui
```
1. File → New Project (set database & image folder)
2. Processing → Feature extraction (Camera model: `PINHOLE`)
3. Processing → Feature matching
4. Reconstruction → Start reconstruction
5. File → Export model as TXT

---

## 2. 3D Gaussian Splatting

Repository: https://github.com/graphdeco-inria/gaussian-splatting

```bash
git clone https://github.com/graphdeco-inria/gaussian-splatting.git --recursive
cd gaussian-splatting
conda env create --file environment.yml
conda activate gaussian_splatting
```

Training:
```bash
python train.py \
    -s /path/to/colmap_output \
    --iterations 80000 \
    --densify_until_iter 30000
```

Output: `output/<run_id>/point_cloud/iteration_80000/point_cloud.ply`

---

## 3. PLY Compression

Using [SuperSplat](https://superspl.at/editor) (MIT License) via GUI:

1. Open https://superspl.at/editor
2. Drag & drop `point_cloud.ply`
3. `Scene → Export → Compressed PLY`

---

## 4. Viewer

Start server:
```bash
cd gs_mesh_viewer
python server.py
```

Access at `http://localhost:8080/gs_mesh_viewer.html`

> `server.py` is required (adds COOP/COEP headers for SharedArrayBuffer). Do **not** use `python -m http.server`.

For remote server, forward port via SSH:
```bash
ssh -L 8080:localhost:8080 username@server-ip
```

---

## 5. Usage

1. Enter PLY path → **Load 3DGS**
2. Enter GLB path → **+ Add GLB** (or **↓ Load All GLBs**)
3. Adjust position / scale / rotation per GLB
4. **💾 Save Config** to save scene layout → place in `config/scene_config.json`
5. **📂 Load Config** to restore layout next session
6. Add camera keyframes → **⏺ Record** to export `3dgs_scene.webm`

---

## 6. File Size

| File | Size |
|---|---|
| scene (compressed PLY) | 27.5 MB |
| animation_hubo.glb | 11.7 MB |
| nubjuki1.glb | 10.5 MB |
| nubjuki2.glb | 12.7 MB |
| nubjuki3_pink.glb | 11.5 MB |
| nubjuki4_green.glb | 12.6 MB |
| **Total** | **≈ 86.5 MB** |

---

## 7. Dependencies

All viewer libraries are loaded via CDN — **no installation required**.

| Library | Version | Purpose |
|---|---|---|
| [Three.js](https://threejs.org/) | 0.180.0 | 3D rendering, GLB loader |
| [@sparkjsdev/spark](https://sparkjs.dev/) | 2.1.0 | Gaussian splat renderer |

| Tool | License | Purpose |
|---|---|---|
| [gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) | Inria | Scene training |
| [COLMAP](https://github.com/colmap/colmap) | BSD | Camera pose estimation |
| [SuperSplat](https://github.com/playcanvas/supersplat) | MIT | PLY compression |

---

## Citation

```bibtex
@article{kerbl3Dgaussians,
    author  = {Kerbl, Bernhard and Kopanas, Georgios and Leimk{\"u}hler, Thomas and Drettakis, George},
    title   = {3D Gaussian Splatting for Real-Time Radiance Field Rendering},
    journal = {ACM Transactions on Graphics},
    year    = {2023},
    volume  = {42},
    number  = {4}
}
```
