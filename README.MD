- Notas
    - Para optimizar la web en una vista de celular hay que usar middleware para fijar templates segun dispositivo
    - Hay que encriptar el token de compra en la db (importancia baja)
    - crear PLQSL para la eliminación de los carritos de sesiones anonimas


- Features
    - La app 'store' usa un context_processors para mostrar el total($) del carrito guardado en cada sesión
    A esto se le agrega también el contador de items en el carrito


- Comando para ejecutar Scripts en Windows (powershell)
    - Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

- Tarjeta de prueba transbank:
    - 4051885600446623 
    - fecha: cualquiera mayor a la actual
    - cvv: 123