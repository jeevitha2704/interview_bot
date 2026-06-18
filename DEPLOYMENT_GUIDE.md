# Vercel Deployment Guide for Interview Bot

## ✅ Repository Setup Complete

Your code has been successfully pushed to: **https://github.com/jeevitha2704/interview_bot**

## 🚀 Deploying to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com) and log in
   - Click "Add New..." → "Project"

2. **Import Your Repository**
   - Search for "interview_bot" in your GitHub repositories
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Select "Python" (or leave as "Other")
   - **Root Directory**: Keep as `./` (root)
   - **Build Command**: Leave blank (Vercel will auto-detect)
   - **Output Directory**: Leave blank
   - **Install Command**: Leave blank (Vercel will use requirements.txt)

4. **Environment Variables**
   - Click "Environment Variables" → "Add Variable"
   - Add the following variables from your `.env.example`:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `FLASK_ENV`: Set to `production`
     - Any other required variables

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (~2-3 minutes)
   - Vercel will provide a live URL (e.g., `https://interview-bot.vercel.app`)

### Option 2: Deploy via Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to project directory
cd /Users/jeevithaj/Downloads/INTERVIEW_BOT

# Deploy to production
vercel --prod
```

## 🔧 Post-Deployment Configuration

### Environment Variables
Make sure to set these in Vercel's dashboard:
- **Project Settings** → **Environment Variables**
- Add all variables from your `.env.example` file
- Set `FLASK_ENV=production` for production deployments

### Custom Domain (Optional)
1. Go to **Project Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed

## 📝 Important Notes

### 1. File Structure
Your project is correctly structured for Vercel:
```
interview_bot/
├── app.py                 # Main Flask app entry point
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── app/                  # Flask app package
│   ├── __init__.py
│   ├── routes.py
│   ├── question_generator.py
│   └── resume_parser.py
├── templates/            # HTML templates
├── static/              # CSS, JS files
└── uploads/             # Upload directory
```

### 2. Vercel Configuration
The `vercel.json` file configures:
- Python runtime via `@vercel/python`
- Route handling to direct all requests to `app.py`
- Production environment settings

### 3. Dependencies
All required packages are listed in `requirements.txt`:
- Flask and extensions
- OpenAI SDK
- PDF and document processing libraries
- CORS support

### 4. Build Process
Vercel will automatically:
1. Detect Python runtime
2. Install dependencies from `requirements.txt`
3. Build and deploy your Flask app
4. Set up serverless functions

## 🔍 Testing Your Deployment

After deployment:
1. Visit your Vercel URL (e.g., `https://your-project.vercel.app`)
2. Test the main page loads
3. Test resume upload functionality
4. Test AI question generation

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check Vercel deployment logs
   - Ensure all dependencies are in `requirements.txt`
   - Verify `app.py` imports are correct

2. **Runtime Errors**
   - Check environment variables are set correctly
   - Verify API keys are valid
   - Check Vercel function logs

3. **404 Errors**
   - Ensure `vercel.json` routes are configured correctly
   - Check that static files are in the `static/` directory

4. **CORS Issues**
   - Flask-CORS is already configured in your app
   - May need to configure allowed origins in production

## 📊 Monitoring

- **Vercel Dashboard**: View deployment logs and analytics
- **Function Logs**: Check serverless function execution
- **Custom Domains**: Monitor traffic and performance

## 🔄 Updating Your App

After making changes:
```bash
# Commit and push changes
git add .
git commit -m "Your changes"
git push origin main

# Vercel will automatically redeploy!
```

## 🆘 Need Help?

- [Vercel Documentation](https://vercel.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)

---

**Your app is now ready to deploy! 🎉**

Follow the steps above, and your Interview Bot will be live on Vercel in minutes.