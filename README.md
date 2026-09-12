# Análisis del sistema

Herramientas para analizar el sistema operativo y guardar el resultado de forma estructurada. Incluye dos implementaciones equivalentes: una en Python y otra en Bash.

## Contenido

| Archivo | Lenguaje | Salida |
| --- | --- | --- |
| `analisis_sistema.py` | Python 3 | `~/sistema.md` |
| `sistema.sh` | Bash | stdout (consola) |

## `analisis_sistema.py`

Script en Python que recopila información del sistema y la guarda en `~/sistema.md` (Markdown).

### Requisitos

- Python 3.6 o superior.
- Sin dependencias externas: usa solo la biblioteca estándar.

### Uso

```bash
python3 analisis_sistema.py
```

Al terminar imprime la ruta del archivo generado:

```
Análisis guardado en: /home/usuario/sistema.md
```

### Datos que recopila

- **Sistema operativo:** nombre, distribución (via `/etc/os-release`), versión, kernel, arquitectura, hostname y usuario.
- **CPU:** núcleos visibles (`/proc/cpuinfo` y `nproc`), modelo (x86/ARM) e implementer (ARM), carga media 1/5/15 minutos (`/proc/loadavg`).
- **Memoria:** RAM total, libre y en uso, y swap (`/proc/meminfo`).
- **Almacenamiento:** espacio total, usado y libre en `/` (`shutil.disk_usage`).
- **Uptime:** tiempo de actividad desde `/proc/uptime` (o `uptime -p` como alternativa).
- **Python:** versión y ejecutable en uso.
- **Fecha del análisis.**

### Funciones internas

| Función | Descripción |
| --- | --- |
| `leer_proc(ruta, por_linea=False)` | Lee archivos de `/proc` de forma segura; devuelve `None` si fallan. |
| `ejecutar(cmd)` | Ejecuta un comando con límite de 10 s; devuelve stdout o `None`. |
| `main()` | Orquesta la recopilación y escribe el archivo de salida. |

### Notas

- Diseñado para sistemas tipo Unix/Linux; usa los archivos de `/proc`.
- En sistemas no Linux usa `platform.processor()` como alternativa para la CPU.

## `sistema.sh`

Script en Bash que genera un análisis rápido del sistema en la consola (stdout) sin escribir archivos.

### Requisitos

- Bash 4 o superior.
- Herramientas estándar: `uname`, `nproc`, `date`, `grep`, `awk`, `df`, `uptime`.
- En Termux/Android la detección de CPU y `/proc/meminfo` puede variar.

### Uso

```bash
bash sistema.sh
```

### Datos que recopila

- **Sistema operativo:** nombre, kernel, arquitectura, hostname, usuario y distribución (`/etc/os-release`).
- **CPU:** número de núcleos (`nproc`), modelo, carga media 1/5/15.
- **Memoria:** RAM total y libre (`/proc/meminfo`, en GiB).
- **Almacenamiento:** uso de `/` vía `df -h`.
- **Uptime:** tiempo de actividad desde `/proc/uptime`.

## Comparación

| Característica | `analisis_sistema.py` | `sistema.sh` |
| --- | --- | --- |
| Salida | Archivo Markdown | Consola |
| Detalle | Más completo (swap, % de uso) | Rápido y mínimo |
| Dependencias | Solo stdlib | Herramientas CLI |