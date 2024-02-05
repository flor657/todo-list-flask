
    function confirmarEliminacion(url) {
        // Configurar el botón de confirmación dentro del modal
        $('#confirmarEliminarBtn').off('click').on('click', function() {
            // Redirigir a la URL de eliminación si el usuario confirma
            window.location.href = url;
        });
    }

    function eventFired(type) {
        let n = document.querySelector('#demo_info');
        n.innerHTML += '<div>' + type + ' event - ' + new Date().getTime() + '</div>';
        n.scrollTop = n.scrollHeight;
    }
    
    $(document).ready(function () {
        $('#example').DataTable()
            
    });
    

