from pseyepy import Camera, Display

cam = Camera()
display = Display(cam)

frame, timestamp = cam.read()

cam.end()

# only tests camera output
