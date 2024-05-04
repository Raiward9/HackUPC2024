from taipy import Gui
import taipy.gui.builder as tgb
import taipy as tp

cities = ["Taipei", "New York", "London", "Tokyo", "Sydney"]
dates = ["2024-01-01", "2024-12-31"]

departure = ""
arrival = ""


init = True
start_again = False
def change_init(state):
    state.init = False
    state.start_again = True
    print(state.dates)

def default_values(state):
    state.init = True
    state.start_again = False

def on_action(state, name: str, value: any):
    if name == "dates":
        d1 = str(value[0])
        d2 = str(value[1])
        dates = [d1,d2]




with tgb.Page(on_refresh=change_init) as root_page:
    tgb.text(value="# Welcome Traveler", mode="md", color="primary", align="center")
    with tgb.layout("10 2*5"):
        with tgb.part(render = "{init}") as part:
            tgb.date_range("{dates}", with_time=False)
        with tgb.part(render = "{init}") as part: 
            tgb.selector(label="Departure", lov="{cities}", default="Taipei", dropdown=True)
        with tgb.part(render = "{init}") as part:
            tgb.selector(label="Arrival", lov="{cities}", default="Taipei",dropdown=True)
    
    with tgb.part(render = "{init}"):
        tgb.button("Meet People", color="primary", size="lg", block=True, on_action=change_init)
    with tgb.part(render = "{start_again}"):
        tgb.button("Start Again", color="secondary", size="lg", block=True, on_action=default_values)


pages = {
    "/" : root_page
}

if __name__ == '__main__':
    Gui(pages=pages).run(debug=True, use_reloader=True, )

