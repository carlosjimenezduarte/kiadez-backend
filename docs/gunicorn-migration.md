# Migracion segura a Gunicorn + Uvicorn Worker

Esta migracion esta pensada para no tocar de inmediato el servicio actual con `uvicorn`.
La idea es levantar Gunicorn en otro puerto, validarlo, cambiar Nginx y solo despues retirar el servicio viejo.
No incluye migraciones de Alembic ni cambios de esquema: el objetivo es cambiar el proceso de aplicacion, no los datos.

Si quieres ir directo sobre `kiadez.com`, tambien puedes hacer un corte directo reemplazando el proceso actual en el mismo puerto interno que ya usa produccion.

## Lo que se agrego en el repo

- `requirements-production.txt`
- `deploy/gunicorn.conf.py`
- `deploy/gunicorn_worker.py`
- `deploy/systemd/kiadez-backend-gunicorn.service.example`
- `deploy/systemd/kiadez-backend-gunicorn-cutover.service.example`
- `deploy/nginx/kiadez-backend-gunicorn.conf.example`
- `scripts/install_production_requirements.sh`
- `scripts/run_gunicorn.sh`
- `scripts/check_backend_health.sh`

Nada de esto cambia el arranque actual por defecto.

## Suposiciones

- Backend FastAPI en `app.main:app`
- Virtualenv en `./venv`
- Servidor Linux con `systemd`
- Nginx como proxy reverso
- Servicio actual con `uvicorn` vivo en produccion

## Fase 0: respaldo rapido

Antes de mover nada, guarda la configuracion actual:

```bash
sudo systemctl cat kiadez-backend
sudo cp /etc/systemd/system/kiadez-backend.service /etc/systemd/system/kiadez-backend.service.bak
sudo nginx -T > /tmp/nginx-before-gunicorn.txt
```

Si tu servicio actual tiene otro nombre, reemplazalo en los comandos.

Si quieres blindarte aun mas frente al miedo de perder datos, toma tambien un backup de PostgreSQL antes del corte:

```bash
pg_dump -Fc -h 127.0.0.1 -U <usuario_db> -d <nombre_db> > /tmp/kiadez-pre-gunicorn.dump
```

Ese respaldo es preventivo. Esta migracion no deberia tocar tablas ni registros.

## Fase 1: instalar dependencias nuevas

En el servidor:

```bash
cd /srv/kiadez-backend/current
scripts/install_production_requirements.sh
```

Cuando el despliegue ya este estable, conviene congelar las versiones exactas instaladas y dejar ese lock guardado.

## Dos formas de corte

### Opcion A: paralela y mas segura

- Gunicorn escucha en `127.0.0.1:8001`
- Luego Nginx cambia el upstream
- Tiene mejor rollback

### Opcion B: corte directo sobre `kiadez.com`

- Gunicorn reemplaza al proceso actual
- Usa el mismo puerto interno que ya consume Nginx
- No requiere cambio de upstream si hoy Nginx ya apunta a `127.0.0.1:8000`
- Tiene menos pasos, pero mas riesgo operativo que la opcion A

Si tu prioridad es salir directo con el menor numero de movimientos, usa la opcion B.

## Fase 2A: preparar el nuevo servicio sin apagar el viejo

1. Copia el unit file de ejemplo:

```bash
sudo cp deploy/systemd/kiadez-backend-gunicorn.service.example /etc/systemd/system/kiadez-backend-gunicorn.service
```

2. Edita estas rutas si en tu servidor no coinciden:

- `User`
- `Group`
- `WorkingDirectory`
- `ExecStart`

3. Manten el bind en `127.0.0.1:8001` al inicio. Eso evita tocar el puerto actual.

4. Recarga systemd:

```bash
sudo systemctl daemon-reload
```

## Fase 3A: arrancar Gunicorn en paralelo

```bash
sudo systemctl start kiadez-backend-gunicorn
sudo systemctl status kiadez-backend-gunicorn
```

Valida salud:

```bash
scripts/check_backend_health.sh http://127.0.0.1:8001
```

Tambien revisa logs:

```bash
sudo journalctl -u kiadez-backend-gunicorn -n 200 --no-pager
```

## Fase 4A: prueba funcional antes del corte

Haz pruebas de navegacion reales apuntando temporalmente al nuevo puerto desde una maquina confiable o con tunel local:

- login
- feed
- home_user
- subida de imagen
- subida de video
- notificaciones

La validacion minima es:

- `200` en `/health`
- login correcto
- feed visible
- avatars cargando
- media publica visible

## Fase 5A: corte de trafico con Nginx

La forma segura es cambiar Nginx, no apagar primero el servicio viejo.

1. Localiza el `proxy_pass` actual y apuntalo a `127.0.0.1:8001`.
2. Conserva el servicio viejo vivo unos minutos.
3. Verifica config:

```bash
sudo nginx -t
```

4. Recarga Nginx:

```bash
sudo systemctl reload nginx
```

5. Observa errores y latencia:

```bash
sudo journalctl -u kiadez-backend-gunicorn -f
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Fase 6A: dejar estabilizar y retirar Uvicorn

Si el trafico ya entra por Gunicorn y todo se ve bien:

```bash
sudo systemctl disable --now kiadez-backend
sudo systemctl enable kiadez-backend-gunicorn
```

Es mejor no hacerlo de inmediato. Primero deja pasar una ventana corta de observacion.

## Fase 2B: corte directo sobre el puerto actual

Esta ruta es la que mas se parece a "actualizar proyecto y pasar en limpio a produccion".

Suposicion de esta variante:

- hoy Nginx ya apunta a `127.0.0.1:8000`
- hoy tu servicio actual ocupa ese puerto

Pasos:

1. Instala dependencias:

```bash
cd /srv/kiadez-backend/current
scripts/install_production_requirements.sh
```

2. Reemplaza el unit file actual por la variante de cutover:

```bash
sudo cp deploy/systemd/kiadez-backend-gunicorn-cutover.service.example /etc/systemd/system/kiadez-backend.service
```

3. Ajusta si hace falta:

- `User`
- `Group`
- `WorkingDirectory`
- `ExecStart`

4. Recarga systemd:

```bash
sudo systemctl daemon-reload
```

5. Reinicia el mismo servicio:

```bash
sudo systemctl restart kiadez-backend
sudo systemctl status kiadez-backend
```

6. Verifica salud publica e interna:

```bash
scripts/check_backend_health.sh http://127.0.0.1:8000
curl -i https://kiadez.com/health
```

7. Observa logs inmediatamente despues del corte:

```bash
sudo journalctl -u kiadez-backend -n 200 --no-pager
sudo journalctl -u kiadez-backend -f
sudo tail -f /var/log/nginx/error.log
```

Con esta variante, `kiadez.com` sigue entrando por el mismo Nginx y el mismo puerto interno. Lo unico que cambia es el proceso que atiende detras.

## Rollback rapido en corte directo

Si el corte directo falla y mantuviste copia del unit viejo:

```bash
sudo cp /etc/systemd/system/kiadez-backend.service.bak /etc/systemd/system/kiadez-backend.service
sudo systemctl daemon-reload
sudo systemctl restart kiadez-backend
```

Por eso el backup del unit file al inicio no es opcional.

## Rollback rapido

Si algo sale mal:

1. Reapunta Nginx al puerto viejo.
2. Recarga Nginx.
3. Si hace falta:

```bash
sudo systemctl stop kiadez-backend-gunicorn
sudo systemctl start kiadez-backend
```

Como Gunicorn corre en `8001`, el rollback es rapido y limpio.

## Ajustes iniciales recomendados

Para tu servidor actual (`8 GB RAM`, `4 vCPU`):

- `GUNICORN_WORKERS=3`
- `GUNICORN_TIMEOUT=60`
- `GUNICORN_KEEPALIVE=5`
- `GUNICORN_MAX_REQUESTS=2000`
- `GUNICORN_MAX_REQUESTS_JITTER=200`

Empezar con `3` workers es mas conservador que `4`, porque tambien compartes recursos con PostgreSQL, Nginx y el sistema.

## Cuando subir o bajar workers

Sube workers si:

- CPU disponible
- cola de peticiones
- workers ocupados con frecuencia

Baja workers si:

- sube mucho RAM
- PostgreSQL empieza a sufrir por demasiada concurrencia
- el servidor entra en swap

## Notas importantes

- `uvicorn-worker` es el camino recomendado hoy por la documentacion de Uvicorn.
- `uvicorn.workers` figura como deprecado en la documentacion oficial de Uvicorn.
- La aplicacion ya carga `.env` desde la raiz del proyecto, asi que el unit file puede seguir usando el mismo `WorkingDirectory`.
- Esta migracion mejora estabilidad y concurrencia, pero no sustituye la optimizacion de endpoints y del frontend.

## Comando de prueba manual

Sin tocar systemd, puedes hacer una prueba manual asi:

```bash
cd /srv/kiadez-backend/current
scripts/run_gunicorn.sh
```

Si quieres probar en otro puerto:

```bash
cd /srv/kiadez-backend/current
GUNICORN_BIND=127.0.0.1:8001 scripts/run_gunicorn.sh
```

## Ajustes de base de datos para multiworker

El backend ahora acepta estos parametros por entorno:

- `DATABASE_URL`
- `DB_ECHO`
- `DB_POOL_PRE_PING`
- `DB_POOL_SIZE`
- `DB_MAX_OVERFLOW`
- `DB_POOL_TIMEOUT_SECONDS`
- `DB_POOL_RECYCLE_SECONDS`

Valores iniciales razonables para tu servidor:

- `DB_POOL_PRE_PING=true`
- `DB_POOL_SIZE=4`
- `DB_MAX_OVERFLOW=2`
- `DB_POOL_RECYCLE_SECONDS=1800`
