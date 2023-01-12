from Repositorios.CandidatoRepositorio import CandidatoRepositorio
from Repositorios.PartidoRepositorio import PartidoRepositorio
from Modelos.Partido import Partido
from Modelos.Candidato import Candidato
class CandidatoControlador():
    def __init__(self):
        self.repositorioCandidatos = CandidatoRepositorio()
        self.repositorioPartido = PartidoRepositorio()
    
    def index(self):
        return self.repositorioCandidatos.findAll()
    
    def create(self, infoCandidato):
        nuevoCandidato = Candidato(infoCandidato)
        return self.repositorioCandidatos.save(nuevoCandidato)
    
    def show(self, id):
        elCandidato =Candidato(self.repositorioCandidatos.findById(id))
        return elCandidato.__dict__

    def update(self, id, infoCandidato):
        candidatoActual = Candidato(self.repositorioCandidatos.findById(id))
        candidatoActual.cedula = infoCandidato["cedula"]
        candidatoActual.numero_resolucion = infoCandidato["numero_resolucion"]
        candidatoActual.nombre = infoCandidato["nombre"]
        candidatoActual.apellido = infoCandidato["apellido"]
        return self.repositorioCandidatos.save(candidatoActual)
    def delete(self, id):
        return self.repositorioCandidatos.delete(id)

    def asignarCandidato(self, id, id_partido):
        candidatoActual = Candidato(self.repositorioCandidatos.findById(id))
        partidoActual = Partido(self.repositorioPartido.findById(id_partido))
        candidatoActual.partido = partidoActual
        return self.repositorioCandidatos.save(candidatoActual)