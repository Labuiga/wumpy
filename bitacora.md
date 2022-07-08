BITACORA FOR PHILOSOPHY

Log acciones realizadas:

- Instalar Ubuntu

- Instalar Java

        sudo apt install default-jr
	
- Instalar JetBrains ToolBox

        sudo tar -xzf jetbrains-toolbox-1.18.7455.tar.gz  -C /opt
        ./jetbrains-toolbox
	
- Instalar PyCharm desde ToolBox para que gestione Updates

- Instalar virtualenv para entorno virtualizado al margen del SO:

        sudo apt install virtualenv
        virtualenv -p python3 --system_site_packages p3
	
- Crear el proyecto en Pycharm y añadir el entorno virtual que acabo de instalar como interprete.

- Editar/ Crear wumpus.py y empezar a estructurar el código para programar.

- Establecer Run/Debug configurations en PyCharm para parámetros de lanzamiento

        PyCharm > Run > Edit Configurations > Parameters
    
- Instalar pytest
    
        pip install pytest
        ó
        File > Settings > Python Interpreter > + (install) > pytest
    
- Crear test_wumpus.py

- Ejecutar test con Terminal:
    
        david@pc:~/PycharmProjects/wumpus$ pytest -v
    
- Preparar para que pueda ser ejecutado: añadir permisos de ejecución a launch.py:

        chmod +x launch.py

- Refactorizar el script 

        wumpus_v2.py        

- Agregar un venv local al proyecto

        instal.sh & launch.sh
  
- Avanzar el proyecto por mi cuenta

        ahora se llama wumpy y es un proyecto público

- TO DO:
        
        - código en launch q debería estar en wumpus_v2.py
        - -c 1 < -c: cheats debería ser un argumento sin parámetro
        - print correcto & easily viewable de los cheats y tablero
        - test profesionales y serios, posible fallo al atacar al wumpus
        - crear mi propio stack en otro proyecto
        - interfaz grafica wumpy si se tercia
        - compatibilidad windows si me aptc