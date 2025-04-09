from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        # Open and process the image
        img = Image.open(file.stream)
        output = remove(img)

        # Save to in-memory stream
        img_io = io.BytesIO()
        output.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='no-bg.png')

    return render_template('index.html')

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)
