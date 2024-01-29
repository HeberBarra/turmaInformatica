from typing import List


class Student:

    def __init__(self, nome: str, status: str, grupo: str, dependencias: List[str]):
        self._nome = nome
        self._status = status
        self._grupo = grupo
        self._dependencias = dependencias

    def get_student_data(self) -> dict:
        return {
            "nome": self.nome,
            "status": self.status,
            "grupo": self.grupo,
            "total de dependências": len(self.dependencias),
            "dependências": self.dependencias
        }

    def __lt__(self, other):
        return self.nome < other.nome

    def __eq__(self, other):
        return self == other

    def __repr__(self):
        return (
            f'\nNome: {self.nome}\n'
            f'Status: {self.status}\n'
            f'Grupo: {self.grupo}\n'
            f'Total de dependências: {len(self.dependencias)}\n'
            f'Dependências: {self.dependencias}'
        )

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str):
        self._nome = novo_nome

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str):
        self._status = new_status

    @property
    def grupo(self) -> str:
        return self._grupo

    @grupo.setter
    def grupo(self, novo_grupo):
        self._grupo = novo_grupo

    @property
    def dependencias(self) -> List[str]:
        return self._dependencias

    @dependencias.setter
    def dependencias(self, novas_dependencias: int):
        self._dependencias = novas_dependencias
