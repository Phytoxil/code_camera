import sensor, image, time, lcd ,pyb
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
lcd.init()
day_thresholds = [(20,60)]
night_thresholds = [(20, 40)]
tab = []
mice = []
LINE1_x1 = 60
LINE1_y1 = 20
LINE1_x2 = 60
LINE1_y2 = 75
LINE2_x1 = 120
LINE2_y1 = 20
LINE2_x2 = 120
LINE2_y2 = 75
p_right = pyb.Pin("P5", pyb.Pin.IN)
p_left = pyb.Pin("P6", pyb.Pin.IN)
rect_x = 0
rect_y = 20
rect_w = 160
rect_h = 60
direction : str = "None"
cx =0
cy =0
mouse_info = {
    "centroid": f"({cx}, {cy})",
    "movement_direction": "None",
    "beam": "None"
}
while(True):
    pin_value_right = p_right.value()
    pin_value_left = p_left.value()
    mouse_info["beam"] = "None"
    if pin_value_right == 0:
        mouse_info["beam"] = "Right"
    #if pin_value_left == 0:
    #    mouse_info["beam"] = "Left"

    img = sensor.snapshot().lens_corr(strength = 1.5 )
    light_condition = img.get_pixel(8,3)
    #img.draw_line(LINE1_x1,LINE1_y1 ,LINE1_x2, LINE1_y2)
    #img.draw_line(LINE2_x1,LINE2_y1 ,LINE2_x2, LINE2_y2)
    if light_condition <= 100:
        thld = night_thresholds
    else:
        thld = day_thresholds
    blobs = img.find_blobs(thld, pixels_threshold=200, area_threshold=200)
    mice.clear()
    tab.clear()
    if blobs:
        blobs.sort(key=lambda b: b.area(), reverse=True)
        for blob in blobs:
            cx, cy = blob.cx(), blob.cy()
            mouse_info["centroid"] = f"({cx},{cy})"
#            mouse_info = {
#                "centroid": f"({cx}, {cy})",
#                "movement_direction": "None",
#                "state": "None"
#            }
            if rect_x <= cx <= rect_x + rect_w and rect_y <= cy <= rect_y + rect_h :
                img.draw_cross(cx, cy, size=5, thickness=1)
                img.draw_rectangle(blob.rect(), color=(255, 255, 255))
                mouse_info["movement_direction"] = "Center"
                if cx < LINE1_x1:
                    direction = "Left"
                    mouse_info["movement_direction"] = "Left"
                if cx > LINE2_x1:
                    direction = "Right"
                    mouse_info["movement_direction"] = "Right"


                mice.append(mouse_info)
                tab.append(mouse_info)

                var = str(tab).replace("\'", "\"")
                print(var)
    for idx, mouse_info in enumerate(mice):
        display_str = "Mouse {}: {}".format(idx + 1, mouse_info["beam"])
        img.draw_string(10, 10 + idx * 15, display_str, color=(0, 0, 0))
    lcd.display(img)
