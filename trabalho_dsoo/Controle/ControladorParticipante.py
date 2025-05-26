from Entidades.Participante import Participante
from Entidades.Pessoa import Pessoa
from Entidades.Filme import Filme
from Entidades.Funcao import Funcao
from Limite.TelaPessoas import TelaPessoas

class ControladorParticipante:
    def __init__(self, controladorSistema):
        self.__participantes = []
        self.__controladorSistema = controladorSistema
        self.__telaParticipante = TelaPessoas(self)  # Reaproveitando tela de pessoas

    @property
    def participantes(self):
        return self.__participantes

    @property
    def controladorSistema(self):
        return self.__controladorSistema

    @property
    def telaParticipante(self):
        return self.__telaParticipante

    def exibirMenu(self):
        listaFuncoes = {
            1: self.addParticipante,
            2: self.delParticipante,
            3: self.listarParticipantes,
            4: self.detalharParticipante
        }
        while True:
            opcao = self.telaParticipante.exibirMenu()
            if opcao == 0:
                break
            funcao = listaFuncoes.get(opcao)
            if funcao:
                funcao()
            else:
                self.telaParticipante.mostraMensagem("Opção inválida!")

    def addParticipante(self):
        info = self.telaParticipante.addPessoaInfo()
        nome_filme = self.telaParticipante.getString("Nome do Filme: ")
        ano_filme = self.telaParticipante.getInt("Ano do Filme: ")
        genero_filme = self.telaParticipante.getString("Gênero do Filme: ")
        sinopse_filme = self.telaParticipante.getString("Sinopse do Filme: ")
        nome_funcao = self.telaParticipante.getString("Função (ex: Ator, Diretor): ")
        descricao_funcao = self.telaParticipante.getString("Descrição da Função: ")

        pessoa = Pessoa(info["nome"], info["sexo"], info["nacionalidade"], info["nascimento"])
        filme = Filme(nome_filme, ano_filme, genero_filme, sinopse_filme)
        funcao = Funcao(nome_funcao, descricao_funcao)
        novoParticipante = Participante(pessoa, filme, funcao)

        if not self.verificarSeHaParticipanteDuplicado(novoParticipante):
            self.participantes.append(novoParticipante)
            self.telaParticipante.mostraMensagem(f"\n✅ Participante '{pessoa.nome}' cadastrado!")
        else:
            self.telaParticipante.mostraMensagem(f"\n Participante '{pessoa.nome}' já cadastrado!")

    def verificarSeHaParticipanteDuplicado(self, copia: Participante):
        for participante in self.participantes:
            if participante.pessoa.nome == copia.pessoa.nome and participante.filme.titulo == copia.filme.titulo:
                return True
        return False

    def delParticipante(self):
        self.telaParticipante.mostraMensagem("\n--- Remover Participante ---")
        participanteRemovido = self.buscarParticipante()
        self.participantes.remove(participanteRemovido)
        self.telaParticipante.mostraMensagem(f"\n✅ Participante '{participanteRemovido.pessoa.nome}' foi removido com sucesso!")

    def buscarParticipante(self):
        while True:
            nome = self.telaParticipante.getString("Nome do Participante: ")
            for participante in self.participantes:
                if participante.pessoa.nome == nome:
                    return participante
            self.telaParticipante.mostraMensagem("Participante não encontrado! Tente novamente.")

    def listarParticipantes(self):
        self.telaParticipante.mostraMensagem("\n--- Lista de Participantes ---")
        for participante in self.participantes:
            self.telaParticipante.mostraMensagem(f"{participante.pessoa.nome} ({participante.funcao.nome} em '{participante.filme.titulo}')")
        input()

    def detalharParticipante(self):
        self.telaParticipante.mostraMensagem("\n--- Detalhar Participante ---")
        participante = self.buscarParticipante()
        self.telaParticipante.mostraMensagem(f"Nome: {participante.pessoa.nome}")
        self.telaParticipante.mostraMensagem(f"Filme: {participante.filme.titulo}")
        self.telaParticipante.mostraMensagem(f"Função: {participante.funcao.nome}")
        input()
