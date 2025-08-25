Write-Host "Install backend deps"
pip install -r backend/requirements.txt
Write-Host "Install frontend deps"
npm --prefix frontend install
