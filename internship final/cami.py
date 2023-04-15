import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract
import webbrowser
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Znmd@1234",
  database="books"
)
def have_common_substring(str1, str2):
    substrings1 = set(str1[i:j] for i in range(len(str1)) for j in range(i+1, len(str1)+1))
    substrings2 = set(str2[i:j] for i in range(len(str2)) for j in range(i+1, len(str2)+1))
    return bool(substrings1.intersection(substrings2))

mycursor = mydb.cursor()
mycursor.execute("SELECT name FROM products")
myresult = mycursor.fetchall()
# print(myresult)
# print(type(myresult))

net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

classes = []
with open("coco.names.txt", "r") as f:
    classes = f.read().splitlines()

class Video(object):
    def __init__(self):
    #     cv2.namedWindow("Camera", cv2.WND_PROP_FULLSCREEN)
    #     cv2.setWindowProperty("Camera", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        self.video=cv2.VideoCapture(0)
    def ans(self,text):
        if "MITIGATING" and "DEFICIENCIES" and "TECHNICAL" and "EDUCATION" in text:
            print("Book is of Cognifront Company \nBook Name: Mitigating Deficiencies of Technical Education\nBook Link:http://www.cognifront.com/iview.php?c=MDTE")
            webbrowser.open("http://www.cognifront.com/iview.php?c=MDTE")
            item= "Mitigating Deficiencies of Technical Education"
            mycursor.execute("SELECT * FROM products WHERE name = %s",[item])
            Answer=mycursor.fetchall()
            return Answer
        elif "FLUID" and "FLOW" and "SIMULATION" in text:
            print("Book is of Cognifront Company \nBook Name: Coding Mathematics : Fluid Flow Simulation\n Book Link:http://www.cognifront.com/iview.php?c=FFSIM")
            webbrowser.open("http://www.cognifront.com/iview.php?c=FFSIM")
            item= "Coding Mathematics : Fluid Flow Simulation"
            mycursor.execute("SELECT * FROM products WHERE name = %s",[item])
            Answer=mycursor.fetchall()
            return Answer
        elif "SYMBOTIC"and"RELATIONSHIP" in text:
            print("Book is of Cognifront Company \nBook Name: Symbiotic Relationship : Academia Industry Interaction\nBook Link:http://www.cognifront.com/iview.php?c=SRAII")
            webbrowser.open("http://www.cognifront.com/iview.php?c=SRAII")
            item= "Symbiotic Relationship : Academia Industry Interaction"
            mycursor.execute("SELECT * FROM products WHERE name = %s",[item])
            Answer=mycursor.fetchall()
            return Answer
                                    
        elif "GROOMING"and"ENGINEERS" in text:
            print("Book is of Cognifront Company \nBook Name: Grooming Engineers\nBook Link:http://www.cognifront.com/iview.php?c=GE")
            webbrowser.open("http://www.cognifront.com/iview.php?c=GE")
            item= "Grooming Engineers"
            mycursor.execute("SELECT * FROM products WHERE name = %s",[item])
            Answer=mycursor.fetchall()
            return Answer
                                    
        elif " IMPROVING"and "ENGINEERING"and"EDUCATION" in text:
            print("Book is of Cognifront Company \nBook Name:  Improving Engineering Education\nBook Link:http://www.cognifront.com/iview.php?c=GE")
            webbrowser.open("http://www.cognifront.com/iview.php?c=IEE")
            item= "Improving Engineering Education"
            mycursor.execute("SELECT * FROM products WHERE name = %s",[item])
            Answer=mycursor.fetchall()
            return Answer

                                    
        else :
            print("Recognize textfrom image : \n"+text)
            print("Book is of Another Company")
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        # cap = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_PLAIN
        colors = np.random.uniform(0, 255, size=(100, 3))
        
        while True:
            _, img = self.video.read()
            height, width, _ = img.shape

            blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
            net.setInput(blob)
            output_layers_names = net.getUnconnectedOutLayersNames()
            layerOutputs = net.forward(output_layers_names)

            boxes = []
            confidences = []
            class_ids = []
            # screen_width, screen_height = turtle.screensize()
            for output in layerOutputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.2:
                        center_x = int(detection[0]*width)
                        center_y = int(detection[1]*height)
                        w = int(detection[2]*width)
                        h = int(detection[3]*height)

                        x = int(center_x - w/2)
                        y = int(center_y - h/2)

                        boxes.append([x, y, w, h])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

            if len(indexes)>0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = str(round(confidences[i],2))
                    color = colors[i]
                    cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                    cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,255), 2)
                    if class_ids[i] ==73:
                        print("Book Detected")
                        ret, frame = self.video.read()
                        cv2.imwrite("webcam_image.png", frame)
                        # Defining paths to tesseract.exe
                        # and the image we would be using
                        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                        # image_path = r"E:\OD_model\webcam_image.png"

                        # Opening the image & storing it in an image object
                        img1 = Image.open("webcam_image.png")

                        # Providing the tesseract executable
                        # location to pytesseract library
                        pytesseract.tesseract_cmd = path_to_tesseract

                        # Passing the image object to image_to_string() function
                        # This function will extract the text from the image
                        global text
                        text=""
                        text = pytesseract.image_to_string(img1)
                        # text = text.replace('\n',' ').lower()
                        print(text)
                        # print(myresult)
                        # print(type(text))
                        # print(type(myresult))
                        
# loop over the course list and check if the search string is present in any of the tuples
                        # for tuple in myresult:
                        #     for item in tuple:
                        #         if text in str(item):
                        #             print("Search string found in tuple:", item)
                        #             sql_query = "SELECT price_inr FROM products WHERE name = %s"
                        #             mycursor.execute(sql_query, item)
                        #             mycursor.execute("SELECT price_inr FROM products WHERE name = ?"[item])
                        #             print(mycursor.fetchone())
                        #             break
                        #         else:
                        #             print("Search string not found in any tuple.")
                        # for course_tuple in myresult:
                        #     for i in ran:
                        #     # print(course_tuple[0])
                        #         if have_common_substring(course_tuple[i], text):
                        #             print("Search string found in tuple:", course_tuple[0])
                        #             sql_query = "SELECT price_inr FROM products WHERE name = %s"
                        #             mycursor.execute(sql_query, [course_tuple[0]])
                        #             # mycursor.execute("SELECT price_inr FROM products WHERE name = ?"[course_tuple[0]])
                        #             print(mycursor.fetchone())
                        #             #webbrowser.open("http://www.cognifront.com/iteachers.php#books")
                        #             break  # exit the loop if the search string is found
                        #         else:
                        #             print("Search string not found in any tuple.")
                        # print(text)
                        # words = text.split()
                        
                        # for row in myresult:
                        #     row1=row[0].upper()
                        #     words_list = row1.split()
                        #     if all(word in words for word in words_list):
                        #         print("Words found in array:", words_list)
                        #         webbrowser.open("http://www.cognifront.com/iteachers.php#books")
                        #         break
                        #     break
                        # break
                        # Displaying the extracted text
                        # print(text[:-1])
                        # global Answer
                        global Answer1
                        Answer1=self.ans(text)
                        print(Answer1)                   
                        
                        
                            

        # For each detection
            #     for detection in output:
            # # Get the class label and class score
            #         print(int(detection[1]))
                    # class_label = int(detection[0])
                    # class_score = float(detection[1])
            
            # Check if the class label is "book"
                # if class_label == 73:
                # # Keep the detection if the class score is above a threshold
                #     if class_score > 0.2:
                #     # Store the detection information
                #         book_detections.append("hello")
                #         print(book_detections)
        # book_detections now contains only the detections of the book
            
            cv2.imshow('Image', img)
        # encode the processed frame as JPEG
            # x = int((screen_width - img.shape[1]) / 2)
            # y = int((screen_height - img.shape[0]) / 2)
            # cv2.moveWindow("Image", x, y)
            key = cv2.waitKey(1)
            if key==ord("q"):
                break

        self.video.release()
        # cv2.destroyAllWindows()
        ret,jpg=cv2.imencode('.jpg',frame)
        return jpg.tobytes()
# vid1=Video()
# Result=vid1.ans(text=Answer1)