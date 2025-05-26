from Entidades.MembroAcademia import MembroAcademia
from Limite.TelaMembroAcademia import TelaMembroAcademia
from Entidades.Indicacao import Indicacao
from datetime import date

class ControladorMembroAcademia:
    def __init__(self, controladorSistema):
        self.__membrosAcademia = []
        self.__controladorSistema = controladorSistema
        self.__telaMembroAcademia = TelaMembroAcademia(self)

    @property
    def membrosAcademia(self):
        return self.__membrosAcademia

    @property
    def controladorSistema(self):
        return self.__controladorSistema

    @property
    def telaMembroAcademia(self):
        return self.__telaMembroAcademia

    def exibirMenu(self):
        lista_opcoes = {
            1: self.addMembro,
            2: self.delMembro,
            3: self.listarMembros,
            4: self.indicar
        }
        while True:
            opcao = self.telaMembroAcademia.exibirMenuMembros()
            if opcao == 0:
                break
            funcao = lista_opcoes.get(opcao)
            if funcao:
                funcao()
            else:
                self.telaMembroAcademia.mostraMensagem("Opção inválida!")

    def addMembro(self):
        info = self.telaMembroAcademia.incluirMembroInfo()
        novoMembro = MembroAcademia(info["nome"], info["sexo"], info["nascimento"], info["nacionalidade"])
        if not self.verificarSeHaMembroDuplicado(novoMembro):
            self.membrosAcademia.append(novoMembro)
            self.controladorSistema.adicionarPessoa(novoMembro)
            self.telaMembroAcademia.mostraMensagem(f"\n✅ Membro '{novoMembro.nome}' cadastrado com ID {novoMembro.id}!")
        else:
            self.telaMembroAcademia.mostraMensagem(f"\nMembro '{novoMembro.nome}' já cadastrado!")

    def verificarSeHaMembroDuplicado(self, novoMembro):
        for membro in self.membrosAcademia:
            if membro.nome == novoMembro.nome:
                return True
        return False

    def delMembro(self):
        self.telaMembroAcademia.mostraMensagem("\n--- Remover Membro ---")
        membroRemover = self.buscarMembro()
        self.membrosAcademia.remove(membroRemover)
        self.telaMembroAcademia.mostraMensagem(f"\n✅ Membro '{membroRemover.nome}' removido com sucesso")

    def buscarMembro(self):
        while True:
            nomeMembro = self.telaMembroAcademia.getString("Nome do Membro: ")
            for membro in self.membrosAcademia:
                if membro.nome == nomeMembro:
                    return membro
            self.telaMembroAcademia.mostraMensagem("Membro não encontrado. Tente Novamente!")

    def listarMembros(self):
        self.telaMembroAcademia.mostraMensagem("\n--- Lista de Membros da Academia ---")
        for i, membro in enumerate(self.membrosAcademia, 1):
            self.telaMembroAcademia.mostraMensagem(f"{i} - {membro.nome} (ID: {membro.id})")
        input()

    def indicar(self):
        self.telaMembroAcademia.mostraMensagem("\n--- Indicar Filme ou Participante ---")
        membro = self.buscarMembro()
        # Selecionar categoria
        categorias = self.controladorSistema.controladorCategorias.categorias
        if not categorias:
            self.telaMembroAcademia.mostraMensagem("Nenhuma categoria cadastrada!")
            return
        for i, cat in enumerate(categorias, 1):
            self.telaMembroAcademia.mostraMensagem(f"{i} - {cat.nome}")
        idx_cat = self.telaMembroAcademia.getInt("Escolha a categoria (número): ") - 1
        if idx_cat < 0 or idx_cat >= len(categorias):
            self.telaMembroAcademia.mostraMensagem("Categoria inválida.")
            return
        categoria = categorias[idx_cat]

        # Selecionar indicado conforme tipo de categoria
        if categoria.e_filme:
            filmes = self.controladorSistema.controladorFilmes.filmes
            if not filmes:
                self.telaMembroAcademia.mostraMensagem("Nenhum filme cadastrado!")
                return
            for i, filme in enumerate(filmes, 1):
                self.telaMembroAcademia.mostraMensagem(f"{i} - {filme.titulo} ({filme.ano})")
            idx_filme = self.telaMembroAcademia.getInt("Escolha o filme indicado (número): ") - 1
            if idx_filme < 0 or idx_filme >= len(filmes):
                self.telaMembroAcademia.mostraMensagem("Filme inválido.")
                return
            indicado = filmes[idx_filme]
        else:
            participantes = self.controladorSistema.controladorParticipante.participantes
            if not participantes:
                self.telaMembroAcademia.mostraMensagem("Nenhum participante cadastrado!")
                return
            for i, part in enumerate(participantes, 1):
                self.telaMembroAcademia.mostraMensagem(f"{i} - {part.pessoa.nome} ({part.funcao.nome} em '{part.filme.titulo}')")
            idx_part = self.telaMembroAcademia.getInt("Escolha o participante indicado (número): ") - 1
            if idx_part < 0 or idx_part >= len(participantes):
                self.telaMembroAcademia.mostraMensagem("Participante inválido.")
                return
            indicado = participantes[idx_part]

        # Criar e registrar a indicação no controlador de indicações do sistema
        nova_indicacao = Indicacao(indicado, categoria, membro)
        self.controladorSistema.controladorIndicacao.indicacoes.append(nova_indicacao)
        self.telaMembroAcademia.mostraMensagem("\n✅ Indicação cadastrada com sucesso!")
