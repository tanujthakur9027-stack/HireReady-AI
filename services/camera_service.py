try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    cv2 = None
    CV2_AVAILABLE = False

from streamlit_webrtc import VideoTransformerBase

if CV2_AVAILABLE:
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
else:
    face_detector = None


class VideoProcessor(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        if not CV2_AVAILABLE:
            return img

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            img,
            f"Faces : {len(faces)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        return img