param([string]$Host, [string]$Project)
ssh $Host "cd $Project; docker compose -f docker-compose.staging.yml up -d"
