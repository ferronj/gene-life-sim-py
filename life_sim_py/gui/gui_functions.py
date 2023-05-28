from life_sim_py.simulation.run_simulation import run_simulation


# Scrapping GUI for now... pygame is funny... I don't know if I like it all that much...


class GUIFunctions:
    def __init__(self):
        self.generations = 0
        self.running = False

    def start_simulation(self, args):
        if not self.running:
            self.running = True
            print("Simulation started")
            run_simulation(args)

    def stop_simulation(self):
        if self.running:
            self.running = False
            print("Simulation stopped")

    def save_population(self):
        print("Population saved")

    def update_generations(self, value):
        try:
            self.generations = int(value)
        except ValueError:
            print("Invalid input for generations")

        print("Generations updated:", self.generations)
