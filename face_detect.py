import cv2
import sys
from PIL import Image
import urllib2
import io
from random import randint
from bs4 import BeautifulSoup


def resize_im(fname, dst_w, dst_h):
	img = cv2.imread(fname)
	height, width, channel = img.shape
	#print img.shape
	
	hfactor = float(dst_h) / height * 1.15
	wfactor = float(dst_w) / width * 1.15
	#print "width" + str(hfactor)
	#print "height" + str(wfactor)
	if width < height:
		res = cv2.resize(img, None, fx = wfactor, fy = wfactor, interpolation = cv2.INTER_CUBIC)
	else:
		res = cv2.resize(img, None, fx = hfactor, fy = hfactor, interpolation = cv2.INTER_CUBIC)
	#print res.shape
	return res

animal_list = ["rabbit_face.png","tiger.png","lion.png","giraffe.png","donkey_headnbg.png","minnie.png","mickey.png","horse.jpg"]
# Get user supplied values
imagePath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)


def random_resized_animal(img, x, y, w, h):
	i = randint(0,7)

	head_image = 'head_img/' + animal_list[i]

	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
	resized_animal = resize_im(head_image, w, h)
	return resized_animal;


def change_face(image):
	# Read the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.15,
	    minNeighbors=7,
	    minSize=(30, 30),
	    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	print "Found {0} faces!".format(len(faces))

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:

	   	resized_animal = random_resized_animal(image, x, y, w, h)
	    #replace the area of the face to the ball
		dh, dw, c = resized_animal.shape
		#print res.shape
		while y+h-dh < 0:
			resized_animal = random_resized_animal(image, x, y, w, h)
			dh, dw, c = resized_animal.shape
		
		image[y+(h-dh) : y+(h-dh)+dh, x: x +dw] = resized_animal
	return image

	#cv2.imshow("Faces found", image)
	#cv2.waitKey(0)

def process_image(image_url):
	fd = urllib2.urlopen(image_url)
	image_file = io.BytesIO(fd.read())
	image = Image.open(image_file)
	new_image = change_face(image)
	return new_image

def process_web(web_url):
	page = BeautifulSoup(urllib2.urlopen(web_url))
    all_img = page.findAll('img')
    src_list = []
    for img_link in all_img:
        src_list.append(img_link['src'])
    new_image_list = []
    for img_url in src_list:
    	new_image_list.append(process_image(image_url))
    # Now new_image_list consists of modified images of 
    # the type Image in PIL lib. 
    for i in range(len(new_image_list)):
    	new_image_list[i].save(str(i)+".jpg", "JPEG")
    
    	






