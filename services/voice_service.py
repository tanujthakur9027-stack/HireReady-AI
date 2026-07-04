from gtts import gTTS
import tempfile
import base64
import os


def text_to_speech(text):

    try:

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        with open(temp.name, "rb") as f:

            audio = base64.b64encode(
                f.read()
            ).decode()

        os.remove(temp.name)

        return audio

    except Exception:

        return None