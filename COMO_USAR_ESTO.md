# 📱 Cómo Usar Este Chatbot con Voz

## 🚀 Pasos para Hacer Funcionar el Chatbot

### 1️⃣ Preparar los Archivos de Piper TTS
1. Descarga estos archivos de [Piper TTS para Windows](https://github.com/rhasspy/piper/releases):
   - `piper.exe`
   - La carpeta `espeak-ng-data`
   - `onnxruntime.dll`
   - El modelo de voz en español: `es_MX-claude-high.onnx`

2. Crea una carpeta llamada `piper` y pon todos esos archivos ahí dentro.

### 2️⃣ Instalar Python y Dependencias
1. Descarga e instala [Python 3.8 o más nuevo](https://www.python.org/downloads/)
2. Abre una terminal en la carpeta del proyecto
3. Instala las dependencias:
   ```bash
   pip install flask flask-cors google-generativeai
   ```

### 3️⃣ Configurar la API de Google
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una API key
3. Abre el archivo `chatbot.py`
4. Busca esta línea:
   ```python
   genai.configure(api_key='TU_API_KEY')
   ```
5. Reemplaza 'TU_API_KEY' con tu API key

### 4️⃣ Ejecutar el Chatbot
1. Abre una terminal en la carpeta del proyecto
2. Ejecuta:
   ```bash
   python chatbot.py
   ```
3. Abre tu navegador
4. Ve a: `http://localhost:5000`

## 🎙️ Cómo Usar el Chatbot

### Para Hablar con el Chatbot:
1. Haz clic en el botón del micrófono 🎤
2. El botón se pondrá verde cuando esté activo
3. Habla normalmente - te escuchará continuamente
4. Cuando el chatbot responda:
   - El micrófono se pausará automáticamente
   - Escucharás la respuesta
   - El micrófono se reactivará solo cuando termine
5. Para apagar el micrófono, haz clic nuevamente en el botón

### También puedes escribir:
1. Escribe tu mensaje en el cuadro de texto
2. Presiona Enter o haz clic en Enviar
3. El chatbot responderá con texto y voz

## ❌ Solución de Problemas

### Si el micrófono no funciona:
- Usa Chrome o Edge (funcionan mejor)
- Dale permiso al navegador para usar el micrófono
- Cierra otras apps que usen el micrófono

### Si no escuchas la voz del chatbot:
- Revisa que todos los archivos estén en la carpeta `piper`
- La estructura debe ser así:
  ```
  tu_carpeta/
  ├── piper/
  │   ├── piper.exe
  │   ├── onnxruntime.dll
  │   ├── es_MX-claude-high.onnx
  │   └── espeak-ng-data/
  ├── chatbot.py
  └── requirements.txt
  ```

### Si hay errores de API:
- Verifica que pusiste bien tu API key de Google
- Asegúrate de tener internet
- Revisa que no hayas superado el límite de la API

## 🔍 Estructura de Archivos
```
chatbot-vozpipertts/
├── chatbot.py            # Código principal
├── requirements.txt      # Dependencias
├── COMO_USAR_ESTO.md    # Este archivo
└── piper/               # Carpeta con archivos de voz
    ├── piper.exe
    ├── onnxruntime.dll
    ├── es_MX-claude-high.onnx
    └── espeak-ng-data/
```

## 💡 Consejos
- Habla claro y natural
- Espera a que el chatbot termine de hablar antes de hacer otra pregunta
- Si hay problemas, reinicia el servidor (Ctrl+C y vuelve a ejecutar python chatbot.py)
- Usa auriculares para evitar que el micrófono capte la voz del chatbot

## 🆘 ¿Necesitas Ayuda?
Si tienes problemas:
1. Revisa los mensajes de error en la terminal
2. Asegúrate de tener todos los archivos en el lugar correcto
3. Verifica que tienes todas las dependencias instaladas
4. Comprueba que tu API key de Google es válida
