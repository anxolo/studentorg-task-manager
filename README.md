# StudentOrg Task Manager

**StudentOrg Task Manager** é un proxecto piloto dunha aplicación web para a xestión de tarefas, deseñada especificamente para as necesidades dunha Organización Estudantil ou Delegación de Alumnos. Permite organizar o traballo por comisións, asignar responsables e facer un seguimento do estado das actividades.

## 🎓 Contexto Académico

Este proxecto foi desenvolvido como parte da materia de **Redes** do 2º curso do **Grao en Intelixencia Artificial (GrIA)** na **Universidade de Vigo** (Cruso 2025/2026).

## ⚠️ Disclaimer e Melloras Pendentes

**Nota Importante:** Este software é un prototipo académico e **non está listo para un ambiente de produción real** sen realizar melloras previas, especialmente en materia de seguridade e xestión de usuarios.

Aínda que a aplicación conta con autenticación básica, **necesita implementar as seguintes melloras críticas:**

* **Verificación de Usuarios:** Actualmente, calquera persoa pode rexistrarse libremente. Para un uso real nunha delegación, é imprescindible implementar un sistema onde un **Administrador** verifique e aprobe as contas novas para asegurar que só os membros da organización teñen acceso.
* **Roles e Permisos:** Non existe distinción entre roles (ex: admin vs. usuario normal).


## ✨ Características Principais

* **Xestión de Usuarios:** Rexistro e inicio de sesión seguro (contrasinais hasheados).
* **Panel de Control (Dashboard):** Vista rápida de tarefas pendentes e completadas.
* **Xestión de Tarefas:**
* Crear, Editar e Eliminar tarefas.
* Asignar responsables e comisións/grupos de traballo.
* Establecer datas de entrega.
* Cambiar estados: Pendente, En Progreso, Feito.


* **Suxestións Intelixentes:** O sistema suxire responsables e comisións baseándose nas entradas máis frecuentes anteriores.

## 🛠️ Tecnoloxías Empregadas

* **Backend:** Python 3, Flask.
* **Base de Datos:** MySQL (con SQLAlchemy e PyMySQL).
* **Frontend:** HTML5, CSS3, Bootstrap 5.

## 🚀 Instalación e Despregamento

Para executar este proxecto en local:

1. **Clonar o repositorio:**
```bash
git clone https://github.com/anxolo/studentorg-task-manager.git
cd studentorg-task-manager

```


2. **Crear un entorno virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# ou
.\venv\Scripts\activate   # En Windows

```


3. **Instalar as dependencias:**
```bash
pip install -r requirements.txt

```


4. **Configuración da Base de Datos:**
O proxecto está configurado para buscar variables de entorno, pero ten valores por defecto para a base de datos de probas. Para configuralo correctamente, define as seguintes variables de entorno no teu sistema ou nun ficheiro `.env`:
* `DB_HOST`: Host da base de datos MySQL.
* `DB_USER`: Usuario da base de datos.
* `DB_PASS`: Contrasinal.
* `DB_NAME`: Nome da base de datos.
* `SECRET_KEY`: Clave para as sesións de Flask.


5. **Executar a aplicación:**
```bash
flask run

```


A aplicación estará dispoñible en `http://127.0.0.1:5000`.

## 📂 Estrutura do Proxecto

* `__init__.py`: Inicialización da app Flask e configuración da DB.
* `routes.py`: Lóxica do backend, rutas e control de base de datos.
* `templates/`: Arquivos HTML (Jinja2) para as vistas.
* `static/`: Arquivos CSS e recursos estáticos.
* `requirements.txt`: Lista de librerías necesarias.

---

**Autor:** Anxo López Rodríguez
