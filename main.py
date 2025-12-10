if __name__ == "__main__":
    from PetModel import PetModel
    from PetView import PetView
    from PetController import PetController

    model = PetModel()
    # try to restore saved state if available
    try:
        loaded = model.load_from_file('save.json')
        if loaded:
            model.updateMood(model.energy, model.hunger)
    except Exception:
        pass
    view = PetView()
    # set default GIF display size (width, height)
    view.setGifSize(300, 300)
    controller = PetController(model, view)

    view.setController(controller)
    # initialize view from model so images/labels are set before mainloop
    controller.updateView()
    view.start()