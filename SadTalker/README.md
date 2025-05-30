<div align="center">
  <h1>🎭 AI Avatar Lab</h1>
</div>

---

## 📌 Introduction

### 🎯 Purpose of the Project  
AI Avatar Lab is designed to create a highly realistic, AI-driven speaking avatar that synchronizes lip movements with generated speech. The project leverages advanced deep learning techniques to achieve seamless text-to-speech (TTS) conversion and realistic facial animations.

### 🌐 Applications
- 💬 **Virtual Assistants** – AI-powered avatars for customer support, education, and interactive bots.  
- 🎥 **Content Creation** – Enhance videos with AI-driven talking avatars.  
- 📚 **Language Learning** – Improve pronunciation through real-time lip-sync visualization.  
- 🎮 **Gaming & VR** – Integrate lifelike AI characters into immersive environments.

---

## 📌 Architecture Diagram

![Architecture Diagram](https://github.com/user-attachments/assets/740bdae8-3c9c-4f82-ae67-45855694ef3e)

### 🛠️ Step-by-Step Breakdown
1. **User Input** – Image, text, or speech uploaded via **Streamlit frontend**.  
2. **Backend Processing** – Managed by **Python backend scripts** handling inference and processing.  
3. **AI Engine**:
   - **TTS**: Text converted to speech using **VITS**.  
   - **Avatar Generation**: Animated avatar created via **SadTalker**.
4. **Post-Processing**:
   - **Audio-Video Sync** – Align speech and facial movement.  
   - **Rendering** – Handled via **FFmpeg** and custom tools.
5. **Deployment**:
   - **AWS S3** – For file storage.  
   - **CDN** – (Cloudflare / AWS CloudFront) for fast delivery.  
   - **WebSockets** – For real-time frontend updates.
6. **Final Output** – Talking avatar video shown on **Streamlit frontend**.

---

## 📌 Workflow Diagram

![Workflow Diagram](https://github.com/user-attachments/assets/be942b30-020b-42bf-ba22-a0cdb17b2d6e)

### ⚙️ Workflow Details
1. **Text Input** – User enters or uploads text via **Streamlit UI**.
2. **TTS Conversion** – Converted to audio using **VITS TTS**.
3. **Lip Sync Animation**:
   - Analyze speech.  
   - Generate facial movements.  
   - Apply using **SadTalker**, **Wav2Lip**, and **Face Mesh**.
4. **Rendering** – Using **Three.js** and **DeepFaceLive**.
5. **Final Video Output** – Displayed with synchronized audio-visual output on **Streamlit frontend**.

---

## 📌 Research Paper References

### 🔊 Wav2Lip: Accurate Lip-Sync for Any Voice and Video
- GAN-based model ensuring precise lip-syncing.
- Ideal for multi-voice avatar generation.

### 🎥 SadTalker: AI Talking Head Generation
- Uses diffusion models for highly expressive and natural animations.
- Superior to traditional GANs in realism and control.

### 🗣️ FastSpeech 2: Fast and High-Quality End-to-End TTS
- Fast, expressive TTS synthesis.
- Suitable for real-time applications like avatars and assistants.

---

## 👥 Contributors

| S.No | Name                | GitHub ID                                                | Milestone 1 Video | Milestone 2 Video                  | PPT Link  |
|------|---------------------|-----------------------------------------------------------|-------------------|------------------------------------|-----------|
| 1    | Raghav Cheruvu      | [@username1](https://github.com/username1)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |
| 2    | B. Akshaya Reddy    | [@username2](https://github.com/username2)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |
| 3    | Y. Akshaya Reddy    | [@Akshayareddy12022006](https://github.com/Akshayareddy12022006) | [bit.ly/4kCCdTn](https://bit.ly/4kCCdTn) | [YouTube](https://youtu.be/8DS62FEVblk) | [PPT](#)  |
| 4    | A. Jahnavi Reddy    | [@username4](https://github.com/username4)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |
| 5    | A. Sri Vyshnavi     | [@username5](https://github.com/username5)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |
| 6    | M. Rajashekar Reddy | [@username6](https://github.com/username6)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |
| 7    | M. Shiva Reddy      | [@username7](https://github.com/username7)               | [Video 1](#)      | [Video 2](#)                        | [PPT](#)  |

---
