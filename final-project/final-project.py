import cv2 as cv
import numpy as np

def follow_husky(input, name, outpath):
    cap = cv.VideoCapture(input)

    #motion detection e background subtraction
    background_remover = cv.createBackgroundSubtractorKNN(detectShadows=True)

    frames = []
    max_cnts = []
    path = []

    while(cap.isOpened()):
        ret, frame = cap.read()

        if frame is None:
            break

        result = frame.copy()
        image = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        lower_red = np.array([165,30,20])
        upper_red = np.array([189,255,255])

        #filtro de cores
        mask = cv.inRange(image, lower_red, upper_red)
        red_area = cv.bitwise_and(result, result, mask=mask)

        #blur para reduzir ruido
        frame = cv.GaussianBlur(frame, (5, 5), 0)
        
        #background subtraction e suavização com o operador morfológico da máscara resultante
        mask = background_remover.apply(red_area)
        _, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((3,3),np.uint8)) 
        
        #blobs resultantes
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        #seleciona apenas o maior blob válido e desenhamos uma elipse sobre ele
        max_cnt = [0, 0]
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > 800 and len(cnt) >= 5:
                if area > max_cnt[0]:
                    max_cnt = [area, cnt]
        
        if max_cnt[0] != 0:
            elipse = cv.fitEllipse(max_cnt[1])
            path.append([int(elipse[0][0]), int(elipse[0][1])])
            cv.ellipse(frame, elipse, (0, 255, 0), 2)

        #caminho percorrido pelo blob
        for point in path:
            cv.circle(frame, (point[0], point[1]), 2, (255, 255, 255))

        #salva os frames e os blobs
        if ret == True:
            frames.append(frame)
            max_cnts.append(max_cnt)

        #debug options
        #cv.imshow('mask', frame)
        #key = cv.waitKey(33)
        
        #if key == 27:
        #    break

    cap.release()
    cv.destroyAllWindows()

    #salva os frames como video
    img = frames[5].copy()
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(outpath + name + '.avi', fourcc, 20.0, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        out.write(frame)
    out.release()

    #gera a imagem u,v e orientação
    step = 3
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    c_inc = 0
    for i in range(10, len(path)-10, step):
        u = path[i][0] - path[i-step][0]
        v = path[i][1] - path[i-step][1]
        orientation = np.arctan2(v, u)
        #check if length of line is too large (outlier => pescoço)
        if np.sqrt(u**2 + v**2) > 50:
            continue

        cv.arrowedLine(img, (path[i-step][0], path[i-step][1]), (path[i][0], path[i][1]), colors[c_inc%3], 1, tipLength=0.8)
        c_inc += 1

    cv.imwrite(outpath + name + '.png', img)
    return

follow_husky('data/video1_husky.mp4', 'husky1', 'output/')
follow_husky('data/video2_husky.mp4', 'husky2', 'output/')