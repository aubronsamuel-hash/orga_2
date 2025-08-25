param([string]$Host, [string]$Db)
ssh $Host "pg_dump $Db > backup.sql"
