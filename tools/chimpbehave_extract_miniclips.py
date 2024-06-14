import os
import cv2
import json
import csv

def load_annotations(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def create_mini_clips(csv_path, video_folder, json_folder, output_folder, clip_length=20, target_size=(224, 224)):
    with open(csv_path, newline='') as csvfile:
        # reader = csv.reader(csvfile, delimiter=';')
        reader = csv.reader(csvfile)
        next(reader)  # Optionally skip the header
        for row in reader:
            video_filename = row[0]
            activity = row[1]
            json_filename = video_filename.replace(".mp4", "_bboxes.json")
            video_path = os.path.join(video_folder, video_filename)
            json_path = os.path.join(json_folder, json_filename)

            annotations = load_annotations(json_path)
            process_video(video_path, annotations, output_folder, activity, clip_length, target_size)

def process_video(video_path, annotations, output_folder, activity, clip_length=20, target_size=(224, 224)):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Adjust the loop to only process full clips of exactly 20 frames
    for start_frame in range(0, total_frames - clip_length + 1, clip_length):
        end_frame = start_frame + clip_length - 1  # Ensures exactly 20 frames per clip
        output_path = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(video_path))[0]}_{activity}_clip_{start_frame}_{end_frame}.mp4')

        if os.path.exists(output_path):
            print(f'file {output_path} already exists, skipping..')
            continue  # Skip if the output file exists

        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), target_size)

        # Collect all bboxes for this clip
        all_bboxes = []
        for frame_idx in range(start_frame, end_frame + 1):
            frame_data = annotations[frame_idx]
            tracks = frame_data['track_bboxes'][0]
            bboxes = [track for track in tracks if track[0] == 0]  # Assuming individual_id 0
            all_bboxes.extend(bboxes)

        if not all_bboxes:
            print("No bounding boxes found for the clip, skipping...")
            out.release()
            continue

        # Calculate global min and max coordinates for all bounding boxes in the clip
        x_mins, y_mins, x_maxs, y_maxs = zip(*[(bbox[1], bbox[2], bbox[3], bbox[4]) for bbox in all_bboxes])
        global_x_min, global_y_min = min(x_mins), min(y_mins)
        global_x_max, global_y_max = max(x_maxs), max(y_maxs)

        # Define the size and center of the cropping area
        global_width = global_x_max - global_x_min
        global_height = global_y_max - global_y_min
        side_length = max(global_width, global_height, 224)  # Ensure at least 224 in size

        center_x = int((global_x_min + global_x_max) / 2)
        center_y = int((global_y_min + global_y_max) / 2)
        crop_x_min = int(max(0, center_x - side_length // 2))
        crop_x_max = int(min(cap.get(cv2.CAP_PROP_FRAME_WIDTH), center_x + side_length // 2))
        crop_y_min = int(max(0, center_y - side_length // 2))
        crop_y_max = int(min(cap.get(cv2.CAP_PROP_FRAME_HEIGHT), center_y + side_length // 2))

        # Process each frame in the clip
        for frame_idx in range(start_frame, end_frame + 1):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                continue

            cropped_frame = frame[crop_y_min:crop_y_max, crop_x_min:crop_x_max]
            if cropped_frame.size > 0:
                # Resize if necessary
                if cropped_frame.shape[0] > 224 or cropped_frame.shape[1] > 224:
                    cropped_frame = cv2.resize(cropped_frame, target_size)
                out.write(cropped_frame)
            else:
                print(f"Empty or invalid frame at frame index {frame_idx}, skipping.")

        out.release()

    cap.release()

        
csv_path = '../data/chimpbehave/labels.csv'
video_folder = '../data/chimpbehave/original'
json_folder = '../data/chimpbehave/bboxes'
output_folder = '../data/chimpbehave/miniclips'
create_mini_clips(csv_path, video_folder, json_folder, output_folder)
