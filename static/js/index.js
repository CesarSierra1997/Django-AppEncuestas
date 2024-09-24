var $ = jQuery.noConflict();
function listarUsuarios() {
    $.ajax({
        url: "/usuario/listar_usuarios/",
        type: "get",
        datatype: "json",
        success: function (response) {
            if ($.fn.DataTable.isDataTable('#tabla_usuarios')) {
                $('#tabla_usuarios').DataTable().destroy();
            }
            $('#tabla_usuarios tbody').html("");
            for (let i=0; i<response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i+1) + '</td>';
                fila += '<td>' + response[i]["fields"]['username'] + '</td>';
                fila += '<td>' + response[i]["fields"]['nombres'] + '</td>';
                fila += '<td>' + response[i]["fields"]['apellidos'] + '</td>';
                fila += '<td>' + response[i]["fields"]['email'] + '</td>';
                fila += '<td>' + '<button class="btn btn-outline-info btn-sm tableButtom"';
                fila +=  'onclick ="abrir_modal_edicion(\'/usuario/editar_usuario/'+response[i]['pk']+'/\')" >Editar</button>'
                fila +=  '<button class="btn btn-outline-danger btn-sm"';
                fila +=  'onclick ="abrir_modal_eliminacion(\'/usuario/eliminar_usuario/'+response[i]['pk']+'/\')" >Eliminar</button>' + '</td>';
                fila += '</tr>';
                $('#tabla_usuarios').append(fila);
            }
            $('#tabla_usuarios').DataTable({
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
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function registrar(){
    activarBotonCreacion();
    $.ajax({
        data: $('#form_creacion').serialize(),
        url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        success: function (response){
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_creacion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresCreacion(error);
            activarBotonCreacion();
        }
    });
}

function editar(){
    activarBotonEdicion();
    $.ajax({
        data: $('#form_edicion').serialize(),
        url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response){
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_edicion();
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            mostrarErroresEdicion(error);
            activarBotonEdicion();
        }
    });
}

function eliminar(pk){
    $.ajax({
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
        },
        url: '/usuario/eliminar_usuario/'+pk+'/',
        type: 'post',
        success: function (response){
            notificacionSuccess(response.mensaje);
            listarUsuarios();
            cerrar_modal_eliminacion();
            console.log("menjsae del servidor",response);
        },
        error: function(error){
            notificacionError(error.responseJSON.mensaje);
            console.log(error);

        }
    });

}

$(document).ready(function () {
    listarUsuarios();
});