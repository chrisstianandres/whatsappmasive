var logotipo;
const toDataURL = url => fetch(url).then(response => response.blob())
    .then(blob => new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob)
    }));

toDataURL('/media/imagen.PNG').then(dataUrl => {
    logotipo = dataUrl;
});
$(function () {
    var action = '';
    var pk = '';
    var datatable = $("#datatable").DataTable({
        responsive: true,
        autoWidth: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {'action': 'list'},
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "nombres"},
            {"data": "telefono"},
            {"data": "id"}
        ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.15/i18n/Spanish.json',
        },
        dom:"<'row'<'col-sm-12 col-md-3'l>>" +
            "<'row'<'col-sm-12 col-md-12'f>>"+
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        columnDefs: [
            {
                targets: '_all',
                class: 'text-center',
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var edit = '<a style="color: white" type="button" class="btn btn-warning btn-sm" rel="edit" ' +
                        'data-toggle="tooltip" title="Editar Datos"><i class="fa fa-user-edit"></i></a>' + ' ';
                    var del = '<a type="button" class="btn btn-danger btn-sm"  style="color: white" rel="del" ' +
                        'data-toggle="tooltip" title="Eliminar"><i class="fa fa-trash"></i></a>' + ' ';
                    return edit + del

                }
            },
        ],

    });
    $('#datatable tbody')
        .on('click', 'a[rel="del"]', function () {
            action = 'delete';
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            var parametros = {'id': data.id};
            parametros['action'] = action;
            save_estado('Alerta',
                '/cliente/nuevo', 'Esta seguro que desea eliminar este cliente?', parametros,
                function () {
                    menssaje_ok('Exito!', 'Exito al eliminar este cliente!', 'far fa-smile-wink', function () {
                        datatable.ajax.reload(null, false)
                    })
                })})
        .on('click', 'a[rel="edit"]', function () {
            $('#exampleModalLabel').html('<i class="fas fa-edit"></i>&nbsp;Edicion de un registro');
            var tr = datatable.cell($(this).closest('td, li')).index();
            var data = datatable.row(tr.row).data();
            $('input[name="nombres"]').val(data.nombres);
            $('input[name="apellidos"]').val(data.apellidos);
            $('input[name="cedula"]').val(data.cedula).attr('readonly', true);
            $('input[name="correo"]').val(data.correo);
            $('input[name="sexo"]').val(data.sexo);
            $('input[name="telefono"]').val(data.telefono);
            $('input[name="direccion"]').val(data.direccion);
            $('#Modal').modal('show');
            action = 'edit';
            pk= data.id;
        });
    //boton agregar cliente
    $('#nuevo').on('click', function () {
        $('#exampleModalLabel').html('<i class="fas fa-plus"></i>&nbsp;Nuevo registro de un Cliente ');
        $('input[name="cedula"]').attr('readonly', false);
        $('#Modal').modal('show');
        action = 'add';
        pk= '';
    });

    $('#archivo').on('click', function () {
        $('#Modal_file').modal('show');
        action = 'add';
        pk= '';
    });

    //enviar formulario de nuevo cliente
    $('#form').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', action);
        parametros.append('id', pk);
        var isvalid = $(this).valid();
        if (isvalid) {
            save_with_ajax2('Alerta',
                '/cliente/nuevo', 'Esta seguro que desea guardar este cliente?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al guardar este cliente!', 'far fa-smile-wink', function () {
                        $('#Modal').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
        }
    });

    $('#form_file').on('submit', function (e) {
        e.preventDefault();
        var parametros = new FormData(this);
        parametros.append('action', 'file');
        save_with_ajax2('Alerta',
                '/cliente/nuevo', 'Esta seguro que desea subir este archivo?', parametros,
                function (response) {
                    menssaje_ok('Exito!', 'Exito al subir este archivo!', 'far fa-smile-wink', function () {
                        $('#Modal_file').modal('hide');
                        reset();
                        datatable.ajax.reload(null, false);
                    });
                });
    });
});
