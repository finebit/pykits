# -*- coding: utf-8 -*-
# test.py
# Author: FineBit
import cv2

if __name__ == '__main__':
    img = cv2.imread("../res/sign3.jpg")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_img, 50, 255, cv2.THRESH_BINARY)
    thresh = cv2.resize(thresh, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("binary", thresh)
    cv2.waitKey(0)
    cv2.destroyWindow("binary")
    # 无损保存到png
    cv2.imwrite("new_sign3.png", thresh, [cv2.IMWRITE_PNG_COMPRESSION, 0])
