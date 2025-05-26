from Entidades.Voto import Voto
from Limite.TelaVoto import TelaVoto

class ControladorVoto:
    def __init__(self, controladorSistema):
        self.__votos = []
        self.__controladorSistema = controladorSistema
        self.__telaVoto = TelaVoto(self)

    @property
    def votos(self):
        return self.__votos

    @property
    def controladorSistema(self):
        return self.__controladorSistema

    @property
    def telaVoto(self):
        return self.__telaVoto

    def exibirMenu(self):
        listaFuncoes = {
            1: self.addVoto,
            2: self.delVoto,
            3: self.listarVotos,
            4: self.detalharVoto
        }
        while True:
            opcao = self.telaVoto.exibirMenu()
            if opcao == 0:
                break
            funcao = listaFuncoes.get(opcao)
            if funcao:
                funcao()
            else:
                self.telaVoto.mostraMensagem("Opção inválida!")

    def addVoto(self):
        self.telaVoto.mostraMensagem("\n--- Adicionar Voto ---")

        # Selecionar membro da academia que vai votar
        membros = self.controladorSistema.controladorMembroAcademia.membrosAcademia
        if not membros:
            self.telaVoto.mostraMensagem("Nenhum membro da academia cadastrado!")
            return
        for i, membro in enumerate(membros, 1):
            self.telaVoto.mostraMensagem(f"{i} - {membro.nome} (ID: {membro.id})")
        idx_membro = self.telaVoto.getInt("Escolha o membro que vai votar (número): ") - 1
        if idx_membro < 0 or idx_membro >= len(membros):
            self.telaVoto.mostraMensagem("Membro inválido.")
            return
        membro = membros[idx_membro]

        # Selecionar categoria para votar
        categorias = self.controladorSistema.controladorCategorias.categorias
        if not categorias:
            self.telaVoto.mostraMensagem("Nenhuma categoria cadastrada!")
            return
        for i, cat in enumerate(categorias, 1):
            self.telaVoto.mostraMensagem(f"{i} - {cat.nome}")
        idx_cat = self.telaVoto.getInt("Escolha a categoria para votar (número): ") - 1
        if idx_cat < 0 or idx_cat >= len(categorias):
            self.telaVoto.mostraMensagem("Categoria inválida.")
            return
        categoria = categorias[idx_cat]

        # Selecionar indicado (filme ou participante) conforme categoria
        if categoria.e_filme:
            filmes = self.controladorSistema.controladorFilmes.filmes
            if not filmes:
                self.telaVoto.mostraMensagem("Nenhum filme cadastrado!")
                return
            for i, filme in enumerate(filmes, 1):
                self.telaVoto.mostraMensagem(f"{i} - {filme.titulo} ({filme.ano})")
            idx_indicado = self.telaVoto.getInt("Escolha o filme votado (número): ") - 1
            if idx_indicado < 0 or idx_indicado >= len(filmes):
                self.telaVoto.mostraMensagem("Filme inválido.")
                return
            indicado = filmes[idx_indicado]
        else:
            participantes = self.controladorSistema.controladorParticipante.participantes
            if not participantes:
                self.telaVoto.mostraMensagem("Nenhum participante cadastrado!")
                return
            for i, part in enumerate(participantes, 1):
                self.telaVoto.mostraMensagem(f"{i} - {part.pessoa.nome} ({part.funcao.nome} em '{part.filme.titulo}')")
            idx_indicado = self.telaVoto.getInt("Escolha o participante votado (número): ") - 1
            if idx_indicado < 0 or idx_indicado >= len(participantes):
                self.telaVoto.mostraMensagem("Participante inválido.")
                return
            indicado = participantes[idx_indicado]

        # Verificar se o membro já votou nessa categoria para evitar voto duplicado
        for voto in self.votos:
            if voto.membro == membro and voto.categoria == categoria:
                self.telaVoto.mostraMensagem("Este membro já votou nesta categoria!")
                return

        # Criar e salvar o voto
        novo_voto = Voto(membro, categoria, indicado)
        self.votos.append(novo_voto)
        self.telaVoto.mostraMensagem("✅ Voto registrado com sucesso!")

    def delVoto(self):
        self.telaVoto.mostraMensagem("\n--- Remover Voto ---")
        if not self.votos:
            self.telaVoto.mostraMensagem("Nenhum voto registrado!")
            return
        for i, voto in enumerate(self.votos, 1):
            self.telaVoto.mostraMensagem(f"{i} - {self._descricao_voto(voto)}")
        idx = self.telaVoto.getInt("Escolha o voto para remover (número): ") - 1
        if idx < 0 or idx >= len(self.votos):
            self.telaVoto.mostraMensagem("Índice inválido.")
            return
        removido = self.votos.pop(idx)
        self.telaVoto.mostraMensagem(f"✅ Voto removido: {self._descricao_voto(removido)}")

    def listarVotos(self):
        self.telaVoto.mostraMensagem("\n--- Lista de Votos ---")
        if not self.votos:
            self.telaVoto.mostraMensagem("Nenhum voto registrado!")
            return
        for i, voto in enumerate(self.votos, 1):
            self.telaVoto.mostraMensagem(f"{i} - {self._descricao_voto(voto)}")
        input()

    def detalharVoto(self):
        self.telaVoto.mostraMensagem("\n--- Detalhar Voto ---")
        if not self.votos:
            self.telaVoto.mostraMensagem("Nenhum voto registrado!")
            return
        for i, voto in enumerate(self.votos, 1):
            self.telaVoto.mostraMensagem(f"{i} - {self._descricao_voto(voto)}")
        idx = self.telaVoto.getInt("Escolha o voto para detalhar (número): ") - 1
        if idx < 0 or idx >= len(self.votos):
            self.telaVoto.mostraMensagem("Índice inválido.")
            return
        voto = self.votos[idx]
        self.telaVoto.mostraMensagem("Detalhes do Voto:")
        self.telaVoto.mostraMensagem(f"Membro: {voto.membro.nome}")
        self.telaVoto.mostraMensagem(f"Categoria: {voto.categoria.nome}")
        if voto.categoria.e_filme:
            self.telaVoto.mostraMensagem(f"Filme votado: {voto.indicado.titulo} ({voto.indicado.ano})")
        else:
            self.telaVoto.mostraMensagem(f"Participante votado: {voto.indicado.pessoa.nome} ({voto.indicado.funcao.nome} em '{voto.indicado.filme.titulo}')")
        input()

    def _descricao_voto(self, voto):
        if voto.categoria.e_filme:
            return f"[{voto.categoria.nome}] Membro: {voto.membro.nome} | Filme: {voto.indicado.titulo} ({voto.indicado.ano})"
        else:
            return f"[{voto.categoria.nome}] Membro: {voto.membro.nome} | Participante: {voto.indicado.pessoa.nome} ({voto.indicado.funcao.nome} em '{voto.indicado.filme.titulo}')"
