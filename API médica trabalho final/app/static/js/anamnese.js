/**
 * Lógica do formulário de anamnese e envio para triagem.
 */

document.addEventListener("DOMContentLoaded", async () => {
    const formAnamnese = document.getElementById("formulario-anamnese");
    const sliderDor = document.getElementById("intensidade_dor");
    const valorDorDestaque = document.getElementById("valor-dor");
    const divMensagemErro = document.getElementById("mensagem-erro-anamnese");

    // Atualização dinâmica do valor da escala de dor
    if (sliderDor && valorDorDestaque) {
        sliderDor.addEventListener("input", (e) => {
            valorDorDestaque.textContent = e.target.value;
        });
    }

    if (formAnamnese) {
        formAnamnese.addEventListener("submit", async (evento) => {
            evento.preventDefault();
            divMensagemErro.classList.add("oculto");

            const botaoEnviar = document.getElementById("botao-submeter-anamnese");
            botaoEnviar.disabled = true;
            botaoEnviar.textContent = "Analisando sintomas e gerando triagem...";

            try {
                // Coleta de sintomas associados
                const checkboxesSintomas = document.querySelectorAll("input[name='sintomas_associados']:checked");
                const sintomasAssociados = Array.from(checkboxesSintomas).map(cb => cb.value);

                // Coleta de sinais de alerta
                const checkboxesAlertas = document.querySelectorAll("input[name='sinais_alerta']:checked");
                const sinaisAlerta = Array.from(checkboxesAlertas).map(cb => cb.value);

                // Coleta de comorbidades
                const checkboxesComorbidades = document.querySelectorAll("input[name='comorbidades']:checked");
                const comorbidades = Array.from(checkboxesComorbidades).map(cb => cb.value);

                const corpoRequisicao = {
                    nome_paciente: document.getElementById("nome_paciente").value.trim(),
                    idade: parseInt(document.getElementById("idade").value, 10),
                    sexo: document.getElementById("sexo").value,
                    sintoma_principal: document.getElementById("sintoma_principal").value,
                    sintomas_associados: sintomasAssociados,
                    tempo_evolucao: document.getElementById("tempo_evolucao").value,
                    intensidade_dor: parseInt(document.getElementById("intensidade_dor").value, 10),
                    sinais_alerta: sinaisAlerta,
                    comorbidades: comorbidades,
                    medicamentos: document.getElementById("medicamentos").value.trim(),
                    alergias: document.getElementById("alergias").value.trim()
                };

                const resultado = await enviarRequisicao("/api/anamnese/analisar", "POST", corpoRequisicao);

                // Armazenar temporariamente no sessionStorage para exibição na página de resultado
                sessionStorage.setItem("ultimo_resultado_triagem", JSON.stringify(resultado));

                // Redireciona para o painel de resultado
                window.location.href = `/resultado?id=${resultado.id}`;

            } catch (erro) {
                divMensagemErro.textContent = erro.message || "Erro ao processar anamnese. Tente novamente.";
                divMensagemErro.classList.remove("oculto");
                botaoEnviar.disabled = false;
                botaoEnviar.textContent = "Concluir e Ver Triagem";
            }
        });
    }
});
