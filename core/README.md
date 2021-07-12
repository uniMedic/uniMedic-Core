<p align="center">
  <img align="center" src="https://github.com/medtorch/Q-Aid/blob/master/misc/q_aid_logo_small1.png" alt="Q&Aid" width="75%">
</p>


# uniMedic Core

## Introducción

Este módulo será el encargado de realizar las inferencias de las consultas médicas. Se usa `FastAPI` para que en un futuro el proyecto sea escalable y tolerable a fallas.

Descargue los pesos del modelo VQA en este [link](https://drive.google.com/file/d/1dqJjthrbdnIs41ZdC_ZGVQnoZbuGMNCR/view?usp=sharing)
y guardelos en `models/model_vqa/MICCAI19-MedVQA/saved_models/BAN_MEVF/model_epoch19.pth`

## Ejecutar el servidor

```
uvicorn main:app --host 0.0.0.0 --port 8000
```

GET http://127.0.0.1:8000/capabilities retornará una lista de los modelos disponibles.

## Pruebas

Ejecuta los scripts en la carpeta `tests` para verificar cada modelo.
Se requiere que el servidor esté en ejecución.

