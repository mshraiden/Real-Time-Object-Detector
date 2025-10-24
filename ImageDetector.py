import cv2  # OpenCV for image processing
import numpy as np  # Numpy for mathematical operations
import webbrowser  # To open web pages for shapes
import tkinter as tk  
import keyboard 
from tkinter import messagebox 
from stkimg import stkimgs  # Function to stack images

# Initialize camera dimensions
framewidth = 640
frameheight = 480


cap = cv2.VideoCapture(0)
cap.set(3, framewidth)  
cap.set(4, frameheight)  

#Empty function for trackbars
def empty(a):
    pass
#Create a trackbar window for dynamic parameter adjustment
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 51, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 94, 255, empty)
cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)

# Function for displaying the initial menu
def show_menu():
    root = tk.Tk()
    root.geometry("300x150")
    root.title("Shape Recognition Menu")

    def start_recognition():
        root.destroy()  # Close the menu

    # Callback function for "No" button
    def exit_program():
        root.destroy()  # Close the menu
        cap.release()  # Release the camera
        cv2.destroyAllWindows()  # Close all OpenCV windows
        exit()  # Exit the script


    label = tk.Label(root, text="Do you want to recognize shapes?", font=("Arial", 12))
    label.pack(pady=20)


    yes_button = tk.Button(root, text="Yes", command=start_recognition, font=("Arial", 10), width=10)
    yes_button.pack(side="left", padx=30)

    no_button = tk.Button(root, text="No", command=exit_program, font=("Arial", 10), width=10)
    no_button.pack(side="right", padx=30)

    root.mainloop()
    
# GUI function for displaying shape links
def display_output():
    if hasattr(display_output, 'window') and display_output.window.winfo_exists():
        return 

    display_output.window = tk.Tk()
    display_output.window.geometry("400x300")
    display_output.window.title("Shape Info")
    websites = {
        "Circle": "https://en.wikipedia.org/wiki/Circle",
        "Triangle": "https://en.wikipedia.org/wiki/Triangle",
        "Square": "https://en.wikipedia.org/wiki/Square",
        "Rectangle": "https://en.wikipedia.org/wiki/Rectangle",
        "Pentagon": "https://en.wikipedia.org/wiki/Pentagon",
    }

    # Add buttons dynamically based on shapes
    for shape_name, url in websites.items():
        btn = tk.Button(
            display_output.window,
            text=shape_name,
            command=lambda url=url: webbrowser.open(url),
            font=("Arial", 12),
            width=20,
            pady=5
        )
        btn.pack(pady=5)
    display_output.window.mainloop()
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to detect contours and identify shapes
def getcontours(img, imgcontour):
    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Error check: Skip processing if no contours are found
    if not contours:
        print("Warning: No contours found.")
        return

    cv2.drawContours(imgcontour, contours, -1, (255, 0, 255), 7)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        min_area = cv2.getTrackbarPos("Area", "Parameters")  # Adjustable minimum area
        
        if area > min_area:
            cv2.drawContours(imgcontour, cnt, -1, (255, 0, 255), 7)
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True) 
            sides = len(approx)  # Number of sides
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgcontour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            # Identifing the shape based on the number of sides
            if sides==3:
                cv2.putText(imgcontour, "Points: " + str(sides), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                cv2.putText(imgcontour, "Shape : Triangle ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            elif sides==4:
                cv2.putText(imgcontour, "Points: " + str(sides), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                asp_ratio = w/float(h)
                if asp_ratio>0.95 and asp_ratio<1.05: 
                    cv2.putText(imgcontour, "Shape : Square ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                else:
                    cv2.putText(imgcontour, "Shape : Rectangle ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            elif sides==5:
                cv2.putText(imgcontour, "Points: " + str(sides), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                cv2.putText(imgcontour, "Shape : Pentagon ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            elif sides==6:
                cv2.putText(imgcontour, "Points: " + str(sides), (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                cv2.putText(imgcontour, "Shape : Hexagon ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            else:
                cv2.putText(imgcontour, "Points: 0", (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
                cv2.putText(imgcontour, "Shape : Circle ", (x+w+20, y+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            keyboard.on_press_key('z', lambda _: display_output())
show_menu()

# Main loop for video capture and processing
while True:
    success, img = cap.read()
    imgcontour = img.copy()  
    blur = cv2.GaussianBlur(img, (7, 7), 1)
    grayimg = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    cannyimg = cv2.Canny(grayimg, threshold1, threshold2) 
    kernel = np.ones((5, 5))
    imgdil = cv2.dilate(cannyimg, kernel, iterations=1)  
    getcontours(imgdil, imgcontour)
    imgstack = stkimgs(0.8, ([img, cannyimg],[imgdil, imgcontour]))
    cv2.imshow("Result", imgstack)  # Display stacked images
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

