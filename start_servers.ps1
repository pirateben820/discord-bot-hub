# Discord Bot Hub - Start Development Servers
Write-Host "🚀 Starting Discord Bot Hub Development Environment" -ForegroundColor Cyan
Write-Host ""

# Start Backend API
Write-Host "📡 Starting Backend API Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python main.py"

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Frontend Dev Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "✅ Servers starting!" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🎨 Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop" -ForegroundColor Yellow

