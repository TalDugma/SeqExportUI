import os
import sys
import shlex
from subprocess import Popen, CREATE_NEW_CONSOLE, PIPE, STDOUT
from multiprocessing.dummy import Pool  # thread pool
import argparse

CAM_DIR ='D:\\Video'
CUDA_ID = {0: '196608', 1: '196609'}
CLEXPORT_PATH = 'C:\\Program Files\\NorPix\\BatchProcessor\\CLExport.exe'
EXPORTED_SEQ = 'exported_sequences.txt'

def get_lines(process):
    return process.communicate()[0].splitlines()


def get_nearest_date(date, pivot):
    return min(date, key=lambda x: abs(x - pivot))


def write_to_file(file, seq):
    with open(file, 'a+') as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0:
            f.write("\n")
        f.write(seq)


def get_seq_path(seq_dir, seq):
    for file in os.listdir(seq_dir):
        full_path = os.path.join(seq_dir, file)
        if os.path.isfile(full_path) and file.startswith(seq) and file.endswith('.seq'):
            return full_path


def main(input_files, dest_folder):
    seq_to_cam = {}
    cameras_paths = [os.path.join(CAM_DIR, cam) for cam in os.listdir(CAM_DIR)]
    #create a dictionary of cameras enumerated from 0
    cam_dict =  {i:cam for i, cam in enumerate(cameras_paths)}
    for cam, cam_dir in cam_dict.items():

        file_list = [f[:19] for f in os.listdir(cam_dir) if f.endswith('.seq')]
        for seq in file_list:
            if seq not in seq_to_cam:
                seq_to_cam[seq] = [cam]
            else:
                seq_to_cam[seq].append(cam)
    print(seq_to_cam)

    with open(EXPORTED_SEQ, 'r') as f:
        previously_exported = set([line.rstrip() for line in f])

    seq_list = [os.path.splitext(os.path.basename(seq))[0] for seq in input_files]
    seq_list = [seq for seq in seq_list if seq in seq_to_cam.keys()]
    seq_list = sorted(seq_list, reverse=True)

    print(f'Sequences to export: {seq_list}')

    for seq in seq_list:
        export_path = os.path.join(dest_folder, seq)
        if not os.path.exists(export_path):
            os.mkdir(export_path)
        commands = []
        for cam in seq_to_cam[seq]:
            seq_path = get_seq_path(cam_dict[cam], seq)
            cam_path = os.path.join(export_path, f'cam{cam}')
            if not os.path.exists(cam_path):
                os.mkdir(cam_path)
            full_export_path = os.path.join(cam_path, f"{seq}.avi")
            exported_name = f'{seq}_cam{cam}'
            print(exported_name)
            cmd = f'''"{CLEXPORT_PATH}" -i "{seq_path}" -o "{cam_path}" -of cam_{cam} -f mp4'''
            commands.append(cmd)
          
        procs_list = [Popen(shlex.split(cmd), universal_newlines=True, creationflags=CREATE_NEW_CONSOLE) for cmd in commands]
        exitcodes = [p.wait() for p in procs_list]
        write_to_file(EXPORTED_SEQ, seq)
        print(f"{seq} export complete")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Export .seq files to the desired output folder.")
    parser.add_argument("input_files", nargs='+', help="List of .seq files to be exported.")
    parser.add_argument("output_folder", help="Folder to export the .avi files to.")

    args = parser.parse_args()
    main(args.input_files, args.output_folder)
