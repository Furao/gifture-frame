#!/usr/bin/python3
import subprocess
import time
import rpyc
from rpyc.utils.server import ThreadedServer
import threading

class AnimateService(rpyc.Service):
    class exposed_Animator(object):
        def __init__(self):
            self.settings = Settings([],5.0)
            self.lock = threading.Lock()
            self.thread = threading.Thread(target = self.animate_loop)
            self.thread.start()

        def exposed_play_gifs(self, gifs, play_time):
            self.lock.acquire()
            self.settings.gifs = [x for x in gifs]
            self.settings.play_time = play_time
            self.settings.playing = True
            self.settings.updated = True
            self.lock.release()

        def exposed_stop_gifs(self):
            self.lock.acquire()
            self.settings.playing = False
            self.settings.updated = True
            if self.settings.p:
                self.settings.p.kill()
                self.settings.p = None
            self.lock.release()

        def animate_loop(self):
            idx = 0
            p = None
            # splash_args = ['display','-backdrop','-background','black','-borderwidth','0','frame_title.png']

            # args = ['animate','-backdrop','-borderwidth','0','-background','black', 'gif']
            args = ['animate','-borderwidth','0','-background','black', 'gif']

            while(1):
                time.sleep(0.5)
                self.lock.acquire()
                if self.settings.updated:
                    idx = 0
                    self.settings.updated = False
                if self.settings.playing:
                    if self.settings.p:
                        self.settings.p.kill()
                        self.settings.p = None
                    args[5] = self.settings.gifs[idx]
                    self.settings.p = subprocess.Popen(args)
                    idx = (idx + 1) % len(self.settings.gifs)
                    play_time = self.settings.play_time
                    self.lock.release()
                    time.sleep(play_time)
                    self.lock.acquire()
                self.lock.release()


class Settings():
    def __init__(self, gifs, play_time):
        self.playing = False
        self.gifs = gifs
        self.play_time = play_time
        self.updated = False
        self.p = None

    def __repr__(self):
        return 'gifs: {} play_time: {} playing: {} udpated {}'.format(self.gifs, self.play_time, self.playing, self.updated)

if __name__ == "__main__":
    t = ThreadedServer(AnimateService(), port = 18888)
    t.start()