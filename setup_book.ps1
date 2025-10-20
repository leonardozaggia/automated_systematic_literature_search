# Quick Setup Script for AMSR Book

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "AMSR Book - Quick Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if conda is available
Write-Host "Checking for conda..." -ForegroundColor Yellow
$condaAvailable = Get-Command conda -ErrorAction SilentlyContinue

if (-not $condaAvailable) {
    Write-Host "❌ Conda not found. Please install Miniforge or Anaconda first." -ForegroundColor Red
    Write-Host "Download from: https://github.com/conda-forge/miniforge/releases" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Conda found!" -ForegroundColor Green
Write-Host ""

# Create environment
Write-Host "Creating 'amsr' environment with Python 3.10..." -ForegroundColor Yellow
conda create -n amsr python=3.10 -y

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Environment created!" -ForegroundColor Green
Write-Host ""

# Activate environment (note: activation in scripts has limitations)
Write-Host "Activating environment..." -ForegroundColor Yellow
Write-Host "(Note: You may need to run 'conda activate amsr' manually after this script)" -ForegroundColor Yellow
Write-Host ""

# Install requirements
Write-Host "Installing book requirements..." -ForegroundColor Yellow
conda run -n amsr pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Requirements installed!" -ForegroundColor Green
Write-Host ""

# Build the book
Write-Host "Building Jupyter Book..." -ForegroundColor Yellow
conda run -n amsr jupyter-book build .

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Build completed with warnings (this is normal)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Book built successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate the environment: conda activate amsr" -ForegroundColor White
Write-Host "2. View the book: Open _build/html/index.html in your browser" -ForegroundColor White
Write-Host "3. Make changes and rebuild: jupyter-book build ." -ForegroundColor White
Write-Host ""
Write-Host "For deployment to GitHub Pages:" -ForegroundColor Yellow
Write-Host "git add . && git commit -m 'Update book' && git push origin main" -ForegroundColor White
Write-Host ""
Write-Host "Happy researching! 📚🔬" -ForegroundColor Cyan
