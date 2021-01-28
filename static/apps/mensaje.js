 $(document).ready(function () {
   $('input[name="numero_veces"]').TouchSpin({
        min: 1,
        max: 10000,
        step: 1
    });

       $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'add');
        save_with_ajax2('Alerta',
                '/send/nuevo', 'Esta seguro que desea enviar este mensaje?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al subir este archivo!', 'far fa-smile-wink', function () {
                    });
                });
    });
 });

