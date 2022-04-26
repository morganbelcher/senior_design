from imutils.video import VideoStream
from imutils.video import FPS
import cv2
import face_recognition
import imutils
import os
import datetime
import csv
import pandas as pd
import pickle
import time

abspath = os.path.dirname(os.path.abspath(__file__)) + "/"
#Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"

#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0,framerate=10).start()

# Create column headers
attLog = {
    "Name": [],
    "Attendance Time": [],
    "Date": [],
	"Recognition Time":[]
}

#Creating Dataframe 
attLogDF = pd.DataFrame(attLog)

time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# Initial point of timing
	initTime = time.time()
	# grab the frame from the threaded video stream and resize it
	# to 500px (to speedup processing)
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	# Detect the fce boxes
	boxes = face_recognition.face_locations(frame)
	# compute the facial embeddings for each face bounding box
	encodings = face_recognition.face_encodings(frame, boxes)
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown" #if face is not recognized, then print Unknown

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)

			#Current Date and Time Data
			currentTime = datetime.datetime.now()
			ts = currentTime.strftime("%H:%M:%S")
			day = datetime.date.today()

			#Final Recognition Time
			finTime = time.time()

			#Calculate time difference
			deltTime = finTime - initTime

			#Creating a temporary dataset for a recognized face
			tempData = {
        		"Name": [name],
        		"Attendance Time": [ts],
        		"Date": [day],
				"Recognition Time":[deltTime]
    			}
			tempDF = pd.DataFrame(tempData)

			#logging names
			attLogDF = pd.concat([attLogDF, tempDF])

			#If someone in your dataset is identified, print their name on the screen
			if currentname != name:
				currentname = name
				print(currentname)

		# update the list of names
		names.append(name)

	# loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image - color is in BGR
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 225), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			.8, (0, 255, 255), 2)

	# display the image to our screen
	cv2.imshow("Facial Recognition is Running", frame)
	key = cv2.waitKey(1) & 0xFF

	# quit when 'q' key is pressed
	if key == ord("q"):
		print(attLogDF)
		# Reorders the columns (this my not be needed but for some reason in testing the column order would get mirrored)
		attLogDF = attLogDF.reindex(columns=['Name', 'Recognition Time', 'Attendance Time', 'Date'])
		# Deletes duplicate names (Im pretty sure well want to have the sorting done in another script)
		#attLogDF = attLogDF.drop_duplicates(subset=['Name'], keep='first')
		# Sorts the name column by alphabetical order to change to sorting based on time change attLogDF.columns[1]	
		attLogDF.sort_values(attLogDF.columns[1],axis=0,inplace=True)
		# Prints data out to the CSV file
		attLogDF.to_csv(abspath + 'FaceReqData.csv', index=False)
		attLogDF.to_csv(abspath + "flaskserve/" + 'FaceReqData.csv', index=False)
		
		time.sleep(2)
		break

	# update the FPS counter
	fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
