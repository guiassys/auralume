import torch
from diffusers import AnimateDiffPipeline, MotionAdapter, EulerDiscreteScheduler
from PIL import Image
import os
import cv2
import numpy as np
from datetime import datetime

def export_to_video(frames, output_path, fps=8):
    """Exports a list of PIL Images to a video file using OpenCV with a highly compatible codec."""
    print(f"Exporting to video at {output_path} using OpenCV...")

    first_frame = frames[0]
    width, height = first_frame.size

    # Ensure dimensions are even for maximum compatibility
    if width % 2 != 0: width -= 1
    if height % 2 != 0: height -= 1

    # Define the codec ('mp4v' for MPEG-4) and create VideoWriter object
    fourcc_str = 'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not writer.isOpened():
        raise IOError(f"Could not open video writer for path {output_path}. Check if the '{fourcc_str}' codec is supported by your OpenCV/FFmpeg installation. Try other codecs like 'xvid'.")

    for frame in frames:
        # Resize frame to even dimensions if necessary
        if frame.size != (width, height):
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
        
        # Convert PIL image (RGB) to OpenCV image (BGR)
        frame_np = np.array(frame)
        frame_bgr = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)

    writer.release()
    print("Done.")

def animate_breathing_loop(image_path, output_path):
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # 0. Set device and data type
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    print(f"Using device: {device}")

    # 1. Load models
    adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=dtype)
    model_id = "emilianJR/epiCRealism"
    pipe = AnimateDiffPipeline.from_pretrained(model_id, motion_adapter=adapter, torch_dtype=dtype)
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, beta_schedule="linear", timestep_spacing="linspace")

    # 2. Load IP-Adapter
    input_image = Image.open(image_path).convert("RGB")
    pipe.load_ip_adapter("h94/IP-Adapter", subfolder="models", weight_name="ip-adapter_sd15.bin")
    pipe.set_ip_adapter_scale(0.95)

    # 3. Enable memory-saving optimizations
    pipe.enable_vae_slicing()
    if device == "cuda":
        pipe.enable_model_cpu_offload()

    # 4. Define prompts
    prompt = (
        "masterpiece, best quality, anime style, 1girl, angel, sitting on a ledge, "
        "overlooking a city at night, subtle breathing, chest and shoulders rising and falling, "
        "wings slightly moving, static camera"
    )
    negative_prompt = (
        "bad quality, worse quality, low quality, deformed, distorted, disfigured, ugly, blurry, "
        "low resolution, motion blur, frame blending, ghosting, noisy, weird colors, artifacts, "
        "bad anatomy, bad hands, bad feet, bad eyes, bad face, bad proportions, extra limbs, "
        "extra fingers, extra toes, fused fingers, too many fingers, long neck, username, "
        "watermark, signature, text, error, cropped, out of frame, jpeg artifacts, "
        "compression artifacts, camera movement, zoom, pan, tilt, shake"
    )

    # 5. Generate animation
    print("Generating animation...")
    generator_device = "cpu" if device == "cuda" else device
    generator = torch.Generator(generator_device).manual_seed(42)
    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        ip_adapter_image=input_image,
        num_frames=16,
        guidance_scale=7.5,
        num_inference_steps=30,
        generator=generator,
    )
    frames = output.frames[0]
    print(f"Animation generated with {len(frames)} frames.")

    # 6. Export to Video
    export_to_video(frames, output_path)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.mp4"
    
    # Define paths
    image_file = os.path.join(script_dir, "..", "assets", "Silence_Feels_Like_Home.webp")
    output_video_path = os.path.join(script_dir, "..", "..", "outputs", "animations", filename)
    
    animate_breathing_loop(image_file, output_video_path)
