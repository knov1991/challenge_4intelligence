# challenge_4intelligence

## Como rodar o projeto
1. `docker-compose up`
2.  - http://localhost:8001/
    - rota do tipo GET, pode usar o browser mesmo
    - a rota não espera nenhum parametro, esta usando o ip como identificador de usuario
    - deixei um print para mostrar o ip(user_id) e o count de requests, assim é possivel acompanhar pelo console

## Configurações
1. Deixei o arquivo `.env` incluso pois esse código tem o proposito apenas de teste local(não produção).
- REDIS_HOST=redis_notification
- REDIS_PORT=6379
- MAX_REQUESTS_PER_MINUTE=100
- TIME_SECONDS=60

2. `docker-compose.yml`
Em caso de conflito de portas por já estarem sendo usadas, altere.
- fastapi: 8001:8001
- redis: 6379:6379

## Como rodar os testes
1. `pytest src/tests`