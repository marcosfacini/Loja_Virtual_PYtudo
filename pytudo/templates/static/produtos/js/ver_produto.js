function changeImage(element) {

    var main_prodcut_image = document.getElementById('main_product_image');
    main_prodcut_image.src = element.src;
    
}

  
document.addEventListener('DOMContentLoaded', function() {
    // Obtenha os botões pelo ID
    var comprarButton = document.getElementById('comprarButton');
    var listaDesejoButton = document.getElementById('listaDesejoButton');

    // Adicione um ouvinte de evento de clique aos botões
    comprarButton.addEventListener('click', function() {
        var href = comprarButton.getAttribute('data-href');
        if (href) {
            window.location.href = href; // Redirecione para o URL do botão 'Comprar'
        }
    });

    listaDesejoButton.addEventListener('click', function() {
        var href = listaDesejoButton.getAttribute('data-href');
        if (href) {
            window.location.href = href; // Redirecione para o URL do botão 'Lista de Desejo'
        }
    });
});


$(document).ready(function(){
    $('#cep').mask('00000-000');

  });
