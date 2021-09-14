from MyQR import myqr

def myqr_self():
    myqr.run(words='https://www.csdn.net/',
             picture='test.jpg',
             colorized=True,
             save_name="test.png")

    myqr.run(words='https://www.csdn.net/',
             picture='eye.gif',
             colorized=True,
             save_name="eye_qr.gif")

if __name__ == '__main__':
    myqr_self()