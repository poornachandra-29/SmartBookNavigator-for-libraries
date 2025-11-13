from paddleocr import PaddleOCR
import numpy as np
import cv2
import time

class BookDetector:
    def __init__(self):
        print("⚙️ Initializing PaddleOCR...")
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        print("✅ OCR ready!\n")

    def process_image(self, image, search_text):
        rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        start = time.time()
        result = self.ocr.predict(rotated)
        print(f"⏱ Inference time: {time.time() - start:.2f}s")

        annotated = cv2.rotate(rotated, cv2.ROTATE_90_COUNTERCLOCKWISE)
        found_texts = []

        if result:
            data = result[0]
            texts = data['rec_texts']
            scores = data['rec_scores']
            polys = data['dt_polys']
            max_conf_idx = int(np.argmax(scores)) if scores else -1
            print(texts)
            print(search_text)
            for i, text in enumerate(texts):
                conf = scores[i]
                poly = np.array(polys[i]).astype(np.int32)
                if conf > 0.6:
                    print(f"Detected: {text} (Confidence: {conf:.2f})")
                    rotated_poly = np.array([[annotated.shape[1] - y, x] for (x, y) in poly], np.int32)
                    color = (0, 255, 0)
                    if i==max_conf_idx:
                        color = (255, 0, 0)
                        thickness=3  # Highlight highest confidence in blue
                    if search_text.lower() in text.lower():
                        print(f"--> Match found for search text: {search_text}")
                        found_texts.append((text, conf))
                        cv2.polylines(annotated, [rotated_poly], True, (0, 0, 255), 2)
                        x_min, y_min = np.min(rotated_poly[:, 0]), np.min(rotated_poly[:, 1])
                        cv2.putText(annotated, f"{text} ({conf:.2f})", (x_min, y_min - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        return annotated, found_texts
        