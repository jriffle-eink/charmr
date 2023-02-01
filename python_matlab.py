import matlab.engine
print("REAGLing images")
slideshow_List =  [r"C:\Users\jriffle\Documents\Demos\images_crystal\Landscape_examples", r"C:\Users\jriffle\Documents\Demos\images_crystal\Portrait_examples"]
eng = matlab.engine.start_matlab()
for i in range(len(slideshow_List)): 
    eng.python_REAGL(slideshow_List[i], nargout=0)
    print("REAGLed: " + slideshow_List[i].path)