try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
    cv2 = None

from streamlit_webrtc import VideoTransformerBase


class VideoProcessor(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        if not CV2_AVAILABLE:
            return img

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        faces = face_detector.detectMultiScale(gray)

        for (x, y, w, h) in faces:

            cv2.rectangle(
                img,
                (x, y),
                (x+w, y+h),
                (0,255,0),
                2
            )

        return img