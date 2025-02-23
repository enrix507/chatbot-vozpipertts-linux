import os
import subprocess
import base64
from flask import Flask, request, jsonify, Response, stream_with_context, send_file
from flask_cors import CORS
import google.generativeai as genai
import json
import time

app = Flask(__name__)
CORS(app)

# Configurar API key y modelo
api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyD9zzEWibJGLwKqaGszyorPqucdGwIKybU')
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    generation_config={
        'temperature': 0.9,
        'top_p': 0.9,
        'top_k': 40,
        'max_output_tokens': 200,
    }
)

# Configuración de Piper TTS
PIPER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "piper")
PIPER_MODEL = "es_ES-davefx-medium.onnx"

def generar_audio(texto):
    try:
        temp_text = f"temp_{int(time.time())}.txt"
        temp_audio = f"temp_{int(time.time())}.wav"
        text_path = os.path.join(PIPER_PATH, temp_text)
        audio_path = os.path.join(PIPER_PATH, temp_audio)
        
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(texto)
        
        cmd = f'./piper --model {PIPER_MODEL} --output_file {temp_audio} < {temp_text}'
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=PIPER_PATH,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return None
            
        if os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            
            # Limpiar archivos temporales inmediatamente
            try:
                os.remove(text_path)
                os.remove(audio_path)
            except:
                pass
                
            return audio_base64
            
        return None
        
    except Exception as e:
        print(f"Error al generar audio: {str(e)}")
        # Intentar limpiar archivos en caso de error
        try:
            if os.path.exists(text_path):
                os.remove(text_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass
        return None

@app.route('/chat-stream', methods=['GET'])
def chat_stream():
    try:
        user_message = request.args.get('message', '')
        
        def generate():
            prompt = f"Eres chinri, mi mejor amiga chistosa y divertida. Responde de forma breve y con humor. Usuario dice: {user_message}"
            response = model.generate_content(prompt, stream=True)
            
            accumulated_text = ""
            for chunk in response:
                if chunk.text:
                    accumulated_text += chunk.text
                    yield f"data: {json.dumps({'chunk': chunk.text, 'full_text': accumulated_text})}\n\n"
            
            # Generar audio al final
            audio_base64 = generar_audio(accumulated_text)
            if audio_base64:
                yield f"data: {json.dumps({'audio': audio_base64, 'done': True})}\n\n"
            else:
                yield f"data: {json.dumps({'error': 'Error al generar audio', 'done': True})}\n\n"
                
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
        
    except Exception as e:
        print(f"Error en /chat-stream: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        # Generar respuesta
        prompt = f"Actúa como un chinri mi mejor amiga chistosa. El usuario dice: {user_message}"
        response = model.generate_content(prompt)
        bot_response = response.text
        
        # Generar audio
        audio_base64 = generar_audio(bot_response)
        
        return jsonify({
            'respuesta': bot_response,
            'audio': audio_base64,
            'error': None if audio_base64 else 'Error al generar audio'
        })
        
    except Exception as e:
        print(f"Error en /chat: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chinri Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f0f2f5;
            }
            #chat-container {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ccc;
                padding: 20px;
                margin-bottom: 20px;
                background: white;
                border-radius: 10px;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 10px;
            }
            .user-message {
                background: #e3f2fd;
                margin-left: 20%;
                margin-right: 5px;
            }
            .bot-message {
                background: #f5f5f5;
                margin-right: 20%;
                margin-left: 5px;
            }
            #input-container {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            #user-input {
                flex-grow: 1;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background: #1a73e8;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #1557b0;
            }
            .loading {
                display: none;
                color: #666;
                font-style: italic;
                margin-bottom: 10px;
            }
            #mic-button {
                padding: 10px;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #dc3545;
                transition: background-color 0.3s;
            }
            #mic-button.active {
                background: #28a745;
            }
            #mic-status {
                display: none;
                color: #28a745;
                margin-bottom: 10px;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <h1>Chat con Chinri 🤖</h1>
        <div id="chat-container"></div>
        <div class="loading" id="loading">Chinri está escribiendo...</div>
        <div id="mic-status">Micrófono activo - Hablando...</div>
        <div id="input-container">
            <input type="text" id="user-input" placeholder="Escribe tu mensaje...">
            <button id="mic-button" onclick="toggleMicrophone()">🎤</button>
            <button onclick="sendMessage()">Enviar</button>
        </div>

        <script>
            const chatContainer = document.getElementById('chat-container');
            const userInput = document.getElementById('user-input');
            const loading = document.getElementById('loading');
            const micButton = document.getElementById('mic-button');
            const micStatus = document.getElementById('mic-status');
            
            let recognition = null;
            let isRecording = false;

            // Configurar reconocimiento de voz
            function initializeSpeechRecognition() {
                if ('webkitSpeechRecognition' in window) {
                    recognition = new webkitSpeechRecognition();
                    recognition.continuous = true;      // Mantener el micrófono activo continuamente
                    recognition.interimResults = true;
                    recognition.lang = 'es-ES';

                    recognition.onstart = () => {
                        isRecording = true;
                        micButton.classList.add('active');
                        micStatus.style.display = 'block';
                        micStatus.textContent = 'Escuchando...';
                    };

                    recognition.onend = () => {
                        // Si aún está en modo grabación, reiniciar automáticamente
                        if (isRecording) {
                            setTimeout(() => {
                                try {
                                    recognition.start();
                                } catch (e) {
                                    console.error('Error al reiniciar reconocimiento:', e);
                                }
                            }, 100);
                        } else {
                            micButton.classList.remove('active');
                            micStatus.style.display = 'none';
                            micStatus.textContent = '';
                        }
                    };

                    recognition.onresult = (event) => {
                        let finalTranscript = '';
                        let interimTranscript = '';
                        
                        for (let i = event.resultIndex; i < event.results.length; i++) {
                            const transcript = event.results[i][0].transcript;
                            if (event.results[i].isFinal) {
                                finalTranscript += transcript;
                            } else {
                                interimTranscript += transcript;
                            }
                        }
                        
                        // Mostrar texto mientras habla
                        if (interimTranscript) {
                            userInput.value = interimTranscript;
                        }
                        
                        // Si hay texto final, enviarlo pero NO detener el reconocimiento
                        if (finalTranscript) {
                            userInput.value = finalTranscript;
                            sendMessage();
                        }
                    };

                    recognition.onerror = (event) => {
                        console.error('Error en reconocimiento de voz:', event.error);
                        if (event.error === 'no-speech' && isRecording) {
                            // Si no hay habla pero está activo, reiniciar
                            recognition.stop();
                            setTimeout(() => {
                                if (isRecording) {
                                    try {
                                        recognition.start();
                                    } catch (e) {
                                        console.error('Error al reiniciar después de no-speech:', e);
                                    }
                                }
                            }, 100);
                        }
                    };
                } else {
                    micButton.style.display = 'none';
                    console.error('El reconocimiento de voz no está soportado en este navegador');
                }
            }

            // Función para alternar el micrófono
            function toggleMicrophone() {
                if (!recognition) {
                    initializeSpeechRecognition();
                }
                
                if (isRecording) {
                    // Lo detenemos manualmente
                    isRecording = false;
                    recognition.stop();
                } else {
                    // Lo iniciamos manualmente
                    isRecording = true;
                    recognition.start();
                }
            }

            function addMessage(text, isUser) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
                messageDiv.textContent = text;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }

            function playAudio(base64Audio) {
                // 1. Pausar el reconocimiento antes de reproducir
                if (recognition && isRecording) {
                    recognition.stop();
                    isRecording = false;
                }

                // 2. Reproducir el audio
                const audio = new Audio('data:audio/wav;base64,' + base64Audio);
                
                // 3. Cuando termine el audio, reactivar el micrófono
                audio.onended = () => {
                    if (recognition) {
                        isRecording = true;
                        recognition.start();
                    }
                };

                audio.play();
            }

            async function sendMessage() {
                const message = userInput.value.trim();
                if (!message) return;

                addMessage(message, true);
                userInput.value = '';
                loading.style.display = 'block';

                const eventSource = new EventSource(`/chat-stream?message=${encodeURIComponent(message)}`);
                let fullResponse = '';

                eventSource.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    
                    if (data.chunk) {
                        fullResponse = data.full_text;
                        const botMessages = document.getElementsByClassName('bot-message');
                        if (botMessages.length > 0) {
                            botMessages[botMessages.length - 1].textContent = fullResponse;
                        } else {
                            addMessage(fullResponse, false);
                        }
                    }
                    
                    if (data.audio) {
                        playAudio(data.audio);
                    }
                    
                    if (data.done) {
                        eventSource.close();
                        loading.style.display = 'none';
                    }
                };

                eventSource.onerror = function() {
                    eventSource.close();
                    loading.style.display = 'none';
                };
            }

            userInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Inicializar reconocimiento de voz al cargar
            initializeSpeechRecognition();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Verificar que exista el directorio y el modelo
    if not os.path.exists(PIPER_PATH):
        raise Exception(f"No se encontró el directorio de Piper: {PIPER_PATH}")
        
    model_path = os.path.join(PIPER_PATH, PIPER_MODEL)
    if not os.path.exists(model_path):
        raise Exception(f"No se encontró el modelo de Piper: {model_path}")
    
    print("=== Configuración ===")
    print(f"Directorio Piper: {PIPER_PATH}")
    print(f"Modelo: {PIPER_MODEL}")
    print("==================")
    
    # Ejecutar en modo producción
    app.run(host='0.0.0.0', port=5000, debug=False)
