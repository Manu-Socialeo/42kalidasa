"""
Compiles rendered animation preview frames into MP4 video using OpenCV.
"""

import cv2
import glob
import os
import sys

def compile_preview_video():
    frames_dir = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\anim_frames"
    output_video = r"C:\Users\manpr\Documents\42 Kalidasa\renders\preview\camera_path_preview.mp4"
    
    frame_files = sorted(glob.glob(os.path.join(frames_dir, "frame_*.png")))
    if not frame_files:
        print("ERROR: No animation frames found in", frames_dir)
        sys.exit(1)
        
    print(f"Found {len(frame_files)} frames. Compiling MP4 video...")
    
    first_frame = cv2.imread(frame_files[0])
    h, w, _ = first_frame.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, 24.0, (w, h))
    
    for f in frame_files:
        img = cv2.imread(f)
        if img is not None:
            # write frame twice to maintain 24fps smooth duration (step=2 rendering)
            out.write(img)
            out.write(img)
            
    out.release()
    if os.path.exists(output_video) and os.path.getsize(output_video) > 0:
        print(f"SUCCESS: Video compiled ({os.path.getsize(output_video)/1024:.1f} KB) -> {output_video}")
    else:
        print("ERROR: Failed to create output video!")
        sys.exit(1)

if __name__ == "__main__":
    compile_preview_video()

