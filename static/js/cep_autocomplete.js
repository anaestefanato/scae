document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.querySelector('input[name="cep"]');
    const cidadeInput = document.querySelector('input[name="cidade"]');
    const bairroInput = document.querySelector('input[name="bairro"]');
    const ruaInput = document.querySelector('input[name="rua"]');

    if (cepInput) {
        cepInput.addEventListener('blur', function() {
            let cep = cepInput.value.replace(/\D/g, '');
            if (cep.length === 8) {
                fetch(`https://viacep.com.br/ws/${cep}/json/`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.erro) {
                            if (cidadeInput) cidadeInput.value = data.localidade;
                            if (bairroInput) bairroInput.value = data.bairro;
                            if (ruaInput) ruaInput.value = data.logradouro;
                        }
                    });
            }
        });
    }
});
// xhfdhtxd