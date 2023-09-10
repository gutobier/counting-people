import cv2
import numpy as np
import face_recognition as fr

def contagem_entrada(left, N1, N2, n_person):
	enter = False
	if 200 > left[1] > 100 and n_person > N1:
		N1 += 1
	if 300 > left[1] > 200:
		N2 += 1
	if N2 - N1 > 0:
		enter = True
		N1 -= 1
		N2 -= 1
	return N1, N2, enter

video = cv2.VideoCapture('loja_teste.mp4')

if video.isOpened() == False:
	print('Error opening video')

N = 0
N1 = 0
N2 = 0
while video.isOpened():
	ret, img = video.read()
	
	if ret:
		
		cv2.line(img, (50, 100), (600,100), (200,200,200), 2)
		cv2.line(img, (50, 180), (600,180), (200,200,200), 2)
		
		rgb_img = img[:,:,::-1]
		
		face_locations = fr.face_locations(rgb_img)
		#face_encodings = fr.face_encodings(rgb_img, face_locations)
		cv2.putText(img, ('Presentes: ' + str(len(face_locations))), (400, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
		cv2.putText(img, 'Entradas: ' + str(N), (400, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
		
		n_person = len(face_locations)
		
		print(face_locations)
		
		for top, right, bottom, left in face_locations:
			
			cv2.rectangle(img, (left, top), (right, bottom), (0,0,255), 1)
			
			N1, N2, enter = contagem_entrada(N1, N2, n_person)
		
		if enter:
			N += 1
		
		cv2.imshow("Imagem", img)
		
		if cv2.waitKey(25) & 0xFF == ord('q'):
			break
			
	else:
		break
		
video.release()
cv2.destroyAllWindows()