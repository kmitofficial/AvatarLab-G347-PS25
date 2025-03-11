<div align="center">
    <h1>🎭 AI Avatar Lab</h1>
</div>

## 📌 Introduction
### Purpose of the Project
AI Avatar Lab is designed to create a highly realistic, AI-driven speaking avatar that synchronizes lip movements with generated speech. The project leverages advanced deep learning techniques to achieve seamless text-to-speech (TTS) conversion and realistic facial animations.

### Applications of the Project
- **Virtual Assistants** – AI-powered avatars for customer support, education, and interactive chatbots.
- **Content Creation** – Enhancing video production with AI-driven avatars.
- **Language Learning** – Improving pronunciation with real-time lip-sync.
- **Gaming & VR** – Integrating lifelike AI characters for immersive experiences.

---

## 📌 Architecture Diagram
![downloads](https://github.com/user-attachments/assets/740bdae8-3c9c-4f82-ae67-45855694ef3e)

### Step-by-Step Explanation  

1. **User Interaction** – The user uploads text, speech, or an image via the **React.js frontend**.  
2. **API Communication** – The frontend communicates with the backend using a **REST API** built with **FastAPI and Flask**.  
3. **AI Processing:**  
   - **Text-to-Speech (TTS) Conversion** – The input text is converted into speech using **VITS**.  
   - **Talking Avatar Generation** – The **DiffTalk** model creates an animated avatar based on the speech and image.  
4. **Post-Processing Layer:**  
   - **Audio-Video Synchronization** – Aligns the generated speech with the avatar’s lip movements.  
   - **Rendering Engine** – Uses **FFmpeg & a Custom Renderer** to finalize the video.  
5. **Storage & Deployment:**  
   - **AWS S3** stores generated videos and audio files.  
   - **CDN (Cloudflare / AWS CloudFront)** ensures fast content delivery.  
   - **WebSockets** provide real-time updates to the frontend.  
6. **User Output** – The **React.js frontend** displays the final talking avatar video for the user to view, download, or share.  

---

## 📌 Workflow Diagram
![download (1)](https://github.com/user-attachments/assets/be942b30-020b-42bf-ba22-a0cdb17b2d6e)

### Step-by-Step Explanation
1. **User Input** – The user provides a text input.
2. **Text-to-Speech (TTS) Conversion** – The input text is converted into speech using **VITS TTS**.
3. **Lip-Sync Animation Generation (Highlighted Section):**
   - **Process Speech Audio** – The generated speech is analyzed.
   - **Generate Lip Movements** – AI maps speech phonemes to facial movements.
   - **AI-Driven Avatar Animation** – The lip movements are applied to the avatar using **DiffTalk, Wav2Lip, and Face Mesh**.
4. **Avatar Rendering** – The animated avatar is rendered using **Three.js and DeepFaceLive**.
5. **Final Output** – The user sees and hears the AI-powered speaking avatar.

---

## 📌 Brief Explanation of the Reference Research Papers
### Wav2Lip: Accurate Lip-Sync for Any Voice and Video
- This paper presents an advanced lip-sync model that achieves precise synchronization by training a GAN-based architecture.
- The technique improves upon existing methods by reducing lip-sync errors, making it ideal for AI avatars.

### DiffTalk: Diffusion Models for Talking Head Generation
- DiffTalk leverages diffusion models for realistic facial animation, outperforming traditional GAN-based methods.
- It enables fine-grained control over facial movements, enhancing expressiveness in AI avatars.

### FastSpeech 2: Fast and High-Quality End-to-End Text-to-Speech
- This paper introduces an improved TTS model that enhances speech clarity and expressiveness.
- It ensures real-time speech synthesis, making it suitable for interactive AI avatars.
