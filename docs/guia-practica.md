# Guía práctica de Ghostty para tu trabajo de desarrollo

Tu punto de partida es una Mac con Ghostty, zsh, Starship, tmux y Lazygit.
Puedes seguir usando las interfaces de tus agentes y VS Code para notebooks.
Ghostty será el lugar donde organizas terminales, procesos, Git y conexiones.

**Empieza por el ejercicio de cinco minutos.** Después consulta Docker, SSH
o notebooks cuando los necesites. No tienes que aprender todo de una vez.

## Contenido

- [Qué hace cada herramienta](#qué-hace-cada-herramienta)
- [Tus primeros tres paneles](#tus-primeros-tres-paneles)
- [Cómo leer y escribir comandos](#cómo-leer-y-escribir-comandos)
- [Paneles de Ghostty y paneles de tmux](#paneles-de-ghostty-y-paneles-de-tmux)
- [Tu flujo diario de trabajo](#tu-flujo-diario-de-trabajo)
- [Git y Lazygit](#git-y-lazygit)
- [Un agente dentro de un panel](#un-agente-dentro-de-un-panel)
- [Docker con OrbStack](#docker-con-orbstack)
- [SSH y tus computadoras](#ssh-y-tus-computadoras)
- [ML y notebooks](#ml-y-notebooks)
- [Cómo salir y recuperar el control](#cómo-salir-y-recuperar-el-control)
- [Tu tarjeta de comandos](#tu-tarjeta-de-comandos)

## Qué hace cada herramienta

| Herramienta | Qué es | Ejemplo |
| --- | --- | --- |
| Ghostty | La aplicación que muestra tus terminales | Una ventana de macOS con texto y pestañas |
| zsh | El programa que interpreta tus comandos | Ejecuta `cd`, `git` o `docker` |
| Starship | La información que aparece antes de escribir | Proyecto, rama, Python y host remoto |
| tmux | Organiza terminales en sesiones, ventanas y paneles | Un espacio por proyecto con logs y comandos |
| Lazygit | Una interfaz de Git manejada con teclado | Revisar cambios, preparar commits y subirlos |
| Docker | Ejecuta aplicaciones en contenedores | PostgreSQL, Redis o una API |
| SSH | Abre una terminal en otra computadora | Ejecutar comandos en tu VM de GCP |
| Agente CLI | Un agente que funciona dentro de la terminal | Claude Code en uno de tus paneles |

Una **sesión tmux** es un espacio de trabajo, por ejemplo `mi-api`.
Dentro puede haber varias **ventanas tmux**, como pestañas internas.
Cada ventana puede dividirse en varios **paneles**, cada uno con su propia shell.

```text
Ventana de Ghostty
└── Sesión tmux: mi-api
    ├── Ventana 1: desarrollo
    │   ├── Panel de terminal local
    │   ├── Panel conectado por SSH
    │   └── Panel con un agente CLI
    └── Ventana 2: pruebas
```

Esto permite una distribución como la que viste con Milton. Un menú que enumera
computadoras guardadas es otra función: podría venir de Kitmux, Herdr u otra
herramienta. **Tu instalación actual tiene selector de sesiones tmux, pero no
un menú de computadoras SSH.** No se puede identificar la herramienta exacta
que viste únicamente por su apariencia descrita.

## Tus primeros tres paneles

Este ejercicio usa tu repositorio de dotfiles, sin editar archivos ni lanzar agentes.

### Paso 1 Abre una sesión

Abre Ghostty. Si estaba abierto desde antes de la instalación, pulsa
**Cmd+Shift+,** para recargar y abre una ventana nueva con **Cmd+n**.

Escribe una línea, pulsa Enter y luego la siguiente:

```sh
dots
tp practica
```

`dots` entra a tus dotfiles. `tp practica` crea la sesión `practica` o vuelve a
ella si ya existe. Verás una barra superior con el nombre de la sesión.

### Paso 2 Divide la ventana

En esta guía, **Ctrl-a → tecla** significa:

1. Mantén Control y pulsa `a`.
2. Suelta ambas teclas.
3. Pulsa la tecla indicada.

No se escribe `Ctrl-a` como texto ni se mantiene presionado mientras haces todo.

Pulsa **Ctrl-a → |** para dividir a izquierda y derecha. Después, estando en
el panel derecho, pulsa **Ctrl-a → -** para dividirlo en dos.

```text
┌───────────────────────────┬───────────────────────────┐
│                           │ Panel 2                   │
│ Panel 1                   │ Logs, pruebas o SSH       │
│ Terminal principal        ├───────────────────────────┤
│ y revisión de Git         │ Panel 3                   │
│                           │ Agente o más comandos     │
└───────────────────────────┴───────────────────────────┘
```

Puedes hacer clic en un panel para seleccionarlo. También puedes usar
**Ctrl-a → flecha**. Cada panel se inicia en la carpeta del panel que dividiste.

Si no encuentras `|` en tu teclado, ejecuta esto dentro de tmux:

```sh
tmux split-window -h -c "$PWD"
```

Para dividir arriba y abajo por comando:

```sh
tmux split-window -v -c "$PWD"
```

### Paso 3 Comprueba qué hace cada panel

En el panel izquierdo:

```sh
git status
```

En el derecho superior:

```sh
pwd
```

En el derecho inferior:

```sh
hostname
```

Por ahora todos son terminales en tu Mac. Dividir la pantalla no conecta
automáticamente una VM ni inicia un agente.

Pulsa **Ctrl-a → g**: Lazygit aparece encima. Pulsa `q` para volver a los paneles.
Pulsa **Ctrl-a → z** para ampliar el panel seleccionado y repítelo para restaurarlo.

### Paso 4 Sal y vuelve

Pulsa **Ctrl-a → d**. Sales de la vista de tmux, pero dejas abierta la sesión.
Desde la terminal normal:

```sh
tl
ta practica
```

Deberías volver a tus tres paneles. Esta es la diferencia entre desconectarte
de una sesión y terminar sus procesos.

## Cómo leer y escribir comandos

El prompt usa bloques oscuros: arriba aparecen el entorno detectado (Node,
Python o Conda) y la carpeta; debajo, la rama Git en verde. El bloque de cambios
solo aparece si hay algo que indicar: `mod:2` son dos archivos modificados,
`+1` es un archivo preparado, `?1` uno sin seguimiento y `↑1` un commit por subir.
La línea con `❯` es donde escribes. Si el comando anterior falló, cambia a rojo.
Fuera de un repositorio no aparece la fila de Git. Los bloques usan la fuente
Menlo existente y son rectangulares; no necesitan instalar fuentes adicionales.

### Sugerencias mientras escribes

Abre una terminal nueva para cargar esta configuración. Si ya estás en un panel
de tmux, ejecuta `exec zsh` cuando estés en el prompt para recargar ese panel.

- **Texto gris:** es una sugerencia. Pulsa **flecha derecha** con el cursor al
  final del texto para aceptarla. **Enter** ejecuta el comando.
- **Tab:** completa comandos, opciones y rutas. En el frontend, escribe
  `npm run ` y pulsa Tab para ver los scripts de su `package.json`; por ejemplo,
  `npm run d` + Tab completa `dev` si es la única coincidencia.
- **uv:** `uv r` + Tab completa el subcomando; las opciones y rutas se completan
  según lo que soporte uv. Tras ejecutar `uv run python train.py`, podrás recuperar
  esa línea escribiendo su comienzo, si ese archivo existe en tu proyecto.
- **Ctrl-r:** sigue buscando en tu historial general con fzf; Escape cancela.

Las sugerencias recuerdan primero lo que ejecutaste **en esa carpeta exacta**.
Por ejemplo, después de usar `npm run dev` en frontend y `npm run build` en otra
carpeta, escribir `npm run ` prioriza el comando propio de cada carpeta.
Si aún no hay historial local que coincida, se busca en el historial general y
en los completados. No se ejecutan comandos al mostrar o aceptar sugerencias.

Atuin empieza a aprender la ubicación de los comandos desde esta configuración;
el historial antiguo de zsh no contiene esa información. El historial nuevo se
guarda localmente fuera de Git, sin cuenta ni sincronización. Funciona dentro y
fuera de tmux. Las herramientas npm/uv deben estar instaladas para sus completados.

### Teclas y rutas básicas

| Elemento | Significa |
| --- | --- |
| `~` | Tu carpeta de usuario |
| `.` | La carpeta actual |
| `..` | La carpeta superior |
| `cd carpeta` | Cambiar de carpeta |
| `pwd` | Mostrar la carpeta actual |
| `ls` / `ls -la` | Listar archivos / incluir ocultos y detalles |
| Tab | Completar una ruta o comando |
| Flecha arriba | Recuperar un comando anterior |
| Ctrl-r | Buscar en tu historial con fzf |
| Ctrl-c | Interrumpir el comando que está en primer plano |

Los nombres en MAYÚSCULAS, como `ALIAS_VM` o `PROYECTO_GCP`, son marcadores:
reemplázalos por tus valores. Los archivos `train.py`, `app.main` y los servicios
`api` o `db` son ejemplos; deben existir en tu proyecto.

Para abrir una carpeta que tiene espacios, usa comillas:

```sh
cd "$HOME/Documents/personal-github/Mi Proyecto"
```

Después de visitar una carpeta, zoxide aprende su ubicación. Puedes probar
`z parte-del-nombre`; con `zi` eliges una carpeta de una lista. `Ctrl-t` busca
archivos e inserta su ruta en el comando, pero no los abre automáticamente.

## Paneles de Ghostty y paneles de tmux

Ghostty puede dividir ventanas por sí mismo. Son útiles para algo rápido:

| Atajo de Ghostty | Acción |
| --- | --- |
| Cmd+d | Dividir a los lados |
| Cmd+Shift+d | Dividir arriba y abajo |
| Cmd+[ / Cmd+] | Panel anterior / siguiente |
| Cmd+Shift+Enter | Ampliar o restaurar un panel de Ghostty |
| Cmd+t | Nueva pestaña de Ghostty |
| Cmd+n | Nueva ventana de Ghostty |
| Cmd+p | Mostrar u ocultar la terminal rápida, con Ghostty enfocado |
| Cmd+c / Cmd+v | Copiar la selección / pegar |
| Cmd+, | Abrir configuración |

Para tus proyectos, usa **una sesión tmux y sus divisiones internas**. Así
puedes volver a la misma sesión. Mezclar muchos paneles de Ghostty con muchos
paneles tmux hace más difícil recordar qué atajo controla cada uno.

Dentro de tmux, tus atajos son:

| Después de Ctrl-a | Acción |
| --- | --- |
| `\|` / `-` | Dividir a los lados / arriba y abajo |
| Flecha o `h j k l` | Seleccionar panel |
| `H J K L` | Cambiar el tamaño del panel |
| `z` | Ampliar/restaurar panel |
| `g` | Abrir Lazygit en una ventana emergente |
| `c` | Crear otra ventana tmux |
| `,` | Renombrar la ventana tmux |
| `1`…`9` | Elegir ventana tmux |
| `s` | Elegir sesión de este servidor tmux |
| `d` | Desconectarse de la sesión |
| `[` | Entrar al historial; `q` o Escape vuelve al modo normal |
| `r` | Recargar tu configuración tmux |
| `?` | Consultar todos los atajos |

Para copiar desde el historial: **Ctrl-a → [**, navega con flechas, pulsa `v`
para comenzar la selección y `y` para copiar al portapapeles de macOS.

Los atajos corresponden a [tu configuración de tmux](../home/dot_tmux.conf).
Los atajos de Ghostty se pueden consultar en su paleta con **Cmd+Shift+p**.

## Tu flujo diario de trabajo

### Al abrir un proyecto

Desde una terminal nueva, entra a la carpeta real del proyecto:

```sh
cd "$HOME/Documents/personal-github/MI_PROYECTO"
git status
tp
```

`tp` sin nombre identifica la sesión con la carpeta y un número derivado de
su ruta. Puedes usar `tp mi-api` si prefieres un nombre elegido por ti. Un nombre
explícito reutiliza la misma sesión aunque lo ejecutes desde otra carpeta.

Si es una tarea nueva y corresponde crear una rama, hazlo después de revisar
el estado del repositorio:

```sh
git switch -c tarea/mi-cambio
```

### Mientras desarrollas

| Lugar | Trabajo |
| --- | --- |
| Tu interfaz de agente | Pedir cambios y conversar sobre la implementación |
| Panel principal de tmux | Comandos del proyecto y revisión con Lazygit |
| Segundo panel | Servidor de desarrollo o logs |
| Tercer panel | Tests, scripts o un agente CLI opcional |
| VS Code | Notebooks, `.env` y edición manual cuando te resulte cómoda |

Antes de pedir cambios, comprueba que el agente y la terminal apunten a la
**misma carpeta o worktree**. Un agente puede tener su propio checkout.
Si está modificando otra carpeta, `lg` en la tuya no mostrará sus cambios.

Ejemplo: el agente modifica una API; tú observas logs en un panel, ejecutas
las pruebas del proyecto en otro y revisas el diff con **Ctrl-a → g**.
No necesitas cambiar de interfaz de agente para adoptar este flujo.

### Al terminar

Revisa los cambios, ejecuta las pruebas del proyecto y crea el commit con
Lazygit. Si quieres dejar procesos funcionando, usa **Ctrl-a → d**. Si ya no
los necesitas, detén cada proceso antes de salir. La Mac debe permanecer
encendida y despierta para que sigan ejecutándose.

## Git y Lazygit

Abre Lazygit desde la carpeta correcta con `lg` o **Ctrl-a → g** dentro de tmux.

| Tecla en Lazygit | Acción |
| --- | --- |
| Flechas | Moverte entre elementos y paneles |
| Tab / Shift+Tab | Cambiar de panel |
| Espacio, sobre un archivo en Files | Preparar o retirar ese archivo del commit |
| Enter | Entrar al detalle seleccionado |
| `c`, en Files | Escribir un mensaje y crear un commit con lo preparado |
| `P` mayúscula | Push: subir commits |
| `p` minúscula | Pull: traer e integrar cambios remotos |
| `?` | Ayuda de las teclas disponibles |
| Escape | Volver o cerrar un diálogo |
| `q` | Salir de Lazygit |

**Preparar un cambio** —hacer stage— significa elegir qué entrará al siguiente
commit. El commit lo guarda en Git local. El push lo envía a GitHub.

Tu rutina: selecciona un archivo, lee su diff, pulsa Espacio si debe entrar
al commit, repite con los demás, pulsa `c` y finalmente `P` cuando quieras subirlo.
Si hay conflictos o cambios ajenos sin entender, revisa antes de confirmar.

El equivalente por comandos, sustituyendo la ruta por un archivo real:

```sh
git status
git diff
git add RUTA_DEL_ARCHIVO
git diff --cached
git commit -m "feat: describe el cambio"
git push
```

En una rama nueva, el primer push puede necesitar:

```sh
git push -u origin HEAD
```

Para comprobar la identidad de este proyecto:

```sh
git config --show-origin --get user.email
git remote -v
```

Los repositorios bajo `Documents/personal-github` usan tu identidad personal.
Se conservaron las reglas laborales existentes. Esa identidad firma tus commits;
el acceso al remoto depende de la autenticación HTTPS o SSH.

Si trabajas con `.env`, comprueba que el proyecto lo ignore antes de preparar
cambios: `git check-ignore -v .env`. Que no aparezca una regla requiere revisar
el `.gitignore`; los dotfiles no añaden exclusiones a todos tus proyectos.

## Un agente dentro de un panel

Para reproducir el panel de agente que recuerdas, ejecutas la versión CLI
del agente dentro de uno de los paneles. En tu Mac ya está instalado Claude Code.
Desde el panel y la carpeta del proyecto:

```sh
claude
```

Cuando aparezca su interfaz, escribe por ejemplo:

> Explícame cómo se ejecuta este proyecto y qué comando corre sus pruebas.

Dentro de Claude, `/help` muestra ayuda y `/exit` termina la sesión de la CLI.
Desde la shell, `claude -c` continúa la conversación más reciente de esa carpeta.
La primera ejecución puede pedir autenticación. [Guía oficial de Claude Code](https://code.claude.com/docs/en/quickstart).

Para ir del agente a otro panel usa **Ctrl-a → flecha**. La interfaz gráfica
de una aplicación no se convierte en panel de terminal; lo que aparece dentro
es su cliente CLI. Puedes mantener tu flujo gráfico y usar este panel solo cuando
te sea útil.

### Varios agentes sobre el mismo repositorio

Dos paneles en la misma carpeta comparten archivos. Si dos agentes hacen tareas
independientes, usa distintas carpetas de trabajo. Git lo permite sin instalar
Worktrunk. Desde el repositorio, este ejemplo crea una rama y un worktree hermano:

```sh
git worktree add ../MI_PROYECTO-agente-2 -b tarea/agente-2
```

Abre esa carpeta en el segundo agente y su terminal. Si tu interfaz ya crea
worktrees, usa las rutas que genera. Una carpeta separada no separa automáticamente
puertos ni bases de datos compartidas: cada ejecución necesita sus ajustes.

## Docker con OrbStack

Tu Mac usa el contexto Docker `orbstack`. Abre OrbStack cuando necesites que
funcione su motor de contenedores. Puedes seguir usando su interfaz para observarlos.

```sh
docker context show
docker ps
docker compose version
```

El contexto indica a qué motor Docker le estás enviando comandos. `docker ps`
lista sus contenedores activos. Si cambias a un contexto remoto, ya no estarás
administrando necesariamente contenedores locales. [Contextos de Docker](https://docs.docker.com/reference/cli/docker/context/show/).

### Levantar los servicios de un proyecto

Entra a la carpeta que contiene `compose.yaml` o `docker-compose.yml`.
Estos comandos requieren que el proyecto tenga esa configuración:

```sh
docker compose config --services
docker compose up -d
docker compose ps
```

El primero muestra los nombres de servicios. `up -d` los inicia en segundo
plano. Si necesitas reconstruir una imagen porque cambió su código o Dockerfile,
usa `docker compose up -d --build`. [Referencia de compose up](https://docs.docker.com/reference/cli/docker/compose/up/).

En otro panel observa los logs:

```sh
docker compose logs -f --tail=100
```

O solo los de un servicio, sustituyendo `api` por su nombre real:

```sh
docker compose logs -f --tail=100 api
```

**Ctrl-c aquí deja de seguir los logs; no detiene los servicios que arrancaste
con `up -d`.** En cambio, si ejecutas `docker compose up` sin `-d`, Ctrl-c
detiene esa ejecución y sus contenedores. [Logs](https://docs.docker.com/reference/cli/docker/compose/logs/), [up](https://docs.docker.com/reference/cli/docker/compose/up/).

Para abrir una shell dentro de un servicio que ya está corriendo:

```sh
docker compose exec api sh
```

`exit` sale de esa shell y vuelve a tu terminal anterior. Esto requiere que
la imagen incluya `sh`. [Referencia de compose exec](https://docs.docker.com/reference/cli/docker/compose/exec/).

Para detener servicios conservando sus contenedores usa `docker compose stop`.
`docker compose down` los detiene y elimina contenedores y redes del proyecto.
Los datos duraderos deben estar en volúmenes o carpetas montadas; no en la capa
del contenedor. **No añadas `-v` a `down` si quieres conservar los volúmenes
nombrados de tus bases de datos.** [Referencia de compose down](https://docs.docker.com/reference/cli/docker/compose/down/).

Un layout cómodo: panel izquierdo para comandos, derecho superior con logs y
derecho inferior para pruebas o el agente. Lazygit se abre encima con Ctrl-a → g.

## SSH y tus computadoras

### Conectarte desde un panel

Si el destino de VS Code está definido como `Host` en tu archivo `~/.ssh/config`,
puedes usar ese mismo alias desde Ghostty:

```sh
ssh ALIAS_VM
```

También existe la forma `ssh USUARIO@HOST`. Necesitas el usuario, la dirección,
la autenticación y acceso de red configurados para ese servidor.

Después de conectar, comprueba dónde estás:

```sh
hostname
pwd
whoami
```

Los comandos de ese panel se ejecutan ahora en la VM; los otros paneles siguen
en la Mac. `exit` cierra la shell remota y te devuelve a la shell local.
Conectar no copia el proyecto: debe estar disponible también en la VM.
[Referencia de OpenSSH](https://man.openbsd.org/ssh).

El selector **Ctrl-a → s** lista sesiones de un servidor tmux, no todas tus
computadoras. Un menú de máquinas guardadas se podría añadir cuando definamos
tus destinos reales. El acceso entre redes con Tailscale tampoco está configurado
por estos dotfiles.

### Conectarte a GCP

En tu Mac ya existe `gcloud`. Si tu acceso usa Google Cloud CLI, sustituye los
nombres y usa:

```sh
gcloud compute instances list --project=PROYECTO_GCP
gcloud compute ssh NOMBRE_VM --zone=ZONA --project=PROYECTO_GCP
```

Si tu organización utiliza IAP, el comando puede necesitar `--tunnel-through-iap`
y sus permisos correspondientes. Reutiliza el método de acceso autorizado que
ya usas para esa VM. `gcloud compute ssh` puede preparar las claves necesarias
según la configuración de la cuenta y la instancia. [Referencia oficial de gcloud](https://docs.cloud.google.com/sdk/gcloud/reference/compute/ssh).

### Dejar un proceso en la VM y reconectar

**tmux tiene que correr en la VM para conservar un proceso remoto al perder SSH.**
Un tmux local que contiene `ssh` conserva el cliente local, pero no garantiza
la supervivencia del proceso remoto si se corta la conexión.

Para empezar, abre una pestaña nueva de Ghostty con Cmd+t, conecta por SSH y
comprueba `command -v tmux`. Si falta, instálalo con el gestor del servidor o
pídelo al administrador. No ejecutes nuestro instalador de macOS en Linux.

Una vez dentro de la VM:

```sh
tmux new-session -A -s ml
```

En un servidor con configuración estándar, el prefijo es **Ctrl-b**, no Ctrl-a.
Ejecuta tu trabajo dentro de esa sesión. Después usa **Ctrl-b → d** para
desconectarte de tmux y `exit` para cerrar SSH.

Para volver otro día, conecta de nuevo y ejecuta:

```sh
tmux attach-session -t ml
```

La sesión y sus procesos siguen en la VM mientras esta permanezca encendida,
el servidor tmux siga vivo y no se hayan terminado los procesos. No sobreviven
a un reinicio. [Guía de tmux](https://github.com/tmux/tmux/wiki/Getting-Started).

Los alias `tp`, `ta` y `lg` son locales de tu Mac: no aparecen automáticamente
en la VM. Usa allí los comandos completos o su propia configuración.

## ML y notebooks

### Desarrollo local

Continúa usando VS Code para editar notebooks y escoger su kernel. En tmux
puedes ejecutar entrenamientos, evaluaciones o mirar logs.

Si tu proyecto ya tiene un entorno `.venv`, actívalo en cada panel donde lo
necesites:

```sh
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
```

Activarlo en un panel no lo activa en los demás. Si usas Conda, selecciona tu
entorno con su comando habitual. El prompt de Starship ayuda a ver el entorno.
El kernel de VS Code se selecciona aparte.

En un proyecto que contenga `train.py` y sus dependencias instaladas:

```sh
python -u train.py
```

Puedes dejarlo en una sesión tmux y desconectarte. La opción `-u` permite ver
la salida de Python sin el buffering habitual. Cerrar o dormir la Mac no la
convierte en un servidor que continúa trabajando: para eso usa una máquina
encendida o una VM, con los procesos ejecutándose allí.

### Notebook remoto desde tu Mac

Tu opción habitual sigue siendo VS Code Remote SSH con las extensiones y el
entorno Python en el servidor. Revisa que el kernel elegido sea el remoto.
[VS Code Remote SSH](https://code.visualstudio.com/docs/remote/ssh).

Si prefieres JupyterLab en el navegador, dentro del entorno remoto que tenga
JupyterLab instalado, y opcionalmente dentro de tmux:

```sh
python -m jupyterlab --no-browser --ip=127.0.0.1 --port=8888
```

Desde **otra terminal local en la Mac**, abre un túnel:

```sh
ssh -N -L 127.0.0.1:8888:127.0.0.1:8888 ALIAS_VM
```

Abre `http://127.0.0.1:8888` en tu navegador y usa el token que muestra Jupyter.
La terminal del túnel permanece ocupada mientras lo mantiene abierto. Ctrl-c
cierra el túnel; el Jupyter remoto puede seguir corriendo dentro de tmux.
Si Jupyter elige otro puerto por estar ocupado, ajusta el túnel al puerto real.
[Jupyter Server](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html), [túneles SSH](https://man.openbsd.org/ssh).

## Cómo salir y recuperar el control

| Situación | Qué hacer |
| --- | --- |
| Hay un comando ejecutándose y quieres detenerlo | Ctrl-c en ese panel |
| Estás dentro de Lazygit | Escape para cerrar diálogos; `q` para salir |
| Estás dentro de Claude Code | `/exit` |
| Estás en el historial de tmux y parece que no puedes escribir | `q` o Escape |
| Quieres dejar tus procesos y salir de tmux | Ctrl-a → d en la Mac |
| Quieres cerrar una shell que está libre | `exit`; en tmux cierra ese panel |
| Quieres volver a una sesión local | `tl`, luego `ta NOMBRE` |
| No sabes si estás dentro de tmux | `printenv TMUX`; vacío normalmente significa que no |
| No sabes en qué máquina estás | `hostname` |
| No sabes en qué carpeta estás | `pwd` |
| Docker dice que no puede conectar con el daemon | Abre OrbStack y comprueba `docker context show` |
| Compose dice que falta configuración | Entra a la carpeta con el archivo Compose |
| Un puerto está ocupado | Identifica el proceso con `lsof -nP -iTCP:8000 -sTCP:LISTEN`, cambiando el puerto |
| `tp` o `lg` no existen | Abre una terminal nueva en tu Mac; en una VM los alias no están instalados |
| Git no muestra los cambios del agente | Comprueba que estás en el mismo repo y worktree |
| El panel remoto no entiende Ctrl-a | Su tmux puede usar Ctrl-b o una configuración propia |

Para cerrar una sesión de práctica definitivamente, termina sus shells con
`exit`, una por una. No cierres paneles con trabajos que quieras conservar.
Desconectarse con `d` y terminar con `exit` son acciones distintas.

## Tu tarjeta de comandos

Lo que necesitas memorizar primero:

| Quiero | Uso |
| --- | --- |
| Ir a dotfiles | `dots` |
| Encontrar un proyecto visitado | `z nombre` o `zi` |
| Abrir mi espacio de trabajo | `tp` |
| Dividir a los lados / arriba y abajo | Ctrl-a → `\|` / Ctrl-a → `-` |
| Moverme entre paneles | Clic o Ctrl-a → flecha |
| Revisar Git | `lg` o Ctrl-a → `g` |
| Ampliar un panel | Ctrl-a → `z` |
| Dejar todo abierto y salir | Ctrl-a → `d` |
| Volver | `tl` y `ta nombre` |
| Levantar servicios de un proyecto Compose | `docker compose up -d` |
| Seguir sus logs | `docker compose logs -f --tail=100` |
| Abrir una terminal remota | `ssh ALIAS_VM` |
| Recuperar un comando | Ctrl-r |

Primera práctica: crea tres paneles, abre y cierra Lazygit, desconéctate y vuelve.
Después usa ese mismo esquema en un proyecto real. SSH y los agentes dentro de
paneles son pasos adicionales, no requisitos para empezar.
