from flask import Flask, request, send_file
from gtts import gTTS
import docx2txt
import os
from PyPDF2 import PdfFileReader
from docx import Document

app = Flask(__name__)

@app.route('/')
def form():
    return """
        <html>
        <body>
        <h1>Text to Speech</h1>
        <form method="POST" action="convert" enctype="multipart/form-data">
            <input type="file" name="doc_file" accept=".docx,.doc,.pdf,.txt">
            <input type="submit">
        </form>
        </body>
        </html>
    """

@app.route('/convert', methods=["POST"])
def convert_text_to_speech():
    file = request.files["doc_file"]
    if file.filename.endswith('.docx'):
        text = docx2txt.process(file)
    elif file.filename.endswith('.doc'):
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    elif file.filename.endswith('.pdf'):
        pdf = PdfFileReader(file)
        text = "\n".join([page.extract_text() for page in pdf.pages])
    elif file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    else:
        return "Invalid file type"

    speech = gTTS(text=text, lang='en', slow=False)
    speech.save("output.mp3")

    # Return the audio file to the user
    return send_file("output.mp3", as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
