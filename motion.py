import cv2

static_back = None #Background picture
previous_area = 0 #Background change area for previous frame
static_count = 0 #Count background chage that remains the same

# Capturing video 
video = cv2.VideoCapture(0) 

# Function for detecting motion through camera
def detectMotion(debug=False):
    global static_back
    global previous_area
    global static_count
    
    # Reading frame(image) from video 
    _, frame = video.read()

    # Reduce size to improve framerate
    width = int(frame.shape[1] * .5)
    height = int(frame.shape[0] * .5)
    frame = cv2.resize(frame, (width,height))

    # Initializing motion
    # 0: no motion
    # 1: motion detected
    motion = 0

    # Converting color image to gray_scale image 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

    # Converting gray scale image to GaussianBlur 
    # so that change can be found easily 
    gray = cv2.GaussianBlur(gray, (21, 21), 0) 

    # In first iteration we assign the value 
    # of static_back to our first frame 
    if static_back is None: 
        static_back = gray 
        return motion

    # Difference between static background 
    # and current frame(which is GaussianBlur) 
    diff_frame = cv2.absdiff(static_back, gray) 

    # If change in between static background and 
    # current frame is greater than 30 it will show white color(255) 
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 3) 

    # Finding contour of moving object 
    cnts,_ = cv2.findContours(thresh_frame.copy(), 
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
    sum_area = 0 #Total area of background change
    for contour in cnts:
        area = cv2.contourArea(contour)
        sum_area = sum_area + area
        if area < 5000: #Ignore background change that is too small
            continue
        motion = 1 #Something moved

        if debug:
            # Show bounding rectangle of moving object
            (x, y, w, h) = cv2.boundingRect(contour) 
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Check if the background change is the same
    if sum_area > 5000 \
       and sum_area >= previous_area*0.95 \
       and sum_area <= previous_area*1.05:
            
        static_count += 1
        if static_count == 25: #Background change is permanent
            static_back = gray #Update background to current frame
    
    else: #Different background change
        previous_area = sum_area
        static_count = 0

    # Display results
    if debug:
        #cv2.imshow("Gray Frame", gray)
        #cv2.imshow("Difference Frame", diff_frame)
        cv2.imshow("Threshold Frame", thresh_frame)
        cv2.imshow("Color Frame", frame)

    cv2.waitKey(100) #Reduce stress on CPU
    return motion

