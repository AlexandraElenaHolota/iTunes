import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedAlbum = None
        self._grafo = None

    def handleCreaGrafo(self, e):
        if self._view._txtInDurata.value is None:
            self._view.txt_result.controls.append(ft.Text("Digita una durata in minuti"))
            return
        durata = int(self._view._txtInDurata.value)*60000
        self._grafo = self._model.buildGraph(durata)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(
            f"Il grafo è costituito di {n} nodi e {a} archi."))

        self.fillddAlbum()
        self._view.update_page()

    def fillddAlbum(self):
        album = self._model._idMap
        for a in album.values():
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(data=a,
                                   text=a.Title,
                                   on_click=self.getSelectedAlbum)
            )
        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._selectedAlbum = None
        else:
            self._selectedAlbum = e.control.data

    def handleAnalisiComp(self, e):
        if self._selectedAlbum is None:
            self._view.txt_result.controls.append(ft.Text("Album field not selected."))
            self._view.update_page()
            return
        sizeC, totDurata = self._model.componenteConnessa(self._selectedAlbum.AlbumId)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"La componente connessa che include {self._selectedAlbum.Title}"))
        self._view.txt_result.controls.append(ft.Text(
            f"ha dimensione {sizeC} e durata totale {totDurata}"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        pass