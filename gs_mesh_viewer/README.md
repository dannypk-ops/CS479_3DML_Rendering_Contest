# 3DGS + Animated Mesh Viewer

3D Gaussian Splatting(3DGS)으로 재구성한 실사 배경 위에 애니메이션 GLB 메시를 합성하여 실시간으로 렌더링하고, 카메라 경로를 지정해 영상으로 녹화할 수 있는 단일 HTML 뷰어입니다.

---

## 전체 파이프라인

```
영상/이미지 촬영
      │
      ▼
  COLMAP (SfM)          ← GUI, Pinhole 카메라 모델, default 옵션
      │  카메라 포즈 + 희소 포인트 클라우드 생성
      ▼
  3DGS 학습             ← gaussian-splatting 공식 레포 사용
      │  .ply 생성 (scene/origin_compressed.ply)
      ▼
  gs_mesh_viewer        ← PLY + GLB 합성 뷰어
```

---

## 1. COLMAP 설치

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y \
    colmap \
    libboost-all-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev
```

또는 최신 빌드를 소스에서 직접 컴파일할 경우:

```bash
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -GNinja -DCMAKE_BUILD_TYPE=Release
ninja
sudo ninja install
```

### Windows / macOS

공식 릴리즈 바이너리를 사용합니다:
- https://github.com/colmap/colmap/releases

---

## 2. COLMAP — SfM 실행 (GUI, Pinhole 카메라 모델)

> COLMAP inference는 **GUI**로 진행하였으며, 별도 커스텀 없이 **default 옵션**을 사용했습니다.
> 카메라 모델은 **PINHOLE**로 지정합니다.

### 이미지 준비

촬영한 이미지를 아래 구조로 정리합니다:

```
my_scene/
└── images/
    ├── IMG_0001.jpg
    ├── IMG_0002.jpg
    └── ...
```

### GUI 실행 순서

```bash
colmap gui
```

1. **File → New Project** 선택
   - Database: `my_scene/database.db` 지정
   - Images: `my_scene/images/` 폴더 지정

2. **Processing → Feature extraction**
   - Camera model: `PINHOLE` 선택
   - 나머지 옵션: **default** 유지
   - **Extract** 클릭

3. **Processing → Feature matching**
   - Matching method: `Exhaustive` (이미지 수가 적을 경우) 또는 `Sequential`
   - 나머지 옵션: **default** 유지
   - **Run** 클릭

4. **Reconstruction → Start reconstruction**
   - 옵션: **default** 유지
   - 재구성 완료 후 뷰어에서 카메라 포즈와 희소 포인트 클라우드 확인

5. **File → Export model as TXT** (또는 BIN)
   - 저장 경로: `my_scene/sparse/0/`
   - `cameras.txt`, `images.txt`, `points3D.txt` 생성 확인

---

## 3. 3D Gaussian Splatting 학습

### 레포 클론 및 환경 세팅

```bash
git clone https://github.com/graphdeco-inria/gaussian-splatting.git --recursive
cd gaussian-splatting
```

conda 환경 생성 및 의존성 설치:

```bash
conda env create --file environment.yml
conda activate gaussian_splatting
```

> GPU: CUDA 지원 NVIDIA GPU 필수 (VRAM 8GB 이상 권장)

### 학습 실행

```bash
python train.py -s /path/to/my_scene
```

COLMAP 결과가 `my_scene/sparse/0/` 아래에 있고, 이미지가 `my_scene/images/` 에 있으면 자동으로 인식됩니다.

주요 옵션:

```bash
python train.py \
    -s /path/to/my_scene \
    -m /path/to/output \          # 결과 저장 경로 (기본: output/<hash>)
    --iterations 30000 \          # 학습 반복 횟수 (기본값)
    --eval                        # 평가셋 분리 여부
```

학습 완료 후 결과물:

```
output/
└── <run_id>/
    ├── point_cloud/
    │   └── iteration_30000/
    │       └── point_cloud.ply   ← 뷰어에 사용할 PLY 파일
    └── cameras.json
```

### PLY 압축 (용량 최적화, 선택사항)

용량이 큰 경우 [gsplat-compress](https://github.com/graphdeco-inria/gaussian-splatting) 또는 별도 압축 도구로 경량화합니다. 본 프로젝트의 `scene/origin_compressed.ply` (~27 MB)는 압축 후 결과물입니다.

---

## 4. 뷰어 실행

### 서버 시작

```bash
cd gs_mesh_viewer
python server.py
```

브라우저에서 `http://localhost:8080/gs_mesh_viewer.html` 접속

> `server.py`는 `Cross-Origin-Opener-Policy` / `Cross-Origin-Embedder-Policy` 헤더를 추가한 커스텀 SimpleHTTPServer입니다. SharedArrayBuffer 사용을 위해 일반 `python -m http.server` 대신 반드시 이 서버를 사용해야 합니다.

### 파일 구조

```
gs_mesh_viewer/
├── gs_mesh_viewer.html     # 뷰어 본체
├── server.py               # 로컬 HTTP 서버
├── scene/
│   └── origin_compressed.ply   # 3DGS PLY 파일
├── glb/
│   ├── nubjuki1.glb
│   ├── nubjuki2.glb
│   ├── nubjuki3_pink.glb
│   ├── nubjuki4_green.glb
│   └── new_slow_hubo.glb
└── config/
    └── scene_config.json   # 씬 레이아웃 저장 설정
```

### 기본 사용 흐름

1. **3DGS PLY 경로** 입력 후 `Load 3DGS` 클릭
2. **GLB 경로** 입력 후 `+ Add GLB` 클릭 (또는 `Load All GLBs`)
3. 슬라이더로 각 GLB의 위치/스케일/회전 조정
4. 원하는 뷰에서 `+ Add Current View`로 카메라 키프레임 등록
5. `▶ Preview Path`로 카메라 이동 경로 미리보기
6. `⏺ Record`로 WebM 영상 녹화 및 자동 다운로드
7. `💾 Save Config`로 현재 씬 설정 저장

---

## 의존성 (뷰어)

| 라이브러리 | 버전 | 용도 |
|-----------|------|------|
| [Three.js](https://threejs.org/) | 0.180.0 | 3D 렌더링 엔진, GLB 로더 |
| [@sparkjsdev/spark](https://sparkjs.dev/) | 2.1.0 | 3DGS Gaussian Splat 렌더러 |

모든 의존성은 CDN에서 로드되므로 별도 설치 불필요합니다.
