# How to Make Your Chatbot Live (Free)

Since I am an AI assistant running on your computer, I cannot directly access your credit card/accounts to deploy this. However, I have prepared all the necessary files (`requirements.txt`, `Procfile`) for you.

Here is the **easiest and 100% FREE method** to make it live using **Render.com**:

### Step 1: Push Code to GitHub
1. Create a new repository on GitHub.com.
2. Upload all the files in this folder to that repository.
   (If you have Git installed, run these commands in terminal):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   # Replace URL with your new repo URL
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Deploy on Render (Free)
1. Go to [dashboard.render.com](https://dashboard.render.com/) and Sign Up/Login.
2. Click **"New +"** and select **"Web Service"**.
3. Connect your GitHub account and select the repository you just created.
4. Scroll down to settings:
   - **Name**: `iqra-ai-chatbot` (or anything you like)
   - **Region**: Frankfurt (or nearest)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Select **"Free"**.

5. **CRITICAL STEP (Environment Variables)**:
   - Scroll to "Environment Variables" section.
   - Key: OPENROUTER_API_KEY
   - Value: (Paste your key from .env here)
   - Click "Add Environment Variable".

6. Click **"Create Web Service"**.

Wait about 2-3 minutes. Render will give you a URL like `https://iqra-ai-chatbot.onrender.com`.
**That link is your Live Website!** You can share it with anyone.
