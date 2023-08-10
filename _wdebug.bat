docker build -t localsw .
docker run -p 5002-5010:5002-5010 -e TELEGRAM_TOKEN=T_O_K_E_N localsw