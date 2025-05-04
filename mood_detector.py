from deepface import DeepFace

def detect_mood(image_path):
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion'], detector_backend='ssd')
        return analysis[0]['dominant_emotion']
    except Exception as e:
        print(f"Error in mood detection: {e}")
        return None
