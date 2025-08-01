# PDF Paper Downloader

## Deployment on Railway

This application is configured to be deployed on Railway. Follow these steps to deploy it:

1. Make sure you have an account on [Railway](https://railway.app/)
2. Connect your GitHub repository to Railway
3. Create a new project in Railway by selecting the repository
4. Railway will automatically detect the configuration and deploy the application

### Configuration Files for Railway

- `Procfile`: Defines the command to start the application
- `nixpacks.toml`: Configures the build process
- `railway.toml`: Railway-specific configuration
- `runtime.txt`: Specifies the Python version
- `.env`: Environment variables (not uploaded to the repository)

### Environment Variables

- `FLASK_ENV`: Sets the Flask environment (development/production)
- `PORT`: The port on which the application will run (Railway provides this automatically)

### Endpoints

- `/health`: Verifies that the API is working
- `/download`: Downloads the PDF
- `/direct-download`: Direct download of the PDF to the client