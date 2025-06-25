import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self,e):
        if self._view._ddAnno.value == "" or self._view._ddAnno.value is None:
            self._view.create_alert(f"Selezionare un anno!!!")
            return

        self._model.buildGraph(self.season)
        self._model.getBeastDriver()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!!!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model._graph.number_of_nodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model._graph.number_of_edges()}"))
        self._view.txt_result.controls.append(ft.Text(f"Best driver: {self._model.best_driver}, with a score {self._model.best_result}"))
        self._view.update_page()

    def handleCerca(self, e):
        if self._view._txtIntK.value == "" or self._view._txtIntK.value is None:
            self._view.create_alert(f"Inserire un valore K!!!")
            return

        try:
            intK = int(self._view._txtIntK.value)
        except:
            self._view.create_alert("Inserire un valore numerico!!!")
            return

        self._model.getDreamTeam(intK)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Il dream team composto da {intK} piloti con tasso di sconfitta pari a {self._model.min_rate}:"))
        for driver in self._model.dream_team:
            self._view.txt_result.controls.append(ft.Text(driver))
        self._view.update_page()

    def fillDDYear(self):
        myValuesDD = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self.read_DD_value), self._model.getAllSeasons()))
        self._view._ddAnno.options = myValuesDD

    def read_DD_value(self,e):
        self.season = e.control.data