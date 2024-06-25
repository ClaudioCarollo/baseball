import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDYear(self):
        anni = self._model.getYear()
        for a in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(str(a)))
            self._view.update_page()

    def handleDDYearSelection(self, e):
        selected_year = self._view._ddAnno.value
        if selected_year is None:
            self._view._txtOutSquadre.controls.append(ft.Text("Inserisci un Anno!", color='red'))
            self._view.update_page()
        else:
            squadre = self._model.getTeam(selected_year)
            self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno: {selected_year}: {len(squadre)}"))
            for s in squadre:
                self._view._txtOutSquadre.controls.append(ft.Text(f"{s.code} ({s.name})"))
                self._view._ddSquadra.options.append(ft.dropdown.Option(str(s.code)))
                self._view.update_page()



    def handleCreaGrafo(self, e):
        selected_year = self._view._ddAnno.value
        if selected_year is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un anno!", color='red'))
            self._view.update_page()
        self._model.buildgraph(selected_year)
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {len(self._model._grafo.nodes)} nodi e {len(self._model._grafo.edges)}"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        selected_team = self._model._idMap[self._view._ddSquadra.value]
        self._view._txt_result.controls.append(ft.Text(f"Elenco squadre adiacenti a {selected_team.code}:"))
        self._view.update_page()
        pesi_vicini = self._model.getpesidecrescenti(selected_team)
        for k,v in pesi_vicini.items():
            self._view._txt_result.controls.append(ft.Text(f"{v.code}, peso : {k}"))
            self._view.update_page()

    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        selected_team = self._model._idMap[self._view._ddSquadra.value]
        if len(self._model._grafo.nodes) == 0:
            self._view._txt_result.controls.append(ft.Text("Creare un grafo!", color='red'))
            self._view.update_page()
            return
        if selected_team is None:
            self._view._txt_result.controls.append(ft.Text("Selezionare una squadra!", color='red'))
            self._view.update_page()
            return
        componenti = self._model.getPath(selected_team)
        peso = self._model._getScore(componenti)
        if componenti:
            self._view._txt_result.controls.append(ft.Text(f"Peso cammino migliore: {peso}"))
            self._view._txt_result.controls.append(ft.Text(f"Cammino:"))
            for c in componenti:
                self._view._txt_result.controls.append(ft.Text(f"{c}"))
            self._view.update_page()
            return
        else:
            self._view._txt_result.controls.append(ft.Text("Nessun percorso trovato!", color='red'))
            self._view.update_page()
            return