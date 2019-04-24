$(document).ready(function() {
  // Insere classe no primeiro item de produto
  $('#id_estoque-0-produto').addClass('clProduto');
  $('#id_estoque-0-quantidade').addClass('clQuantidade');

  $('#add-item').click(function(ev) {
    ev.preventDefault();
    var count = $('#estoque').children().length;
    var tmplMarkup = $('#item-estoque').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    $('div#estoque').append(compiledTmpl);

    // update form count
    $('#id_estoque-TOTAL_FORMS').attr('value', count + 1);

    // some animate to scroll to view our new form
    $('html, body').animate({
      scrollTop: $("#add-item").position().top - 200
    }, 800);

    $('#id_estoque-' + (count) + '-produto').addClass('clProduto');
    $('#id_estoque-' + (count) + '-quantidade').addClass('clQuantidade');
  });
});

let estoque
let saldo
let campo
let quantidade

$(document).on('change', '.clProduto', function() {
  let self = $(this)
  let pk = $(this).val()
  let url = '/produto/' + pk + '/json/'

  $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
      estoque = response.data[0].estoque
      campo = self.attr('id').replace('produto', 'quantidade')
      // Remove o valor do campo 'quantidade'
      $('#'+campo).val('')
    },
    error: function(xhr) {
      // body...
    }
  })
});

$(document).on('change', '.clQuantidade', function() {
  quantidade = $(this).val();
  saldo = Number(estoque) - Number(quantidade);
  campo = $(this).attr('id').replace('quantidade', 'saldo')
  // Atribui o saldo ao campo 'saldo'
  $('#'+campo).val(saldo)
});