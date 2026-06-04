import argparse
import os
import torch
from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
from hy3dgen.texgen import Hunyuan3DPaintPipeline

def parse_args():
    parser = argparse.ArgumentParser(description="Hunyuan3D-2 Image to 3D GLB Generation")
    parser.add_argument(
        "--image", type=str,
        default=os.path.join("data", "nubjuki1.png"),
        help="Path to input image (default: data/nubjuki1.png)"
    )
    parser.add_argument(
        "--output_dir", type=str, default="output",
        help="Directory to save output GLB files (default: output)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    img_path = args.image
    img_name = os.path.splitext(os.path.basename(img_path))[0]
    out_dir = args.output_dir
    os.makedirs(out_dir, exist_ok=True)

    # ==========================================
    # Step 1: Shape Model 로드 및 Geometry 생성
    # ==========================================
    shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
        "tencent/Hunyuan3D-2",
        subfolder="hunyuan3d-dit-v2-0"
    )
    shape_pipeline.to("cuda")

    print("Shape 모델 로드 완료. 메쉬를 생성합니다...")
    mesh = shape_pipeline(image=img_path)[0]

    shape_out = os.path.join(out_dir, f"shape_only_{img_name}.glb")
    mesh.export(shape_out)
    print(f"Shape 저장 완료: {shape_out}")

    # ==========================================
    # OOM(Out of Memory) 방지를 위한 메모리 정리
    # ==========================================
    del shape_pipeline
    torch.cuda.empty_cache()

    # ==========================================
    # Step 2: Texture Model 로드 및 텍스처링
    # ==========================================
    texture_pipeline = Hunyuan3DPaintPipeline.from_pretrained(
        "tencent/Hunyuan3D-2",
        subfolder="hunyuan3d-paint-v2-0"
    )

    print("Texture 모델 로드 완료. 텍스처를 합성합니다...")
    textured_mesh = texture_pipeline(mesh=mesh, image=img_path)

    texture_out = os.path.join(out_dir, f"final_textured_{img_name}.glb")
    textured_mesh.export(texture_out)
    print(f"최종 결과물 저장 완료: {texture_out}")


if __name__ == "__main__":
    main()
