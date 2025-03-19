import os
import zipfile
from PIL import Image, ImageDraw, ImageFont

class PhotoProcessor:
    def __init__(self, input_dir="photos", output_dir="output", watermark_text="Fotographiya"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.watermark_text = watermark_text
        self.formats = [
            ("web", (1920, 1080), "JPEG"),
            ("mobile", (1080, 720), "JPEG"),
            ("print", (300, 300), "PNG"),
        ]
        os.makedirs(self.output_dir, exist_ok=True)

    def get_font(self, size=60):
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    def add_watermark(self, image):
        draw = ImageDraw.Draw(image)
        font = self.get_font(size=30)
        bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = image.width - text_width - 10
        y = image.height - text_height - 10
        draw.text((x, y), self.watermark_text, font=font, fill=(255, 255, 255, 128))
        return image

    def process_image(self, img_path, filename):
        img = Image.open(img_path)
        for format_name, size, img_format in self.formats:
            resized_img = img.copy().resize(size)
            watermarked_img = self.add_watermark(resized_img)
            output_filename = f"{format_name}_{os.path.splitext(filename)[0]}.{img_format.lower()}"
            output_path = os.path.join(self.output_dir, output_filename)
            watermarked_img.save(output_path, img_format)
            print(f"Saved: {output_path}")

    def process_batch(self):
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                img_path = os.path.join(self.input_dir, filename)
                self.process_image(img_path, filename)
        print("Batch processing completed!")
        self.zip_output()

    def zip_output(self):
        zip_filename = "Wedding_Photos_Package.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(self.output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=file)
        print(f"Photos packaged into {zip_filename}")

if __name__ == "__main__":
    processor = PhotoProcessor()
    processor.process_batch()
