from Controle.ControladorMembroAcademia import ControladorMembroAcademia
from Controle.ControladorPessoas import ControladorPessoas
from Controle.ControladorFilmes import ControladorFilmes
from Controle.ControladorCategoria import ControladorCategoria
from Controle.ControladorParticipante import ControladorParticipante
from Controle.ControladorIndicacao import ControladorIndicacao
from Controle.ControladorVoto import ControladorVoto
from Limite.TelaSistema import TelaSistema

class ControladorSistema:
    def __init__(self):
        self.__telaSistema = TelaSistema(self)
        self.__controladorMembroAcademia = ControladorMembroAcademia(self)
        self.__controladorPessoas = ControladorPessoas(self)
        self.__controladorFilmes = ControladorFilmes(self)
        self.__controladorCategorias = ControladorCategoria(self)
        self.__controladorParticipante = ControladorParticipante(self)
        self.__controladorIndicacao = ControladorIndicacao(self)
        self.__controladorVoto = ControladorVoto(self)

    @property
    def telaSistema(self):
        return self.__telaSistema

    @property
    def controladorMembroAcademia(self):
        return self.__controladorMembroAcademia

    @property
    def controladorPessoas(self):
        return self.__controladorPessoas

    @property
    def controladorFilmes(self):
        return self.__controladorFilmes

    @property
    def controladorCategorias(self):
        return self.__controladorCategorias

    @property
    def controladorParticipante(self):
        return self.__controladorParticipante

    @property
    def controladorIndicacao(self):
        return self.__controladorIndicacao

    @property
    def controladorVoto(self):
        return self.__controladorVoto

    def inicia(self):
        self.telaInicial()

    def telaInicial(self):
        listaOpcoes = {
            1: self.controladorMembroAcademia.exibirMenu,
            2: self.controladorPessoas.exibirMenu,
            3: self.controladorFilmes.exibirMenu,
            4: self.controladorCategorias.exibirMenu,
            5: self.controladorParticipante.exibirMenu,
            6: self.controladorIndicacao.exibirMenu,
            7: self.controladorVoto.exibirMenu
        }

        while True:
            opcao = self.telaSistema.exibirMenuPrincipal()
            if opcao == 0:
                break
            funcao = listaOpcoes.get(opcao)
            if funcao:
                funcao()
            else:
                self.telaSistema.mostraMensagem("Opção não encontrada. Tente novamente!")

    def adicionarPessoa(self, novaPessoa):
        self.controladorPessoas.pessoas.append(novaPessoa)

    def adicionarIndicacao(self, indicacao):
        if not hasattr(self, "_indicacoes"):
            self._indicacoes = []
        self._indicacoes.append(indicacao)

    def buscar_membro_por_id(self, id):
        for membro in self.controladorMembroAcademia.membrosAcademia:
            if membro.id == id:
                return membro
        return None
