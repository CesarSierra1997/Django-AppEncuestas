var $ = jQuery.noConflict();
function listarUsuarios() {
    $('#loading').show();
    $.ajax({
        url: "/usuario/listar_usuarios/",
        type: "get",
        datatype: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_usuarios')) {
                $('#tabla_usuarios').DataTable().destroy();
            }
            $('#tabla_usuarios tbody').html("");
            // Comprobamos si la respuesta tiene datos
            if (response.length === 0) {
                $('#agregar_usuario').hide();  // Ocultar botón si no hay usuarios
            } else {
                $('#agregar_usuario').show();  // Mostrar botón si hay usuarios
            }
            for (let i = 0; i < response.length; i++) {
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['username'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nombres'] + '</td>';
                fila += '<td>' + response[i]["fields"]['apellidos'] + '</td>';
                fila += '<td>' + response[i]["fields"]['email'] + '</td>';
                if (response[i]["fields"]['rol'] == 1) {
                    fila += '<td>Admin</td>';
                } else {
                    fila += '<td>Usuario</td>';
                }
                fila += '<td>' + '<button class="btn btn-outline-info btn-sm tableButtom"';
                fila += 'onclick ="abrir_modal_edicion(\'/usuario/editar_usuario/' + response[i]['pk'] + '/\')" ><i class="fa-solid fa-user-pen"></i></button>'
                fila += '<button class="btn btn-outline-danger btn-sm mx-1"';
                fila += 'onclick ="abrir_modal_eliminacion(\'/usuario/eliminar_usuario/' + response[i]['pk'] + '/\')" ><i class="fa-solid fa-trash-can mx-1"></i></button>' + '</td>';
                fila += '</tr>';
                $('#tabla_usuarios').append(fila);
            }
            $('#tabla_usuarios').DataTable({
                responsive: true,
                autoWidth: true,
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                    infoFiltered: "(Filtrado de _MAX_ total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                        first: "Primero",
                        last: "Ultimo",
                        next: "Siguiente",
                        previous: "Anterior",
                    },
                },
            });
            // Ocultar el GIF de carga y mostrar la tabla
            $('#loading').hide();
            $('#tabla_usuarios').show();
        },
        error: function (error) {
            console.log(error);
            // Ocultar el GIF de carga incluso en caso de error
            $('#loading').hide();
            $('#tabla_usuarios').show();
        }
    });
}

function registrar() {
    activarBotonCreacion();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_creacion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBotonCreacion();
        }
    });
}

function editar() {
    activarBotonEdicion();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_edicion();
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBotonEdicion();
        }
    });
}

function eliminar(pk) {
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/usuario/eliminar_usuario/' + pk + '/',
        type: 'post',
        success: function (response) {
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_eliminacion();
            console.log("menjsae del servidor", response);
        },
        error: function (error) {
            notificacionError(error.responseJSON.mensaje);
            console.log(error);

        }
    });

}

$(document).ready(function () {
    listarUsuarios();
});