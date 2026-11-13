/**
 * Lógica da página de histórico de anamneses do usuário.
 */

document.addEventListener("DOMContentLoaded", async () => {
    const containerHistorico = document.getElementById("tabela-historico-corpo");
    const containerVazio = document.getElementById("historico-vazio");
    const containerCarregando = document.getElementById("historico-carregando");
    const modalDetalhe = document.getElementById("modal-detalhes-anamnese");

    if (!containerHistorico) return;

    try {
        const registros = await enviarRequisicao("/api/anamnese/historico", "GET");
        containerCarregando.classList.add("oculto");

        if (!registros || registros.length === 0) {
            containerVazio.classList.remove("oculto");
            return;
        }

        containerHistorico.innerHTML = "";
        registros.forEach((item) => {
            const linha = document.createElement("tr");

            const dataFormatada = new Date(item.criado_em).toLocaleDateString("pt-BR", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            });

            linha.innerHTML = `
                <td><strong>${dataFormatada}</strong></td>
                <td>${item.nome_paciente} (${item.idade} anos)</td>
                <td>${item.sintoma_principal}</td>
                <td>
                    <span class="badge-risco ${item.cor_risco}">
                        ${item.nivel_risco}
                    </span>
                    ${item.indicacao_urgencia ? '<span style="color:#DC2626; font-size:0.8rem; margin-left:5px;">⚠️ Urgente</span>' : ''}
                </td>
                <td>
                    <a href="/resultado?id=${item.id}" class="botao botao-secundario" style="padding: 0.35rem 0.9rem; font-size: 0.85rem;">
                        Ver Orientações
                    </a>
                </td>
            `;
            containerHistorico.appendChild(linha);
        });

    } catch (erro) {
        containerCarregando.textContent = "Erro ao carregar histórico: " + erro.message;
    }
});
