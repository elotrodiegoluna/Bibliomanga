- Notas
    - Para optimizar la web en una vista de celular hay que usar middleware para fijar templates segun dispositivo




- Features
    - La app 'store' usa un context_processors para mostrar el total($) del carrito guardado en cada sesión
    A esto se le agrega también el contador de items en el carrito




- Advertencias
    - En producción hay que crear un middleware o programar en la base de datos la eliminación de los carritos de sesiones anonimas



- Comando para ejecutar Scripts en Windows (powershell)
    - Set-ExecutionPolicy RemoteSigned -Scope CurrentUser