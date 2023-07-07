from flask import Flask, request, send_file
import os
from google.cloud import texttospeech
import docx2txt
from PyPDF2 import PdfFileReader
from docx import Document

app = Flask(__name__)

# List of available voices
voices = [
    texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-A',
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE),
    texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-D',
        ssml_gender=texttospeech.SsmlVoiceGender.MALE),
    # Add more voices here...
]

@app.route('/')
def form():
    return """
        <html>
        <body>
        <h1>Text to Speech</h1>
        <form method="POST" action="convert" enctype="multipart/form-data">
            <input type="file" name="doc_file" accept=".docx,.doc,.pdf,.txt">
            <select name="voice">
                <option value="0">Female (en-US-Wavenet-A)</option>
                <option value="1">Male (en-US-Wavenet-D)</option>
            </select>
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

    voice_index = request.form.get('voice')
    voice = voices[int(voice_index)]

    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the audio to a file
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    # Return the audio file to the user
    return send_file("output.mp3", as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
