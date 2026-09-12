#!/usr/bin/env python3
#Descripcion:
#Nombre:
#Matricula:
#Grupo:
#Fecha:
"""Analiza el sistema operativo actual y guarda el resultado en sistema.md."""

import datetime
import os
import platform
import shutil
import subprocess
import sys


def leer_proc(ruta, por_linea=False):
    try:
        with open(ruta) as f:
            contenido = f.read().strip()
        return contenido.splitlines() if por_linea else contenido
    except (OSError, IOError):
        return None


def ejecutar(cmd):
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        return None


def main():
    lineas = []
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    system = platform.system()
    is_linux_like = system in ("Linux", "Android")
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    uname = getattr(os, "uname", lambda: None)()
    nodo = uname.nodename if uname else platform.node()
    usuario = os.environ.get("USER") or ejecutar(["whoami"]) or "desconocido"

    lineas.append(f"# Análisis del sistema ({ahora})")
    lineas.append("")

    lineas.append("## Sistema operativo")
    lineas.append(f"- Nombre: {system}")
    lineas.append(f"- Distribución: {platform.platform()}")
    lineas.append(f"- Versión: {version}")
    lineas.append(f"- Kernel: {release}")
    lineas.append(f"- Arquitectura: {machine}")
    lineas.append(f"- Hostname: {nodo}")
    lineas.append(f"- Usuario: {usuario}")

    if is_linux_like:
        os_release = leer_proc("/etc/os-release", por_linea=True) or []
        for ln in os_release:
            if ln.startswith(("PRETTY_NAME=", "NAME=")):
                lineas.append(f"- Distribución (os-release): {ln.split('=', 1)[1].strip(chr(34))}")
                break

    lineas.append("")

    lineas.append("## CPU")
    cpu_path = "/proc/cpuinfo"
    if os.path.exists(cpu_path) and is_linux_like:
        cpuinfo = leer_proc(cpu_path, por_linea=True)
        modelos = [l.split(":", 1)[1].strip() for l in cpuinfo if l.startswith("model name")]
        if not modelos:
            modelos = [l.split(":", 1)[1].strip() for l in cpuinfo if l.startswith("Processor")]
        n_nucleos = sum(1 for l in cpuinfo if l.startswith("processor"))
        upline = [l for l in cpuinfo if l.startswith("CPU implementer")]
        if n_nucleos:
            lineas.append(f"- Núcleos visibles: {n_nucleos}")
        if modelos:
            lineas.append(f"- Modelo: {modelos[0]}")
        if upline:
            lineas.append(f"- Implementer (ARM): {upline[0].split(':', 1)[1].strip()}")
    else:
        lineas.append(f"- Procesador: {platform.processor()}")

    nproc = ejecutar(["nproc"])
    if nproc:
        lineas.append(f"- nproc (núcleos): {nproc}")

    load = leer_proc("/proc/loadavg")
    if load:
        lineas.append(f"- Carga media (1/5/15 min): {load.split()[0]} / {load.split()[1]} / {load.split()[2]}")

    lineas.append("")

    lineas.append("## Memoria")
    memfile = "/proc/meminfo" if is_linux_like and os.path.exists("/proc/meminfo") else None
    if memfile:
        mem = {}
        for ln in leer_proc(memfile, por_linea=True):
            partes = ln.replace("kB", "").split(":")
            if len(partes) == 2:
                mem[partes[0].strip()] = int(partes[1].strip()) * 1024
        total = mem.get("MemTotal", 0)
        libre = mem.get("MemFree", 0)
        swaptotal = mem.get("SwapTotal", 0)
        lineas.append(f"- RAM total: {total / (1024**3):.2f} GiB ({total / 1024**2:.0f} MiB)")
        lineas.append(f"- RAM libre: {libre / (1024**3):.2f} GiB")
        if total:
            usada = total - libre
            lineas.append(f"- RAM en uso: {usada / (1024**3):.2f} GiB ({usada / total * 100:.1f}%)")
        if swaptotal:
            lineas.append(f"- Swap total: {swaptotal / (1024**3):.2f} GiB")
    else:
        lineas.append("- Memoria total: no disponible")
        lineas.append("- RAM libre: no disponible")

    lineas.append("")

    lineas.append("## Almacenamiento")
    uso = shutil.disk_usage("/")
    lineas.append(f"- Espacio total en /: {uso.total / (1024**3):.2f} GiB")
    lineas.append(f"- Espacio usado en /: {uso.used / (1024**3):.2f} GiB")
    lineas.append(f"- Espacio libre en /: {uso.free / (1024**3):.2f} GiB")
    lineas.append(f"- Uso de /: {uso.used / uso.total * 100:.1f}%")

    lineas.append("")

    lineas.append("## Tiempo de actividad (uptime)")
    uptime = leer_proc("/proc/uptime") if is_linux_like else None
    if uptime:
        segundos = round(float(uptime.split()[0]))
        dias, resto = divmod(segundos, 86400)
        horas, resto = divmod(resto, 3600)
        minutos, seg = divmod(resto, 60)
        lineas.append(f"- {dias} días, {horas} horas, {minutos} minutos, {seg} segundos ({segundos} s)")
    else:
        hijack = ejecutar(["/usr/bin/uptime", "-p"]) or ejecutar(["uptime", "-p"])
        lineas.append(f"- {hijack or 'desconocido'}")

    lineas.append("")

    lineas.append("## Python")
    lineas.append(f"- Versión: {platform.python_version()}")
    lineas.append(f"- Ejecutable: {sys.executable}")

    lineas.append("")

    lineas.append("## Fecha del análisis")
    lineas.append(f"- {ahora}")

    contenido = "\n".join(lineas) + "\n"

    ruta = os.path.join(os.path.expanduser("~"), "sistema.md")
    with open(ruta, "w") as f:
        f.write(contenido)

    print(f"Análisis guardado en: {ruta}")


if __name__ == "__main__":
    main()
