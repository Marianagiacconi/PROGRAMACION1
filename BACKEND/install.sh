#Prepara el entorno
command -v python3 >/dev/null 2>&1 || { echo >&2 "python3 is not installed.  Aborting."; exit 1; } #Verificar si existe el comando
dpkg-query -l python3-venv > /dev/null 2>&1 || { echo >&2 "python3-venv is not installed. Aborting.";exit 1;} #Verificar si el paquete está instalado

python3 -m venv . #Crea el entorno virtual
source bin/activate #Activa el entorno virtual

#Comprobacion variables de entorno
file=.env
path=$(pwd)
if [ ! -f $file ]; then
    echo "Generando .env..."
    lineA=$(echo "export PORT = 5000" >> .env )
    lineB= $(echo "export DATABASE_NAME = 'database.db'" >> .env)
    lineC=$(echo "export DATABASE_PATH = '$path/'" >> ./.env)  

    $lineA
    $lineB
    $lineC 
fi

pip install --upgrade pip #Verifica si pip está actualizado
pip install -r requirements.txt #Instala paquetes