import numpy as np
import random
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import io
import base64

class TechnologyModel:
    def __init__(self, n, gamma, t_steps, dsm_density=0.2):
        self.n = n  # Number of components
        self.gamma = gamma  # Difficulty of reducing costs (exponent)
        self.t_steps = t_steps  # Number of innovation steps
        self.dsm_density = dsm_density  # Density of DSM (probability of interactions)
        
        # Initialize costs randomly between 0 and 1
        self.costs = np.random.rand(n)
        
        # Initialize Design Structure Matrix (DSM) with some density
        self.dsm = self.generate_dsm()
        
    def generate_dsm(self):
        """Generate a random Design Structure Matrix (DSM)"""
        dsm = np.random.rand(self.n, self.n) < self.dsm_density
        np.fill_diagonal(dsm, 0)  # No self-dependence
        return dsm

    def update_costs(self):
        """Perform one innovation attempt and update costs"""
        i = random.randint(0, self.n - 1)
        Ai = np.where(self.dsm[i, :] == 1)[0]
        new_costs = np.random.rand(len(Ai)) ** self.gamma  
        current_sum = np.sum(self.costs[Ai])
        new_sum = np.sum(new_costs)
        if new_sum < current_sum:
            self.costs[Ai] = new_costs
            return True
        return False 
    
    def run_simulation(self):
        """Run the simulation for t_steps"""
        cost_history = [np.sum(self.costs)]  # Track total cost
        for _ in range(self.t_steps):
            self.update_costs()
            cost_history.append(np.sum(self.costs))
        return cost_history

    def plot_results(self, cost_history):
        """Plot the evolution of total cost over time"""
        plt.figure(figsize=(10, 6))
        plt.plot(cost_history)
        plt.xlabel('Innovation Attempts')
        plt.ylabel('Total Cost of Technology')
        plt.title(f'Total Cost Evolution Over {self.t_steps} Innovation Attempts')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return img_base64

    def plot_dsm_heatmap(self):
        """Plot a heatmap of the Design Structure Matrix (DSM) using Matplotlib"""
        plt.figure(figsize=(8, 6))
        plt.imshow(self.dsm, cmap="Blues", interpolation='nearest')
        plt.colorbar(label='Dependency Strength')  # Add a color bar for reference
        plt.title("Design Structure Matrix (DSM) Heatmap")
        plt.xlabel('Component Index')
        plt.ylabel('Component Index')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        
        return img_base64

def create_window():
    layout = [
        [sg.Text('Technology Simulation')],
        [sg.Text('Number of components (n):'), sg.InputText('', size=(10, 1), key='n')],
        [sg.Text('Difficulty of Reducing Costs (gamma):'), sg.InputText('', size=(10, 1), key='gamma')],
        [sg.Text('Number of Innovation Steps (t_steps):'), sg.InputText('', size=(10, 1), key='t_steps')],
        [sg.Button('Run Simulation')],
        [sg.Text('Total Cost Evolution:')],
        [sg.Image(filename='', key='cost_evolution')],
        [sg.Text('DSM Heatmap:')],
        [sg.Image(filename='', key='dsm_heatmap')],
    ]
    return sg.Window('Technology Simulation', layout, finalize=True)

def main():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Run Simulation':
            # Get the input values from the user
            try:
                n = int(values['n'])
                gamma = float(values['gamma'])
                t_steps = int(values['t_steps'])

                # Create the model
                model = TechnologyModel(n, gamma, t_steps)

                # Run the simulation and get the results
                cost_history = model.run_simulation()
                cost_img_data = model.plot_results(cost_history)
                dsm_img_data = model.plot_dsm_heatmap()

                # Update the window with the images
                window['cost_evolution'].update(data=cost_img_data)
                window['dsm_heatmap'].update(data=dsm_img_data)

            except ValueError:
                sg.popup_error('Please enter valid numbers for all inputs.')

    window.close()

if __name__ == "__main__":
    main()
