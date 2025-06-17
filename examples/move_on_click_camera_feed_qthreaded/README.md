## Any questions, contact me on christian.orr@diamond.ac.uk

I am developing a Qt GUI for a laser shaping system I've built at Diamond. A core component of this is a video feed from an On-Axis Viewing system (OAV). To allow the user to position thier sample where the laser is also centered, I implemented a move-on-click function. To allow the video to update in the background without blocking other components on the GUI, I have put it in a Qthread which emits images to the GUI after doing some conditioning and drawing. In addition to the move-on-click, I have implemented a 'draw-on-click' mode which allows the user to mark areas to be cut with the laser by clicking the video feed. Example images are in this folder. 

# The repo for the GUI is here: https://github.com/DiamondLightSource/aithre

# The code for the QThread, with comments on what each bit is doing:

'''

    class OAVThread(QtCore.QThread):
        ImageUpdate = QtCore.pyqtSignal(QtGui.QImage) # to emit the image to a widget on the GUI
    
        def __init__(self):
            super(OAVThread, self).__init__()
            self.ThreadActive = False
            self.zoomLevel = 1 # can change the digital zoom on the GUI, so need a way to account for this when drawing crosshairs etc.
            self.beamX = beamX
            self.beamY = beamY
            self.line_width = line_width
            self.line_spacing = line_spacing
            self.line_color = line_color
    
        def run(self):
            self.ThreadActive = True
            self.cap = cv.VideoCapture(OAVADDRESS)
            while self.ThreadActive:
                ret, frame = self.cap.read()
                if self.ThreadActive and ret:
                    for i in range(beamX % line_spacing, frame.shape[1], line_spacing):
                        cv.line(frame, (i, 0), (i, frame.shape[0]), line_color, line_width)
                    for i in range(beamY % line_spacing, frame.shape[0], line_spacing):
                        cv.line(frame, (0, i), (frame.shape[1], i), line_color, line_width)
                    # this is drawing a crosshair where the laser beam centre is
    
                    cv.line(
                        frame,
                        (beamX - 20, beamY),  # bigness
                        (beamX + 20, beamY),
                        (0, 255, 0),  # color
                        3,  # thickness
                    )
                    cv.line(
                        frame,
                        (beamX, beamY - 20),
                        (beamX, beamY + 20),
                        (0, 255, 0),
                        3,
                    )
    
                    if self.zoomLevel != 1: # this handles changes in the digital zoom level
                        new_width = int(frame.shape[1] / self.zoomLevel)
                        new_height = int(frame.shape[0] / self.zoomLevel)
    
                        x1 = max(self.beamX - new_width // 2, 0)
                        y1 = max(self.beamY - new_height // 2, 0)
                        x2 = min(self.beamX + new_width // 2, frame.shape[1])
                        y2 = min(self.beamY + new_height // 2, frame.shape[0])
    
                        x1, x2 = self.adjust_roi_boundaries(
                            x1, x2, frame.shape[1], new_width
                        )
                        y1, y2 = self.adjust_roi_boundaries(
                            y1, y2, frame.shape[0], new_height
                        )
    
                        cropped_frame = frame[y1:y2, x1:x2]
    
                        frame = cv.resize(cropped_frame, (frame.shape[1], frame.shape[0]))
    
                    rgbImage = cv.cvtColor(
                        frame, cv.COLOR_BGR2RGB
                    )  
                    convertToQtFormat = QtGui.QImage(
                        rgbImage.data,
                        rgbImage.shape[1],
                        rgbImage.shape[0],
                        QtGui.QImage.Format_RGB888,
                    )
                    p = convertToQtFormat
                    p = convertToQtFormat.scaled(
                        display_width, display_height, QtCore.Qt.KeepAspectRatio
                    ) 
                    self.ImageUpdate.emit(p)
    
        def adjust_roi_boundaries(self, start, end, max_value, window_size):
            if start < 0:
                end -= start
                start = 0
            if end > max_value:
                start -= end - max_value
                end = max_value
            if (end - start) < window_size and (start + window_size) <= max_value:
                end = start + window_size
            return start, end
    
        def setZoomLevel(self, zoomLevel):
            self.zoomLevel = zoomLevel 
    
        def stop(self):
            self.ThreadActive = False
            self.cap.release()
'''

# canvas and move mode for drawing on the feed or moving motors

'''

    # this is connected to a radio button to move between the two modes
    
    def toggleCanvasMode(self, mode):
        if mode == "move":
            self.canvasMode = "move"
        elif mode == "draw":
            self.canvasMode = "draw"
        else:
            self.canvasMode = "move"

    def onMouse(self, event):
        if self.canvasMode == "move":
            self.zoomclickcal = int(self.ui.sliderZoom.value())
            if self.zoomclickcal == 1:
                self.xcent = beamX
                self.ycent = beamY
            else:
                self.xcent = 2012
                self.ycent = 1518
            x = event.pos().x()
            x = x * feed_display_ratio
            y = event.pos().y()
            y = y * feed_display_ratio
            x_curr = float(ca.caget(pv.stage_x_rbv))
            #print(x_curr)
            y_curr = float(ca.caget(pv.gonio_y_rbv))
            z_curr = float(ca.caget(pv.gonio_z_rbv))
            omega = float(ca.caget(pv.omega_rbv))
            print("Clicked", x, y)
            Xmove = x_curr - ((x - self.xcent) * (calibrate / self.zoomclickcal))
            Ymove = y_curr + (math.sin(math.radians(omega)) * ((y - self.ycent) * (calibrate / self.zoomclickcal)))
            Zmove = z_curr + (math.cos(math.radians(omega)) * ((y - self.ycent) * (calibrate / self.zoomclickcal)))
            print("Moving", Xmove, Ymove, Zmove)
            ca.caput(pv.stage_x, round(Xmove, 4))
            ca.caput(pv.gonio_y, round(Ymove, 4))
            ca.caput(pv.gonio_z, round(Zmove, 4))
        elif self.canvasMode == "draw":
            self.drawn_points.append(event.pos())
            self.redrawPoints()
        else:
            pass
        
    def redrawPoints(self):
        if self.image is not None:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 5))
            if len(self.drawn_points) < 2:
                for point in self.drawn_points:
                    painter.drawPoint(point)
            if len(self.drawn_points) > 1:
                for i in range(len(self.drawn_points) - 1):
                    painter.drawLine(self.drawn_points[i], self.drawn_points[i + 1])
            painter.end()
            self.ui.oav_stream.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def savePoints(self):
        points_list = []
        now = datetime.now()
        filename = now.strftime("%Y%m%d_%H%M%S_points.txt")
        for i, point in enumerate(self.drawn_points):
            correctedX = round((point.x() * calibrate), 4)
            correctedY = round((point.y() * calibrate), 4)
            if i == 0:
                points_list.append((correctedX, correctedY, False))
            else:
                points_list.append((correctedX, correctedY, True))
        
        if points_list:
            with open(filename, 'w') as file:
                for point in points_list:
                    file.write(f"{point[0]}, {point[1]}, {point[2]}\n")
            self.points_list = points_list * self.ui.spinBoxRepetitions.value()
            print(points_list)
        else:
            print("No shapes to cut...")
'''

