# ========================= IMPORT REQUIRED LIBRARIES =========================
from glob import glob                      # For matching file patterns (e.g., *.jpg)
import shutil                             # For file and folder operations
import torch                              # Deep learning framework (used for inference)
from time import strftime                 # To generate unique time-based folder names
import os, sys, time                      # OS-level utilities and system path handling
from argparse import ArgumentParser       # For reading CLI arguments

# =================== IMPORT SADTALKER CORE MODULES ===========================
from src.utils.preprocess import CropAndExtract                    # Handles image preprocessing & 3DMM feature extraction
from src.test_audio2coeff import Audio2Coeff                       # Converts audio features to face motion coefficients
from src.facerender.animate import AnimateFromCoeff                # Renders video from motion coefficients
from src.generate_batch import get_data                            # Prepares batch for audio2coeff stage
from src.generate_facerender_batch import get_facerender_data      # Prepares batch for rendering
from src.utils.init_path import init_path                          # Loads model/config paths based on input
# ============================================================================

# =========================== MAIN FUNCTION START =============================
def main(args):
    # ---------------------- SETUP PATHS & CONFIG -----------------------
    pic_path = args.source_image
    audio_path = args.driven_audio
    save_dir = os.path.join(args.result_dir, strftime("%Y_%m_%d_%H.%M.%S"))  # Unique folder for each output
    os.makedirs(save_dir, exist_ok=True)

    pose_style = args.pose_style
    device = args.device
    batch_size = args.batch_size
    input_yaw_list = args.input_yaw
    input_pitch_list = args.input_pitch
    input_roll_list = args.input_roll
    ref_eyeblink = args.ref_eyeblink
    ref_pose = args.ref_pose

    current_root_path = os.path.split(sys.argv[0])[0]

    # ------------ INIT PATHS FOR MODELS & CONFIG FILES ----------------
    sadtalker_paths = init_path(args.checkpoint_dir, os.path.join(current_root_path, 'src/config'),
                                args.size, args.old_version, args.preprocess)

    # ------------ LOAD SADTALKER MODELS -------------------------------
    preprocess_model = CropAndExtract(sadtalker_paths, device)
    audio_to_coeff = Audio2Coeff(sadtalker_paths, device)
    animate_from_coeff = AnimateFromCoeff(sadtalker_paths, device)

    # ------------------- STEP 1: PREPROCESS IMAGE ---------------------
    first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
    os.makedirs(first_frame_dir, exist_ok=True)
    print('Extracting 3DMM features from source image')

    first_coeff_path, crop_pic_path, crop_info = preprocess_model.generate(
        pic_path, first_frame_dir, args.preprocess,
        source_image_flag=True, pic_size=args.size)

    if first_coeff_path is None:
        print("❌ Could not extract coefficients from source image.")
        return

    # ----------------- OPTIONAL: PROCESS EYE BLINK REFERENCE ----------
    if ref_eyeblink:
        blink_video_name = os.path.splitext(os.path.basename(ref_eyeblink))[0]
        blink_frame_dir = os.path.join(save_dir, blink_video_name)
        os.makedirs(blink_frame_dir, exist_ok=True)
        print('Extracting eye blink reference coefficients')

        ref_eyeblink_coeff_path, _, _ = preprocess_model.generate(
            ref_eyeblink, blink_frame_dir, args.preprocess, source_image_flag=False)
    else:
        ref_eyeblink_coeff_path = None

    # ----------------- OPTIONAL: PROCESS POSE REFERENCE ---------------
    if ref_pose:
        if ref_pose == ref_eyeblink:
            ref_pose_coeff_path = ref_eyeblink_coeff_path
        else:
            pose_video_name = os.path.splitext(os.path.basename(ref_pose))[0]
            pose_frame_dir = os.path.join(save_dir, pose_video_name)
            os.makedirs(pose_frame_dir, exist_ok=True)
            print('Extracting head pose reference coefficients')

            ref_pose_coeff_path, _, _ = preprocess_model.generate(
                ref_pose, pose_frame_dir, args.preprocess, source_image_flag=False)
    else:
        ref_pose_coeff_path = None

    # ------------------- STEP 2: AUDIO → COEFFICIENTS -----------------
    print("Converting audio to motion coefficients")
    batch = get_data(first_coeff_path, audio_path, device, ref_eyeblink_coeff_path, still=args.still)
    coeff_path = audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path)

    # ----------- OPTIONAL: GENERATE 3D VISUALIZATION ------------------
    if args.face3dvis:
        from src.face3d.visualize import gen_composed_video
        gen_composed_video(args, device, first_coeff_path, coeff_path, audio_path,
                           os.path.join(save_dir, '3dface.mp4'))

    # ------------------- STEP 3: COEFF → VIDEO ------------------------
    print("Rendering animated video")
    data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path,
                               batch_size, input_yaw_list, input_pitch_list, input_roll_list,
                               expression_scale=args.expression_scale, still_mode=args.still,
                               preprocess=args.preprocess, size=args.size)

    result = animate_from_coeff.generate(data, save_dir, pic_path, crop_info,
                                         enhancer=args.enhancer,
                                         background_enhancer=args.background_enhancer,
                                         preprocess=args.preprocess,
                                         img_size=args.size)

    # --------------------- SAVE FINAL VIDEO ---------------------------
    shutil.move(result, save_dir + '.mp4')
    print('✅ Generated video saved as:', save_dir + '.mp4')

    # -------------------- CLEANUP TEMP FILES (optional) ---------------
    if not args.verbose:
        shutil.rmtree(save_dir)
# ======================================================================

# ========================== ENTRY POINT ===============================
if __name__ == '__main__':
    parser = ArgumentParser()

    # -------- BASIC INPUTS --------
    parser.add_argument("--driven_audio", default='./examples/driven_audio/bus_chinese.wav')
    parser.add_argument("--source_image", default='./examples/source_image/full_body_1.png')
    parser.add_argument("--ref_eyeblink", default=None)
    parser.add_argument("--ref_pose", default=None)
    parser.add_argument("--checkpoint_dir", default='./checkpoints')
    parser.add_argument("--result_dir", default='./results')

    # -------- MODEL/GENERATION SETTINGS --------
    parser.add_argument("--pose_style", type=int, default=0)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--expression_scale", type=float, default=1.)
    parser.add_argument("--input_yaw", nargs='+', type=int, default=None)
    parser.add_argument("--input_pitch", nargs='+', type=int, default=None)
    parser.add_argument("--input_roll", nargs='+', type=int, default=None)
    parser.add_argument("--enhancer", type=str, default=None)
    parser.add_argument("--background_enhancer", type=str, default=None)
    parser.add_argument("--cpu", dest="cpu", action="store_true")
    parser.add_argument("--face3dvis", action="store_true")
    parser.add_argument("--still", action="store_true")
    parser.add_argument("--preprocess", default='crop',
                        choices=['crop', 'extcrop', 'resize', 'full', 'extfull'])
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--old_version", action="store_true")

    # -------- LEGACY/COMPATIBILITY OPTIONS --------
    parser.add_argument('--net_recon', type=str, default='resnet50',
                        choices=['resnet18', 'resnet34', 'resnet50'])
    parser.add_argument('--init_path', type=str, default=None)
    parser.add_argument('--use_last_fc', default=False)
    parser.add_argument('--bfm_folder', type=str, default='./checkpoints/BFM_Fitting/')
    parser.add_argument('--bfm_model', type=str, default='BFM_model_front.mat')

    # -------- RENDERING PARAMETERS --------
    parser.add_argument('--focal', type=float, default=1015.)
    parser.add_argument('--center', type=float, default=112.)
    parser.add_argument('--camera_d', type=float, default=10.)
    parser.add_argument('--z_near', type=float, default=5.)
    parser.add_argument('--z_far', type=float, default=15.)

    # -------- PARSE AND EXECUTE --------
    args = parser.parse_args()

    # -------- DEVICE AUTO-SELECT --------
    if torch.cuda.is_available() and not args.cpu:
        args.device = "cuda"
    else:
        args.device = "cpu"

    # -------- RUN MAIN FUNCTION --------
    main(args)
# ======================================================================
