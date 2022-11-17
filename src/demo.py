import time, os
from threading import Thread

import pseye_sound_inference as psi
import webcam_person_detection_pseye as wpdp
from pseye_channel_filter import return_loudest_channel as rlc

# PlayStation Eye Sound Inference class to be used with threading

class pseye_sound_inference(Thread):
    def run(self):
        psi.main()

# PlayStation Eye Webcam Person Detection class to be used with threading
class pseye_webcam_person_detection(Thread):
    def run(self):
        wpdp.main()

if __name__ == '__main__':
    buffer = [0 for i in range(110)]

    pseye_sound_inference = Thread(target=psi.main, args=(buffer,))
    pseye_sound_inference.start()
    wpdp.main(buffer)
    # psi.main()