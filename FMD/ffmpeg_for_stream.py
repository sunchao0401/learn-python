#!/root/.pyenv/shims/python
# sunchao
# 2017 07 07

import os
import time
import sys
import subprocess
import signal
import json

script, *args = sys.argv
pid = os.getpid()
log_file = "/cache/logs/err_log/ffmpeg_for_stream.log"

if isinstance(args,tuple):
    args = list(args)

local_ip = args.pop(0)
tcurl = args.pop(0)
app = args.pop(0)
name = args.pop(0)
transcode_args = args.copy()

ffmpeg_path = "/usr/local/sbin/ffmpeg -re -i \"rtmp://{0}/{1}/{2} tcUrl={3}\"".format(local_ip,app,name,tcurl)

class stream():

    def __init__(self,ip,app,name,tcurl):
        self.ffprobe = "/usr/local/sbin/ffprobe -i \"rtmp://{0}/{1}/{2} tcurl={3}\" -show_streams -print_format json 2> /dev/null".format(ip,app,name,tcurl)
        self.info = os.popen(self.ffprobe).read()
        self.v = []
        self.a = False

    def video(self):
        ret = json.loads(self.info)["streams"]
        for i in range(0,len(ret)):
            if ret[i]["codec_type"] == "video":
                # 码率不存在或者是0，取无穷大
                try:
                    if ret[i]["bit_rate"] and ret[i]["bit_rate"] != "0":
                        self.v.append(int(ret[i]["bit_rate"]))
                    else:
                        self.v.append(float("inf"))
                except:
                        self.v.append(float("inf"))
                if ret[i]["avg_frame_rate"]:
                    self.v.append(int(ret[i]["avg_frame_rate"].split('/')[0]))
                else:
                    self.v.append(float("inf"))
                if ret[i]["coded_width"]:
                    self.v.append(int(ret[i]["coded_width"]))
                else:
                    self.v.append(float("inf"))
            if ret[i]["codec_type"] == "audio":
                if ret[i]["codec_name"] == "aac" or ret[i]["codec_name"] == "mp3":
                    self.a = True

    def audio(self):
        if self.v:
            return False
        else:
            return True

def log_format(res):
    ret = time.ctime() + ' ' + str(pid) + ' ' + tcurl + ' ' + app + ' ' + name + ' ' + res + ' ' + str(transcode_args) + '\n'
    with open(log_file,"a") as f:
        f.write(ret)

def kill_ffmpeg(SIG,stack):
    os.kill(chaild.pid,signal.SIGKILL)
    log_format("FMD kill ffmpeg {0}".format(chaild.pid))

if len(args)%4 != 0:
    res = "transcode args not complete"
    log_format(res)
    exit(1)

if len(args) == 0:
    res = "no args need args"
    log_format(res)
    exit(2)

log_format("start run this sript")

streaming = stream(local_ip,app,name,tcurl)
streaming.video()

if streaming.audio():
    while args:
        if streaming.a:
            mark = "-map 0 -c copy -f flv \"rtmp://{3}:1835/{4}/{5} tcUrl={6}\"".format(args[0], args[1], args[2], local_ip, app, args[3], tcurl)
        else:
            mark = "-map 0 -acodec libfaac -f flv \"rtmp://{3}:1835/{4}/{5} tcUrl={6}\"".format(args[0], args[1], args[2], local_ip, app, args[3], tcurl)

        for i in range(0,4):
            args.pop(0)
        ffmpeg_path = ffmpeg_path + " " + mark
else:
    while args:
        if int(args[0])*1000 >= streaming.v[0]:
            mark = "-map 0 -c copy -f flv \"rtmp://{3}:1835/{4}/{5} tcUrl={6}\"".format(args[0], args[1], args[2], local_ip, app, args[3], tcurl)
        else:
            if int(args[1]) == -1:
                args[1] = "30"

            if int(args[1]) > streaming.v[1]:
                    args[1] = str(streaming.v[1])

            if args[2]:
                if int(args[2].split("x")[0]) > streaming.v[2]:
                    args[2] = str(streaming.v[2])
                else:
                    args[2] = args[2].split("x")[0]
            else:
                args[2] = str(streaming.v[2])

            if not streaming.a:
                mark = "-map 0 -acodec libfaac -vcodec libx264 -b:v {0}k -r {1} -vf scale=\"{2}:trunc(ow/a/2)*2\" -f flv \"rtmp://{3}:1835/{4}/{5} tcUrl={6}\"".format(args[0], args[1], args[2], local_ip, app, args[3], tcurl)
            else:
                mark = "-map 0 -c:a copy -c:v libx264 -b:v {0}k -r {1} -vf scale=\"{2}:trunc(ow/a/2)*2\" -f flv \"rtmp://{3}:1835/{4}/{5} tcUrl={6}\"".format(args[0], args[1], args[2], local_ip, app, args[3], tcurl)

        for i in range(0,4):
            args.pop(0)
        ffmpeg_path = ffmpeg_path + " " + mark

log_format("transcode start to run")
chaild = subprocess.Popen(ffmpeg_path, shell=True)
signal.signal(signal.SIGTERM,kill_ffmpeg)
chaild.wait()
log_format("transcode stop returncode {0}".format(chaild.returncode))
