$(document).ready(function () {
    var option = $('input[name="option"]').val();
    if (option === 'editar') {
        $('#id_cedula').attr('readonly', 'true');
    }

    jQuery.validator.addMethod("lettersonly", function (value, element) {
        return this.optional(element) || /^[a-z," "]+$/i.test(value);
    }, "Letters and spaces only please");

    $.validator.setDefaults({
        errorClass: 'invalid-feedback',

        highlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-invalid")
                .removeClass("is-valid");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element)
                .addClass("is-valid")
                .removeClass("is-invalid");
        }
    });

    $("#form").validate({
        rules: {
            nombres: {
                required: true,
                minlength: 3,
                maxlength: 50,
                lettersonly: true,
            },

            telefono: {
                required: true,
                minlength: 13,
                maxlength: 13
            }
        },
        messages: {
            nombres: {
                required: "Porfavor ingresa tus nombres",
                minlength: "Debe ingresar al menos un nombre",
                lettersonly: "Debe ingresar unicamente letras y espacios"
            },
            telefono: {
                required: "Porfavor ingresa tu numero celular",
                minlength: "Tu numero de documento debe tener al menos 13 digitos",

                maxlength: "Tu numero de documento debe tener maximo 13 digitos",
            }
        },
    });

    $('#id_nombres').keyup(function () {
        var changue = $(this).val().replace(/\b\w/g, function (l) {
            return l.toUpperCase()
        });
        $(this).val(changue);
    });
    // $('#id_telefono').on('keypress',function (event) {
    //     validaNumericos(event);
    // });


});



