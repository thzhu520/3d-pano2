# pipeline.py

import subprocess
import shutil
import os
import uuid

def process_panorama(input_path: str) -> str:
    """
    Takes a panoramic image and processes it into a .glb file,
    then moves the output to public/assets/ and returns the scene name.
    """
    # Unique working directory
    uid = uuid.uuid4().hex
    work_dir = f"data/{uid}"
    os.makedirs(work_dir, exist_ok=True)

    # Step 1: Copy image and create data.txt
    input_filename = "input.jpg"
    shutil.copy(input_path, f"{work_dir}/{input_filename}")
    with open(f"{work_dir}/data.txt", "w") as f:
        f.write(f"{input_filename}\n")

    # Step 2: Depth Estimation
    subprocess.run(["sh", "depth-estimation/run_360monodepth.sh", work_dir], check=True)

    # Step 3: Mesh + Inpainting
    subprocess.run(["sh", "inpainting/run_3d_photo_inpainting.sh", work_dir], check=True)

    # Step 4: Find and move .glb file to public assets
    for file in os.listdir("results"):
        if file.endswith(".glb"):
            scene_name = os.path.splitext(file)[0]
            dest_path = f"panorama-converter/public/assets/{file}"
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.move(os.path.join("results", file), dest_path)
            return scene_name  # This is used in frontend: /renderer.html?scene=<name>

    raise RuntimeError("No .glb result found after processing.")
