#!/usr/bin/python3
from pprint import pprint
import sys
import time

# linuxpy open UVC device
#
from linuxpy.video.device import Device, MenuControl, VideoCapture, BufferType


options_default = {
        "photo":[1920,1080],
        "color":["YUYV","JPEG",False],
        "crop":[],
        "settle_frames":30
}

def get_photo(output="photo.jpg", uvc_id=0, options = {}, uvc_options={}):
        cam = Device.from_id(uvc_id)
        cam.open()

        options = options_default | options

        print(cam.info.formats)

        for ctrl in cam.controls.values():
                print(ctrl)
        if isinstance(ctrl, MenuControl):
                for (index, name) in ctrl.items():
                        print(f" - {index}: {name}")

        # set camera data format
        capture = VideoCapture(cam)
        capture.set_format(options["photo"][0], options["photo"][1], options["color"][0]) # Maybe figure out later
        cam.open()
        for uvc_option,value in uvc_options.items():
                cam.controls[uvc_option].value=value
        time.sleep(3)


        #
        # get frame from camera
        img = None
        for i, frame in enumerate(cam):
                print(f"frame #{i}: {len(frame)} bytes")
                if i > options["settle_frames"]:
                        img = frame
                        break
        #
        # extract raw data from frame
        raw_yuv = list(img.data)
        if options["color"][2]:
                hold = None
                for i in range(0,len(raw_yuv),2):
                        hold = raw_yuv[i]
                        raw_yuv[i] = raw_yuv[i+1]
                        raw_yuv[i+1] = hold

        data = bytes(raw_yuv)
        pprint(img)
        #

        # create wand image from raw data with format
        from wand.image import Image

        with Image(blob=data, format=options["color"][1],width=options["photo"][0],height=options["photo"][1],depth=8,colorspace="yuv") as image:
                print(image.format)
                if options["crop"] == []:
                        print("Not Cropping")
                elif len(options["crop"]) == 2:
                        image.crop(left=int(options["photo"][0]/2-options["crop"][0]/2), top=int(options["photo"][1]/2-options["crop"][1]/2), width=int(options["crop"][0]), height=int(options["crop"][1]))
                elif len(options["crop"]) == 4:
                        image.crop(left=options["crop"][0], top=options["crop"][1], width=options["crop"][2], height=options["crop"][3])

                #image.crop(left=420, top=0, width=1080, height=1080)
                image.save(filename=output)

        cam.close()


if __name__ == '__main__':
        get_photo(uvc_options={"sharpness":0})
