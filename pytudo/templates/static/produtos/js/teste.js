document.getElementById('paymentMethod').addEventListener('change', function () {
    togglePaymentFields();
  });

  function togglePaymentFields() {
    const paymentMethod = document.getElementById('paymentMethod').value;
    document.getElementById('creditCardFields').classList.add('d-none');
    document.getElementById('boletoFields').classList.add('d-none');
    document.getElementById('pixFields').classList.add('d-none');

    if (paymentMethod === 'creditCard') {
      document.getElementById('creditCardFields').classList.remove('d-none');
    } else if (paymentMethod === 'boleto') {
      document.getElementById('boletoFields').classList.remove('d-none');
    } else if (paymentMethod === 'pix') {
      document.getElementById('pixFields').classList.remove('d-none');
    }
  };


  (function(win,doc){
    'use script';

    if(doc.querySelector('#formCard')){
        let formCard = doc.querySelector('#formCard');
        formCard.addEventListener('submit',(e)=>{
            e.preventDefault();
            let card = PagSeguro.encryptCard({
                publicKey: doc.querySelector('#publicKey').value,
                holder: doc.querySelector('#cardHolder').value,
                number: doc.querySelector('#cardNumber').value,
                expMonth: doc.querySelector('#cardMonth').value,
                expYear: doc.querySelector('#cardYear').value,
                securityCode: doc.querySelector('#cardCvv').value
            });
            let encrypted = card.encryptedCard;
            doc.querySelector('#encriptedCard').value = encrypted;
            formCard.submit();
        });
    }
})(window,document);
 