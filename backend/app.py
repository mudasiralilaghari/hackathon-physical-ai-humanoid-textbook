from main import app

# This is the application instance that Hugging Face Spaces will run
app_instance = app

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use port 7860 which is the standard for Hugging Face Spaces
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app_instance, host="0.0.0.0", port=port)