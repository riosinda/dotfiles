# Dotfiles de Inda

Entorno de desarrollo para macOS, instalado en el disco interno. Ghostty y zsh
con Starship, fzf, zoxide, ripgrep, fd, jq, Lazygit/delta y tmux. Los agentes
siguen usando sus propias interfaces y configuraciones.

**Empieza aquí:** [Guía práctica desde cero: paneles, Git, Docker, SSH y agentes](docs/guia-practica.md).

## Instalar en otra Mac

Requisitos: Homebrew, Git y Python 3 (Command Line Tools o Homebrew).

```sh
mkdir -p "$HOME/Documents/personal-github"
git clone https://github.com/riosinda/dotfiles.git "$HOME/Documents/personal-github/dotfiles"
cd "$HOME/Documents/personal-github/dotfiles"
./install.sh
```

El instalador usa `brew bundle --no-upgrade`: instala herramientas faltantes,
sin una actualización general. Homebrew puede instalar o actualizar dependencias
necesarias. Ghostty se instala en Applications; las herramientas, en Homebrew.
Ninguna configuración depende de un volumen externo.

La primera vez pregunta el nombre y correo personales si no existen en
`~/.gitconfig-personal` o `~/.config/git/personal.gitconfig`. También puedes
proporcionarlos con `DOTFILES_GIT_NAME` y `DOTFILES_GIT_EMAIL`. Se guardan
localmente, fuera del repositorio. La autenticación de GitHub se configura
por separado: por ejemplo, con `gh auth login` y `gh auth setup-git`, o con
tus claves y aliases SSH existentes. Las claves privadas nunca se copian aquí.

Abre una terminal nueva tras instalar. En Ghostty: `Cmd+Shift+,` recarga la
configuración. Si una opción de ventana no cambia, abre una ventana nueva.

## Qué configura

| Herramienta | Configuración |
| --- | --- |
| Ghostty | Mellifluous, Menlo 14, márgenes, controles de macOS y terminal rápida |
| zsh | Conserva Oh My Zsh y tus rutas; sustituye el prompt anterior por Starship |
| Starship | Carpeta, rama/estado Git, Python/Conda, duración y host por SSH |
| fzf | Búsqueda de historial, archivos y carpetas |
| zoxide | Navegación con `z` y selección con `zi` |
| Git | delta para diffs e identidad personal por carpeta |
| Lazygit | Interfaz de Git con delta; sin IA ni servicios de API |
| tmux | Sesiones por proyecto, paneles, ratón, copiar y popup de Lazygit |

Los archivos de `home/` son administrados con chezmoi en modo archivo:
las configuraciones activas se copian a tu usuario. `~/.zshrc` y `~/.gitconfig`
no se versionan completos: el instalador los integra conservando lo demás.
Para nuevos equipos, no instala Oh My Zsh ni Powerlevel10k; zsh funciona sin ellos.

## Uso diario

| Acción | Comando / atajo |
| --- | --- |
| Ir a dotfiles | `dots` |
| Saltar a una carpeta visitada | `z parte-del-nombre` |
| Elegir carpeta visitada | `zi` |
| Buscar historial | `Ctrl-r` |
| Buscar archivos e insertar su ruta | `Ctrl-t` |
| Buscar carpeta y entrar | `Option izquierdo+c` |
| Revisar Git | `lg` |
| Buscar texto | `rg "texto"` |
| Encontrar archivos | `fd "nombre"` |
| Formatear JSON | `jq . archivo.json` |
| Terminal rápida de Ghostty | `Cmd+p`, con Ghostty enfocado |

Se conserva Option derecho para caracteres del teclado español. No se fuerza
Shift+Enter: cada agente mantiene su manejo de entrada multilínea.

## tmux

Desde la carpeta del proyecto, ejecuta `tp`. El nombre incluye un identificador
de la ruta para no mezclar proyectos con nombres iguales. También puedes usar
`tp nombre` para compartir explícitamente una sesión. No se inicia automáticamente.

El prefijo es **Ctrl-a**, se suelta y luego se pulsa la siguiente tecla:

| Tecla después de Ctrl-a | Acción |
| --- | --- |
| `g` | Abrir Lazygit en popup; `q` lo cierra |
| `\|` / `-` | Dividir a los lados / arriba y abajo |
| Flechas o `h j k l` | Cambiar de panel |
| `H J K L` | Ajustar tamaño |
| `z` | Ampliar/restaurar panel |
| `c` | Nueva ventana en la carpeta actual |
| `1`…`9` | Cambiar de ventana |
| `,` | Renombrar ventana |
| `d` | Desconectarse y dejar la sesión abierta |
| `[` | Modo de copia: `v` selecciona, `y` copia al portapapeles de macOS |
| `r` | Recargar configuración |
| `?` | Ver atajos |
| `Ctrl-a` | Enviar Ctrl-a al programa |

`tl` lista sesiones; `ta nombre` vuelve a una. tmux mantiene sus procesos
al desconectarse; la máquina debe seguir encendida y despierta. No sobrevive
a un reinicio ni administra agentes que están en otras aplicaciones.
Las sesiones remotas requieren tmux instalado y ejecutado en el servidor.
Esta configuración usa zsh y `pbcopy` de macOS; no aplicarla tal cual en Linux.

## Git personal y laboral

El instalador agrega una inclusión común para delta y otra para la identidad
personal bajo `~/Documents/personal-github/`. Conserva inclusiones existentes,
incluidas las que seleccionan cuentas SSH y proyectos en discos externos.
También fija la identidad personal en la configuración local de este repositorio.

En esta Mac se mantienen tus reglas laborales anteriores. En una Mac nueva
se configuran aparte: este repositorio no publica las identidades de trabajo.
`user.useConfigOnly=true` evita que Git invente una identidad cuando ninguna
está configurada; no reemplaza una identidad global explícita ya existente.

Comprueba cada proyecto con:

```sh
git config --show-origin --get user.email
git remote -v
```

## Actualizar configuraciones

```sh
cd "$HOME/Documents/personal-github/dotfiles"
git pull --ff-only
./install.sh --skip-packages
```

Para cambios propios, edita los archivos en `home/` y ejecuta `chezmoi diff`
y `chezmoi apply`. Luego revisa y guarda con `lg`. No hay sincronización
automática ni se sube nada a GitHub sin hacer un push.

## Respaldos y verificación

Cada ejecución del instalador respalda los archivos existentes en
`~/.local/state/dotfiles/backups/FECHA-ID/`, fuera del repositorio. Su
`manifest.json` indica qué archivos existían y cuáles son administrados.
Para revertir una integración, restaura `.zshrc` y `.gitconfig` de ese respaldo;
para restaurar un ajuste de una aplicación, copia su archivo correspondiente.
Si antes no existía un archivo, el manifiesto permite identificarlo y retirarlo.
Los paquetes instalados se conservan al restaurar configuraciones.

```sh
python3 -m unittest discover -s tests -v
bash -n install.sh
zsh -n home/dot_config/zsh/dotfiles.zsh
brew bundle check --no-upgrade
chezmoi diff
```

No se versionan historiales, `.env`, credenciales, claves SSH, sesiones ni
configuraciones completas de agentes. El alcance actual es macOS; el soporte
para una futura PC/Linux se añadirá cuando se conozca el sistema.

## Referencias

- [PR #3 de Milton](https://github.com/miltonparedes/dotfiles/pull/3): integración
  simplificada de Lazygit/delta y separación de configuraciones por plataforma.
- [Ghostty](https://ghostty.org/docs/config/reference)
- [chezmoi](https://www.chezmoi.io/)
- [Starship](https://starship.rs/config/)
- [tmux](https://github.com/tmux/tmux/wiki)

La configuración es propia y adaptada a zsh/macOS. No incorpora sus gateways,
secretos, ajustes de hardware ni atajos que desactivan permisos de los agentes.
