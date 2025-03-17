from flask import Flask, request  
import os  
import speech_recognition as sr  
from pydub import AudioSegment  

app = Flask(__name__)  

@app.route('/')  
def index():  
    return '''  
      <html>  
    <head>  
        <title>Audio to Text LWS25</title>  
        <style>  
            body {  
                font-family: Arial, sans-serif;  
                margin: 20px;  
                height: 100vh;  
                background-color: #1e1e1e;  
                color: white;  
                display: flex;  
                flex-direction: column;  
                align-items: center;  
                justify-content: center;  
            }  
            form {  
                text-align: center;  
                background-color: #2e2e2e;  
                padding: 20px;  
                border-radius: 10px;  
                width: 50%;  
            }  
            input, select, button {  
                margin: 10px;  
                padding: 10px;  
                width: 80%;  
            }  
            button {  
                background-color: #00adb5;  
                color: white;  
                border: none;  
                cursor: pointer;  
            }  
        </style>  
    </head>  
    <body>  
        <h1>Audio to Text Transcriber - LWS25</h1>  
        <form action="/upload" method="post" enctype="multipart/form-data">  
            <input type="file" name="audio" required><br>  
            <select name="language">  
                <option value="en-US">English</option>  
                <option value="id-ID" selected>Indonesia</option>  
                <option value="ja-JP">Jepang</option>  
                <option value="ko-KR">Korea</option>  
                <option value="ar-SA">Arab</option>  
            </select><br>  
            <button type="submit">Upload & Transkrip</button>  
        </form>  
    </body>  
    </html>  
    '''  

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return 'No file uploaded', 400

    audio_file = request.files['audio']
    language = request.form['language']
    
    if audio_file.filename == '':
        return 'No selected file', 400

    # Simpan audio sementara di RAM
    audio_path = 'temp_audio_input.wav'
    audio_file.save(audio_path)

    text = audio_to_text(audio_path, language)

    # Hapus audio setelah transkrip
    os.remove(audio_path)
    
    return f'''
    <html>
    <head>
        <title>Transkrip Audio</title>
        <style>
            body {{
                font-family: Arial, sans-serif;  
                margin: 20px;  
                height: 100vh;  
                background-color: #1e1e1e;  
                color: white;  
                display: flex;  
                flex-direction: column;  
                align-items: center;  
                justify-content: center;  
            }}
            textarea {{
                width: 80%;  
                height: 200px;  
                margin-bottom: 20px;  
                background-color: #2e2e2e;  
                color: white;  
                border: none;  
                padding: 10px;  
                border-radius: 10px;  
            }}
            button {{
                background-color: #00adb5;  
                color: white;  
                border: none;  
                padding: 10px 20px;  
                cursor: pointer;  
                border-radius: 5px;  
            }}
            button:hover {{
                background-color: #007e8c;  
            }}
        </style>
    </head>
    <body>
        <h1>Transkrip Audio LWS25</h1>
        <textarea id="transcript" readonly>{text}</textarea><br>
        <button onclick="copyText()">Copy Transkrip</button>

        <script>
            function copyText() {{
                var textArea = document.getElementById('transcript');
                textArea.select();
                document.execCommand('copy');
            }}
        </script>
    </body>
    </html>
    '''

def audio_to_text(audio_path, language):  
    recognizer = sr.Recognizer()  

    # Convert semua format audio ke WAV
    audio = AudioSegment.from_file(audio_path)  
    audio.export("temp.wav", format="wav")  

    with sr.AudioFile("temp.wav") as source:  
        audio_data = recognizer.record(source)  
        try:  
            text = recognizer.recognize_google(audio_data, language=language)  
        except sr.UnknownValueError:  
            text = "Gagal mengenali audio. Coba lagi dengan audio yang lebih jelas."  
        except sr.RequestError:  
            text = "Koneksi ke Google Speech API gagal. Cek koneksi internet."  
        finally:  
            os.remove("temp.wav")  

    return text  

if __name__ == "__main__":  
    app.run()