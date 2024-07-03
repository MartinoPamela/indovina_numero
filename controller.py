from view import View
from model import Model
import flet as ft

# il controller è l'unico che conosce il modello

# il controller controlla quello che fa l'utente e chiede al modello, per ogni cosa che abbia bisogno di logica
# chiede al modello, questo per il pattern MVC


class Controller(object):
    def __init__(self, view: View):
        self._view = view
        self._model = Model()

    def handleNuova(self, e):
        # chiamata quando premo il tasto nuova partita, resetto quindi l'interfaccia grafica e il model
        self._view._txtMrim.value = self.getMmax()
        self._view._btnProva.disabled = False  # così quando parto il tasto è disabilitato,
        # se faccio nuova partita mi sblocca prova
        self._view._txtTentativo.disabled = False  # lo abilito
        self._view._lvOut.controls.clear()  # pulisco la casella di testo in output
        self._view._lvOut.controls.append(ft.Text("Indovina il numero.", color="green"))
        self._model.inizializza()
        self._view._pb.value = self._model._Mrim / self._model._Mmax
        self._view.update()

    def handleProva(self, e):
        # questo metodo legge il valore nel TextField, prova a vedere se quel tentativo è un numero,
        # poi chiede al modello prova questo numero
        tentativo = self._view._txtTentativo.value
        self._view._txtTentativo.value = ""  # ogni volta che provo svuoto il tentativo,
        # mi prendo la stringa e poi la assegno a 0

        try:
            intTentativo = int(tentativo)
        except ValueError:
            self._view._lvOut.controls.append(ft.Text("Il tentativo deve essere un intero."))
            self._view.update()
            return

        mRim, result = self._model.indovina(intTentativo)
        self._view._txtMrim.value = mRim
        self._view._pb.value = self._model._Mrim / self._model._Mmax
        self._view.update()


        if mRim == 0:
            self._view._btnProva.disabled = True  # disabilito i tasti
            self._view._txtTentativo.disabled = True  # disabilito i tasti
            self._view._lvOut.controls.append(ft.Text("Hai perso! :-( Il segreto era: "
                                                      + str(self._model.segreto)))  # non posso legare una stringa con un intero, quindi faccio + str()
            self._view.update()  # ogni volta che modifico qualcosa dell'interfaccia grafica devo aggiornarla
            return

        # se supero questo controllo qui vado a controllare il risultato

        if result == 0:
            self._view._lvOut.controls.append(ft.Text("Hai vinto! :-)"))
            self._view._btnProva.disabled = True  # se ho vinto disabilito il tasto per continuare a giocare
            # perché non mi serve più
            self._view.update()
            return
        elif result == -1:
            self._view._lvOut.controls.append(ft.Text("Nope, il segreto è più piccolo."))
            self._view.update()
            return
        else:
            self._view._lvOut.controls.append(ft.Text("Nope, il segreto è più grande."))
            self._view.update()
            return

    def getNmax(self):  # questo metodo semplicemente chiede al modello qual è il tuo nmax e lo ritorna
        return self._model.NMax

    def getMmax(self):
        return self._model.MMax

    def getMrim(self):
        return self._model.Mrim
