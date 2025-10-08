# Real-Time-Object-Detector
# 📖 Overview
This project performs real-time recognition of geometric shapes using a live camera feed and displays information about these shapes through a Tkinter-based GUI. It integrates computer vision (OpenCV) and graphical interaction to simulate an augmented reality (AR) experience — where users can visualize shape recognition live and learn about each detected shape.
This system forms the first step toward a larger AR-assisted design concept, such as smart glasses that can identify and provide context for shapes in the real world — useful for education, creative design, and engineering visualization.

#🧩 Features
Real-Time Detection
Detects and identifies shapes (circle, triangle, square, rectangle, pentagon, etc.) from a webcam feed.

Augmented Visualization
Highlights contours, counts edges, and labels shapes directly on the live video output.

Interactive GUI
Displays a simple startup menu and allows users to open shape-related Wikipedia pages.

Dynamic Parameter Control
Adjustable Canny edge thresholds and contour area using OpenCV trackbars for live tuning.

Multi-View Stacking
Shows different stages of processing (original, edge-detected, contour-drawn) on one screen using a custom stkimgs() function.

#🧠 Concept & Inspiration
This project addresses the challenge of automating geometric shape recognition — a fundamental part of computer vision and AR.
It serves as a foundation for developing assistive AR tools that can analyze visual input and provide users with context, feedback, or learning opportunities.

#🧾 Installation & Setup
Check out the requirements for running here
