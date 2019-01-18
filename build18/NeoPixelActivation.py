import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, 30)

#in this demo we are using only 4 neopixels
lenPixels = 4

def lightPixel(lst):
    #Change the limit/make it more robust in future versions
    if len(lst) > 4:
        return "Bad input"
    #we don't want indexes greater than the amount of lights we have
    for num in lst:
        if num >= 4:
            return "Bad input"
    #turn on lights in the input, turn off lights not in the input
    for light in pixels:
        if light in lst:
            pixels[light] = (0, 0, 100)
        else:
            pixels[light] = (0, 0, 0)
    return "Lights " + str(lst) + " are active"

def turnOffAllLights():
    for light in pixels:
        pixels[light] = (0, 0, 0)
    return "All lights are turned off"
