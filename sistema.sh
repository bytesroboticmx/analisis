#!/usr/bin/env bash

fecha=$(date "+%Y-%m-%d %H:%M:%S")

echo "# Análisis rápido del sistema ($fecha)"
echo
echo "## Sistema operativo"
echo "- Nombre: $(uname -s)"
echo "- Kernel: $(uname -r)"
echo "- Arquitectura: $(uname -m)"
echo "- Hostname: $(uname -n)"
echo "- Usuario: $(whoami 2>/dev/null || echo $USER)"

if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    echo "- Distribución: $PRETTY_NAME"
fi

echo
echo "## CPU"
echo "- nproc (núcleos): $(nproc 2>/dev/null || echo 'no disponible')"
modelo=$(grep -m1 -E "(model name|Processor)" /proc/cpuinfo | cut -d: -f2 | sed 's/^ //')
[[ -n "$modelo" ]] && echo "- Modelo: $modelo"
if [[ -r /proc/loadavg ]]; then
    echo "- Carga media (1/5/15): $(cut -d' ' -f1-3 /proc/loadavg)"
else
    echo "- Carga media (1/5/15): no disponible"
fi

echo
echo "## Memoria"
if [[ -f /proc/meminfo ]]; then
    total=$(awk '/MemTotal/ {print int($2/1048576)}' /proc/meminfo)
    libre=$(awk '/MemFree/ {print int($2/1048576)}' /proc/meminfo)
    echo "- RAM total: ${total} GiB"
    echo "- RAM libre: ${libre} GiB"
else
    echo "- Memoria: no disponible"
fi

echo
echo "## Almacenamiento"
uso=$(df -h / | awk 'NR==2 {print "De:"$2" Usado:"$3" Libre:"$4" ("$5")"}')
echo "- Raíz (/): $uso"

echo
echo "## Uptime"
if [[ -f /proc/uptime ]]; then
    seg=$(awk '{print int($1)}' /proc/uptime)
    printf -- "- %d días, %d h, %d min\n" $((seg/86400)) $(((seg%86400)/3600)) $(((seg%3600)/60))
else
    uptime -p
fi
