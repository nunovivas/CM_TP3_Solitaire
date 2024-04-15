
import flet as ft
from layout import create_appbar
from settings import Settings
from solitaire import Solitaire

# imports for save games
import logging
import json
import pickle

# logging.basicConfig(level=logging.DEBUG)
LOCAL_STORAGE_KEY = "saved_game"


def save_game_to_local_storage(page, solitaire):

    serialized_game = pickle.dumps(solitaire)
    page.client_storage.clear()  # clears and then rebuilds it
    page.client_storage.set(f"CALCULATORAPP.", serialized_game)


def load_game_from_local_storage(page):
    serialized_game = page.client_storage.get("CALCULATORAPP.")
    # serialized_game = ft.get_storage_item(LOCAL_STORAGE_KEY)
    if serialized_game:
        return pickle.loads(serialized_game)
        # return json.loads(serialized_game)
    return None


def main(page: ft.Page):
    def on_new_game(settings):
        page.controls.pop()
        page.solitaire = Solitaire(settings, on_win)
        page.add(page.solitaire)
        page.update()

    def on_save_state():
        save_game_to_local_storage(page, page.solitaire)

    def on_remaining_moves():
        print(page.solitaire.deck_passes_remaining)
        dialog_md = ft.Markdown(f"You have **{page.solitaire.deck_passes_remaining}** moves left")
        remaining_moves_dialog = ft.AlertDialog(
            title=ft.Text("Remaining Moves"),
            content=dialog_md,
            on_dismiss=lambda e: print("Remaining moves dialog dismissed!"),
        )
        page.dialog = remaining_moves_dialog
        remaining_moves_dialog.open = True
        page.update()
    def on_win():
        page.add(
            ft.AlertDialog(
                title=ft.Text("YOU WIN!"),
                open=True,
                on_dismiss=lambda e: page.controls.pop(),
            )
        )
        print("You win")
        page.update()

    settings = Settings()
    # aqui este appBar se calhar precisa de ter uma propriedade com o valor das jogadas que faltam
    # e estar dentro de um objecto que depois é passado?
    create_appbar(page, settings, on_new_game, on_save_state, on_remaining_moves)

    wtf = page.client_storage.get("CALCULATORAPP.")
    saved_solitaire = load_game_from_local_storage(page)
    if saved_solitaire:
        page.solitaire = saved_solitaire
    else:
        page.solitaire = Solitaire(settings, on_win)
    # solitaire = Solitaire(settings, on_win)
    page.add(page.solitaire)


# ft.app(target=main, assets_dir="assets")
ft.app(target=main, assets_dir="assets", port=8080, view=ft.WEB_BROWSER)
