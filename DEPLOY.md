# Despliegue del Chatbot en VPS

## Requisitos del Servidor
- Ubuntu 20.04 o superior
- Docker y Docker Compose instalados
- Al menos 2GB de RAM
- 20GB de espacio en disco

## Pasos para el Despliegue

### 1. Preparar el Servidor

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose -y
```

### 2. Clonar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/enrix507/chatbot-vozpipertts.git
cd chatbot-vozpipertts
```

### 3. Configurar Variables de Entorno

```bash
# Crear archivo .env
echo "GOOGLE_API_KEY=tu_api_key_aqui" > .env
```

### 4. Construir y Ejecutar con Docker

```bash
# Construir la imagen
docker-compose build

# Ejecutar en segundo plano
docker-compose up -d
```

### 5. Verificar el Despliegue

```bash
# Ver logs
docker-compose logs -f

# Verificar que el contenedor está corriendo
docker ps
```

## Configuración de Dominio

1. Apunta tu dominio al IP del servidor
2. Configura SSL con Let's Encrypt:

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tudominio.com
```

## Mantenimiento

### Actualizar el Chatbot
```bash
# Detener contenedores
docker-compose down

# Obtener últimos cambios
git pull

# Reconstruir y reiniciar
docker-compose up -d --build
```

### Ver Logs
```bash
# Ver logs en tiempo real
docker-compose logs -f
```

### Respaldos
```bash
# Respaldar configuración
cp .env .env.backup
```

## Solución de Problemas

### Si el contenedor no inicia:
```bash
# Ver logs detallados
docker-compose logs chatbot

# Reiniciar contenedor
docker-compose restart chatbot
```

### Si hay problemas de memoria:
```bash
# Ver uso de recursos
docker stats
```

### Si hay problemas de red:
```bash
# Verificar puertos
sudo netstat -tulpn | grep LISTEN
```

## Recomendaciones de Seguridad

1. Mantén el sistema actualizado
2. Usa contraseñas fuertes
3. Configura un firewall
4. Habilita HTTPS
5. Revisa logs regularmente

## Monitoreo

Recomendamos usar:
- Portainer para gestión de Docker
- Prometheus + Grafana para métricas
- Fail2ban para seguridad
