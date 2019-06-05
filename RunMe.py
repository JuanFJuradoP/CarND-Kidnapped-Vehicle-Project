import matplotlib.patches as mpatches
from multiprocessing import Pool 
import matplotlib.pyplot as plt
import subprocess
import csv
import os

def run_process(process):                                                             
    os.system('{}'.format(process)) 

def getClipboardData():
    p = subprocess.Popen(['xclip','-selection', 'clipboard', '-o'], 
        stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data

def setClipboardData(data):
    p = subprocess.Popen(['xclip','-selection','clipboard'], 
        stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

def main():

    # Copy command to clipboard to Create Video from desktop
    video_name = "particle_filter_test.mp4"
    command = "ffmpeg -video_size {}x{} -framerate {} -f x11grab -i :0.0+100,200 {}".format(
        1200, 850, 30, os.path.join(os.getcwd(), "video_results", video_name))
    setClipboardData(command.encode())

    # Run subprocess
    try:

        if not os.path.isdir("build"):
            os.mkdir("build")
            os.system('cd build && cmake .. && make') 
        else:
            os.system('clear && cd build && make') 

        processes = (
            "\{}".format(os.path.join(os.getcwd(), "term2_sim_linux", "term2_sim.x86_64")),
            "\cd {} && ./{}".format(os.path.join(os.getcwd(), "build"), "particle_filter")
        )

        # Run simulator and socket
        pool = Pool(processes=len(processes))                                                        
        pool.map(run_process, processes)
    except Exception as e: 
        print(str(e))

    print("Process has finished")

if __name__=="__main__":

    # Run all
    main()