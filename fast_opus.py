import os
import subprocess
import shutil
import sys
import time
import tempfile
from concurrent.futures import ThreadPoolExecutor

def run_parallel_cmd(args):
    """Executes a single chunk command in its own thread block safely."""
    cmd, chunk_index = args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\n[FFmpeg Error on Chunk {chunk_index}]: {result.stderr.strip()}")
    return chunk_index

# 1. Cross-platform check for FFmpeg and FFprobe installation
if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
    print("\n[ERROR] FFmpeg or FFprobe is not installed or not found in your system PATH!")
    print("Please ensure both 'ffmpeg' and 'ffprobe' are available on your system.")
    input("\nPress ENTER to exit...")
    exit(1)

# 2. Scan directory for any valid media file
IGNORED_EXTENSIONS = {'.py', '.txt', '.opus', '.exe', '.bat', '.sh'}
media_files = sorted([
    f for f in os.listdir('.') 
    if os.path.isfile(f) and os.path.splitext(f)[1].lower() not in IGNORED_EXTENSIONS
])

if not media_files:
    print("\n[ERROR] No valid media files found in this directory!")
    input("\nPress ENTER to exit...")
    exit(1)

# Interactive file selection menu
if len(media_files) == 1:
    INPUT_FILE = media_files[0]
else:
    print("\nMultiple media files found:")
    for i, filename in enumerate(media_files, start=1):
        print(f"  [{i}] {filename}")
    
    while True:
        try:
            choice = input(f"\nSelect a file number (1-{len(media_files)}): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(media_files):
                INPUT_FILE = media_files[choice_idx]
                break
            else:
                print(f"Invalid selection. Please choose a number between 1 and {len(media_files)}.")
        except ValueError:
            print("Please enter a valid number.")

print(f"\nTarget file: '{INPUT_FILE}'")

# Perfect Extension Replacement
file_base_name, _ = os.path.splitext(INPUT_FILE)
OUTPUT_FILE = f"{file_base_name}.opus"

# Overwrite check validation logic
if os.path.exists(OUTPUT_FILE):
    print(f"\n[WARNING] Output file '{OUTPUT_FILE}' already exists!")
    overwrite_choice = input("Do you want to overwrite it? (y/n) [Default: n]: ").strip().lower()
    if overwrite_choice not in ['y', 'yes']:
        print("Skipping process. Operation canceled by user.\n")
        input("Press ENTER to exit...")
        exit(0)

# Record original file size
original_size_bytes = os.path.getsize(INPUT_FILE)

# --- INTERACTIVE SETTINGS PROMPTS ---
print("\n--- Audio Compression Configuration ---")

# 1. Bitrate Prompt
bitrate_input = input("Enter audio bitrate (e.g., 6k, 12k, 16k, 24k) [Default: 16k]: ").strip().lower()
if not bitrate_input:
    BITRATE = "16k"
else:
    BITRATE = bitrate_input if bitrate_input.endswith('k') else f"{bitrate_input}k"

# 2. DTX Prompt
dtx_input = input("Enable DTX (Discontinuous Transmission)? (y/n) [Default: y]: ").strip().lower()
if not dtx_input or dtx_input == 'y' or dtx_input == 'yes':
    USE_DTX = "1"
else:
    USE_DTX = "0"

# 3. Frame Length Prompt
frame_input = input("Enter frame duration in ms (10, 20, 40, 60) [Default: 60]: ").strip()
if frame_input in ["10", "20", "40", "60"]:
    FRAME_DURATION = frame_input
else:
    FRAME_DURATION = "60"

# 4. High-Pass Filter Prompt
hpf_input = input("Enter High-Pass Filter cutoff frequency in Hz (0 to disable) [Default: 100]: ").strip()
if not hpf_input:
    HPF_FREQ = 100
else:
    try:
        HPF_FREQ = int(hpf_input)
        if HPF_FREQ < 0:
            print("[WARNING] Negative frequency entered. Defaulting to 100Hz.")
            HPF_FREQ = 100
    except ValueError:
        print("[WARNING] Invalid number entered. Defaulting to 100Hz.")
        HPF_FREQ = 100

# 5. CPU Worker Thread Allocation Prompt
system_threads = os.cpu_count() or 4
default_workers = min(8, system_threads)

worker_input = input(f"Enter number of parallel CPU workers (1-{system_threads}) [Default: {default_workers}]: ").strip()
if not worker_input:
    WORKERS = default_workers
else:
    try:
        WORKERS = int(worker_input)
        if WORKERS < 1:
            print(f"[WARNING] Minimum value is 1. Defaulting to {default_workers}.")
            WORKERS = default_workers
    except ValueError:
        print("[WARNING] Invalid number entered. Defaulting to {default_workers}.")
        WORKERS = default_workers

print(f"\nApplying settings:")
print(f" -> Bitrate: {BITRATE}")
print(f" -> DTX: {'Enabled' if USE_DTX=='1' else 'Disabled'}")
print(f" -> Frame Duration: {FRAME_DURATION}ms")
print(f" -> High-Pass Filter: {f'{HPF_FREQ}Hz' if HPF_FREQ > 0 else 'Disabled'}")
print(f" -> CPU Workers: {WORKERS} parallel processing tasks")
print("---------------------------------------")

# 3. Safe native duration parsing via FFprobe
print("Analyzing media timeline bounds via FFprobe...")
ffprobe_cmd = [
    'ffprobe', '-v', 'error', 
    '-show_entries', 'format=duration', 
    '-of', 'default=noprint_wrappers=1:nokey=1', 
    INPUT_FILE
]
dur_result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)

try:
    total_duration = float(dur_result.stdout.strip())
except ValueError:
    print("[ERROR] FFprobe could not read the media duration.")
    input("\nPress ENTER to exit...")
    exit(1)

chunk_duration = max(1.0, total_duration / WORKERS)

# --- START PROCESSING TIMER ---
start_processing_time = time.time()

# Create a high-speed system temporary directory context
with tempfile.TemporaryDirectory() as ram_dir:
    print(f"Mounted temporary fast-storage space...")
    
    cmds_task_list = []
    chunk_files = []

    for i in range(WORKERS):
        start_time = i * chunk_duration
        chunk_name = os.path.join(ram_dir, f"part_{i:04d}.opus")
        chunk_files.append(chunk_name)
        
        audio_filters = []
        if HPF_FREQ > 0:
            audio_filters.extend(['-af', f"highpass=f={HPF_FREQ}"])
            
        cmd = [
            'ffmpeg', '-y',
            '-ss', f"{start_time:.3f}",           
            '-i', INPUT_FILE,
            '-ss', '0.000',                       
            '-t', f"{chunk_duration:.3f}",
            '-vn'
        ]
        
        cmd.extend(audio_filters)
        cmd.extend([
            '-c:a', 'libopus', 
            '-ac', '1', 
            '-b:a', BITRATE, 
            '-vbr', 'on', 
            '-application', 'voip', 
            '-dtx', USE_DTX,               
            '-frame_duration', FRAME_DURATION, 
            '-compression_level', '0',
            chunk_name
        ])
        
        cmds_task_list.append((cmd, i + 1))

    # 5. Multithreading UI Progress Execution
    completed_tasks = 0
    sys.stdout.write(f"Processing media... [0/{WORKERS} Tasks Complete]")
    sys.stdout.flush()

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        for chunk_index in executor.map(run_parallel_cmd, cmds_task_list):
            completed_tasks += 1
            percent = int((completed_tasks / WORKERS) * 10)
            bar = "■" * percent + "□" * (10 - percent)
            sys.stdout.write(f"\rProcessing media... [{bar}] {completed_tasks}/{WORKERS} Tasks")
            sys.stdout.flush()

    print("\nProcessing complete!")

    # 6. Concatenate the chunks seamlessly
    print("Stitching chunks back together onto the target drive...")
    list_file = os.path.join(ram_dir, "list.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            # FIXED: Absolute paths require an explicit absolute layout formatting in list.txt
            # We turn the windows/unix path into a clean URL-like syntax that the concat filter accepts
            abs_path = os.path.abspath(cf).replace('\\', '/')
            f.write(f"file '{abs_path}'\n")

    numeric_bitrate = BITRATE.replace('k', '000')

    # FIXED: Added the -unsafe 0 flag explicitly back into the array command block 
    # to allow FFmpeg to load absolute paths from out-of-directory RAM temp spaces
    stitch_cmd = [
        'ffmpeg', '-y', 
        '-f', 'concat', 
        '-safe', '0', 
        '-i', list_file, 
        '-c', 'copy', 
        '-metadata:s:a:0', f'bitrate={numeric_bitrate}', 
        OUTPUT_FILE
    ]
    subprocess.run(stitch_cmd, capture_output=True)

# --- STOP PROCESSING TIMER ---
elapsed_time = time.time() - start_processing_time

# --- CALCULATE & DISPLAY COMPRESSION REPORT ---
if os.path.exists(OUTPUT_FILE):
    final_size_bytes = os.path.getsize(OUTPUT_FILE)
    
    orig_mb = original_size_bytes / (1024 * 1024)
    final_mb = final_size_bytes / (1024 * 1024)
    
    if original_size_bytes > 0:
        compression_ratio = (final_size_bytes / original_size_bytes) * 100
        savings_percentage = 100 - compression_ratio
    else:
        compression_ratio, savings_percentage = 0.0, 0.0

    print(f"Process Finished! Saved optimized file to '{OUTPUT_FILE}'")
    print("\n================ COMPRESSION REPORT ================")
    print(f"Original File Size:   {orig_mb:.2f} MB")
    print(f"Compressed File Size: {final_mb:.2f} MB")
    print(f"Size Reduction:       {savings_percentage:.1f}% smaller")
    print(f"Compression Ratio:    {original_size_bytes / max(1, final_size_bytes):.1f}:1")
    print(f"Total Processing Time:{elapsed_time:.2f} seconds")  
    print("====================================================\n")
else:
    print("[ERROR] Output file creation could not be verified. Check if your RAM path permitted writing.")

input("Job done! Press ENTER to exit this window...")
