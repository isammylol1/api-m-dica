/**
 * Funções globais e controle de autenticação do sistema.
 */

// Função auxiliar para requisições com JSON
async function enviarRequisicao(url, metodo = "GET", corpo = null) {
    const configuracao = {
        method: metodo,
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    };
    if (corpo) {
        configuracao.body = JSON.stringify(corpo);
    }

    const resposta = await fetch(url, configuracao);
    let dados = null;
    try {
        dados = await resposta.json();
    } catch (e) {
        dados = null;
    }

    if (!resposta.ok) {
        const mensagemErro = dados && dados.detail ? dados.detail : "Ocorreu um erro no servidor.";
        throw new Error(mensagemErro);
    }
    return dados;
}

// Logout do usuário
async function encerrarSessao() {
    try {
        await enviarRequisicao("/api/auth/logout", "POST");
        window.location.href = "/";
    } catch (erro) {
        alert("Erro ao encerrar sessão: " + erro.message);
    }
}

// Inicialização de botões de logout globais
document.addEventListener("DOMContentLoaded", () => {
    const botaoLogout = document.getElementById("botao-logout");
    if (botaoLogout) {
        botaoLogout.addEventListener("click", (e) => {
            e.preventDefault();
            encerrarSessao();
        });
    }
});
