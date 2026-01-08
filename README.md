# 🎭 Indonesian Sarcasm Detection - Web Application

A complete web application for detecting sarcasm in Indonesian text using a fine-tuned XLNet model. Built with FastAPI backend and Streamlit frontend, optimized for free deployment on Hugging Face Spaces.

## 📋 Overview

This project provides:

- **FastAPI Backend** (`app_api.py`): REST API for model inference
- **Streamlit Frontend** (`app_web.py`): Modern web UI for user interaction
- **Separation of Concerns**: Backend and frontend run independently
- **CPU-Only Inference**: No GPU required
- **Free Deployment**: Compatible with Hugging Face Spaces

## 🏗️ Project Structure

```
sarcasm-web/
├── app_api.py              # FastAPI backend (model inference)
├── app_web.py              # Streamlit frontend (user interface)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── best_checkpoint/       # Fine-tuned XLNet model folder
    ├── config.json
    ├── model.safetensors
    ├── special_tokens_map.json
    ├── spiece.model
    └── tokenizer_config.json
```

## 🚀 How to Run Locally

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the FastAPI Backend

Open a terminal and run:

```bash
python app_api.py
```

The API will be available at `http://localhost:7860`

Health check endpoint: `http://localhost:7860/health`

API documentation: `http://localhost:7860/docs`

### 3. Start the Streamlit Frontend (In a New Terminal)

```bash
streamlit run app_web.py
```

The web app will open at `http://localhost:8501`

## 🌐 How to Deploy on Hugging Face Spaces

### Prerequisites

- Hugging Face account (free)
- Git and Git LFS installed

### Step-by-Step Deployment

1. **Create a New Space**

   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose Space name: `sarcasm-detection` (or your preference)
   - Select "Docker" runtime
   - Click "Create Space"

2. **Clone the Space Repository**

   ```bash
   git clone https://huggingface.co/spaces/your-username/sarcasm-detection
   cd sarcasm-detection
   ```

3. **Add Model Files with Git LFS**

   ```bash
   git lfs install
   git lfs track "best_checkpoint/*"
   ```

4. **Copy Project Files**

   - Copy `app_api.py`, `app_web.py`, `requirements.txt`, `README.md`
   - Copy entire `best_checkpoint` folder

5. **Create Dockerfile**

   Create a file named `Dockerfile`:

   ```dockerfile
   FROM python:3.10

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 7860 8501

   CMD bash -c "python app_api.py & streamlit run app_web.py --server.port=8501"
   ```

6. **Create .gitattributes**

   ```
   best_checkpoint/** filter=lfs diff=lfs merge=lfs -text
   *.safetensors filter=lfs diff=lfs merge=lfs -text
   ```

7. **Push to Hugging Face**

   ```bash
   git add .
   git commit -m "Add sarcasm detection app"
   git push
   ```

   Hugging Face will automatically build and deploy your space!

## 📡 API Endpoints

### Health Check

```
GET /health
Response: {"status": "healthy"}
```

### Root Endpoint

```
GET /
Response: {"status": "ok", "message": "...", "model_loaded": true}
```

### Prediction Endpoint

```
POST /predict
Content-Type: application/json

Request:
{
  "text": "Your Indonesian text here"
}

Response:
{
  "prediction": "Sarcasm" | "Non-Sarcasm",
  "confidence": 0.95
}
```

## 🔧 Configuration

### Model Parameters

- **Model Type**: XLNet (fine-tuned)
- **Max Sequence Length**: 256 tokens
- **Device**: CPU only
- **Inference Mode**: torch.no_grad() (optimized)

### API Configuration

- **Host**: 0.0.0.0
- **Port**: 7860 (default)
- **Workers**: 1 (CPU-optimized)

### Streamlit Configuration

- **Port**: 8501 (default)
- **Max Request Size**: Enforced in frontend (1000 characters)

## 📊 Model Information

- **Framework**: Hugging Face Transformers
- **Architecture**: XLNet
- **Language**: Indonesian
- **Task**: Sequence Classification (Binary: Sarcasm/Non-Sarcasm)
- **Input**: Text (max 256 tokens)
- **Output**: Prediction + Confidence Score

## ⚡ Performance Optimization

- **CPU-Only**: No CUDA required, runs on any machine
- **No Gradient Computation**: Uses `torch.no_grad()` for faster inference
- **Model Evaluation Mode**: Sets `model.eval()` for inference optimization
- **Batch Disabled**: Single-text inference for simplicity
- **Async Ready**: FastAPI with async support for future scaling

## 🛡️ Error Handling

- Empty text validation
- Text length validation (max 1000 chars)
- API connection error handling
- Timeout handling (30 seconds)
- Model loading error handling

## 📝 Notes

- Ensure `best_checkpoint` folder is in the same directory as the scripts
- Model loading happens once at API startup
- Each prediction is independent and returns fresh results
- Confidence scores are normalized to 0-1 range

## 🐛 Troubleshooting

**Issue**: "Cannot connect to API server"

- Solution: Make sure `app_api.py` is running on port 7860

**Issue**: "Model not loaded"

- Solution: Check if `best_checkpoint` folder exists and contains all model files

**Issue**: Out of memory

- Solution: This is optimized for CPU. Consider using smaller batch sizes if deployed on limited hardware.

**Issue**: Slow inference

- Solution: Normal for CPU inference. GPU would be ~10x faster but costs money on cloud platforms.

## 📄 License

Open source. Feel free to modify and deploy.

## 🤝 Support

For issues or questions, check:

1. Model files are complete in `best_checkpoint`
2. Dependencies installed: `pip install -r requirements.txt`
3. Both services running (API on 7860, Streamlit on 8501)
