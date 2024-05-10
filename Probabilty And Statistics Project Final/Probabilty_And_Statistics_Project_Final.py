import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextBrowser
from PyQt5.QtGui import QIcon

class YoungPopulationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.young_population = None
        self.reading_file = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Young Population Data Analysis ')
        self.setWindowIcon(QIcon('.\Resources\icons8-ai-48.ico'))
        self.setGeometry(100, 100, 600, 400)
        #self.setStyleSheet("background-color: lightgreen;")
        self.analysis_label = QLabel('Analysis Results:', self)
        self.analysis_text_browser = QTextBrowser(self)
        self.analysis_text_browser.setStyleSheet("background-color: white;")
        
        # StyleSheet
        button_style = """
        QPushButton {
        background-color: lightblue;
        border: 2px solid #3498db;
        border-radius: 2px;
        color: white;
        padding: 5px 10px;
        font-size: 16px;
        
        }
        QPushButton:hover {
        background-color: #2980b9;
        border-color: #2980b9;
        }
        """
        
        # Create widgets
        self.load_button = QPushButton('Load Data', self)
        self.reg_button = QPushButton('Regression Analysis', self)
        self.analysis_button = QPushButton('Analysis', self)
        self.load_button.clicked.connect(self.load_data)
        self.analysis_button.clicked.connect(self.analyze_data)
        self.input_label = QLabel('Enter Country Name:', self)
        self.country_dropdown = QComboBox(self)
        self.country_dropdown.addItems(['AUS', 'AUT', 'BEL', 'CAN', 'CZE', 'DNK', 'FIN', 'FRA', 'DEU', 'GRC',
                                        'HUN', 'ISL', 'IRL', 'ITA', 'JPN', 'KOR', 'LUX', 'MEX', 'NLD', 'NZL',
                                        'NOR', 'POL', 'PRT', 'SVK', 'ESP', 'SWE', 'CHE', 'TUR', 'GBR', 'USA',
                                        'BRA', 'CHL', 'COL', 'EST',
                                        'ISR', 'RUS', 'SVN', 'OECD', 'G-7', 'EU28', 'EA19', 'LVA', 'COOMAS'])

        self.show_button = QPushButton('Show Data', self)
        self.show_button.clicked.connect(self.show_data)
        self.pre_button = QPushButton('Data Prediction', self)
        self.pre_button.clicked.connect(self.prediction)

        self.plot_button = QPushButton('Plot Data', self)
        self.plot_button.clicked.connect(self.plot_data)
        self.reg_button.clicked.connect(self.regression_analysis)
        self.plot_type_label = QLabel('Select Plot Type:', self)
        self.plot_type_dropdown = QComboBox(self)
        self.plot_type_dropdown.addItems(['Simple Plot', 'Bar Chart', 'Histogram', 'Scatter Plot', 'Pie Chart'])
        self.text_browser = QTextBrowser(self)
        self.out_label = QLabel("Output box", self)
        self.all_buttons = [self.country_dropdown, self.show_button, self.plot_button, self.plot_type_dropdown, self.text_browser, self.reg_button, self.pre_button, self.analysis_button]
        self.set_buttons_enabled(False)

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.load_button)
        layout.addWidget(self.input_label)
        layout.addWidget(self.country_dropdown)
        layout.addWidget(self.plot_type_label)
        layout.addWidget(self.plot_type_dropdown)
        layout.addWidget(self.show_button)
        layout.addWidget(self.reg_button)
        layout.addWidget(self.pre_button)
        layout.addWidget(self.out_label)
        layout.addWidget(self.text_browser)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.analysis_button)  # Added button to layout
        layout.addWidget(self.analysis_label)
        layout.addWidget(self.analysis_text_browser)
        self.text_browser.setStyleSheet("background-color: white;")
        self.load_button.setStyleSheet(button_style)
        #self.show_button.setStyleSheet("background-color: white;")
        #self.reg_button.setStyleSheet("background-color: white;")
        #self.plot_button.setStyleSheet("background-color: white;")
        self.country_dropdown.setStyleSheet("background-color: white;")
        self.plot_type_dropdown.setStyleSheet("background-color: white;")
        #self.pre_button.setStyleSheet("background-color: white;")
        #self.analysis_button.setStyleSheet("background-color: white;")
        # Applying Style Sheet to Buttons
        for button in self.all_buttons:
            button.setStyleSheet(button_style)  
    def set_buttons_enabled(self, enabled):
        for button in self.all_buttons:
            button.setEnabled(enabled)

    def load_data(self):
        self.reading_file = pd.read_csv("young_population.csv")
        print("Loaded Successfully!!")
        self.set_buttons_enabled(True)

    def show_data(self):
        country_name = self.country_dropdown.currentText()
        location = self.reading_file.loc[self.reading_file['LOCATION'] == country_name]
        self.text_browser.clear()
        self.text_browser.insertPlainText(location.to_string(index=False))

    def plot_data(self):
        country_name = self.country_dropdown.currentText()
        plot_type = self.plot_type_dropdown.currentText()
        t = self.reading_file.loc[self.reading_file['LOCATION'] == country_name, "TIME"]
        v = self.reading_file.loc[self.reading_file['LOCATION'] == country_name, "Value"]

        plt.title(plot_type)
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')

        if plot_type == 'Simple Plot':
            plt.plot(t, v)
        elif plot_type == 'Bar Chart':
            plt.bar(t, v)
        elif plot_type == 'Histogram':
            plt.hist(v, bins=20)  # You may need to adjust the number of bins
        elif plot_type == 'Scatter Plot':
            plt.scatter(t, v)
        elif plot_type == 'Pie Chart':
            plt.pie(v, labels=t)
        else:
            print("Invalid plot type")

        plt.show()

    def regression_analysis(self):
        country_name = self.country_dropdown.currentText()
        time = self.reading_file.loc[self.reading_file['LOCATION'] == country_name, "TIME"]
        value = self.reading_file.loc[self.reading_file['LOCATION'] == country_name, "Value"]
        coefficients = np.polyfit(time, value, 1)
        intercept, slope = coefficients

        result_df = pd.DataFrame({
            'Location': [country_name],
            'Intercept': [intercept],
            'Slope': [slope]
        })
        self.text_browser.clear()
        self.text_browser.insertPlainText(result_df.to_string(index=False))

    def analyze_data(self):
        country_name = self.country_dropdown.currentText()
        data = self.reading_file.loc[self.reading_file['LOCATION'] == country_name]
        analysis_result = f"Analysis on {country_name} is as follows\n\n{data.describe()}"

        # Print to console for verification
        print(analysis_result)

        # Show the analysis result in the GUI
        self.analysis_text_browser.clear()
        self.analysis_text_browser.insertPlainText(analysis_result)

    def prediction(self):
        country_name = self.country_dropdown.currentText()
        data_subset = self.reading_file.loc[self.reading_file['LOCATION'] == country_name, ["TIME", "Value"]]

        # Sort the data by 'TIME' if it's not already sorted
        data_subset = data_subset.sort_values(by='TIME')

        X = data_subset["TIME"].values.reshape(-1, 1)
        y = data_subset["Value"].values

        # Create a linear regression model
        model = LinearRegression()

        # Fit the model to your data
        model.fit(X, y)

        # Predict the increase in population for the next 5 years
        self.text_browser.clear()
        future_years = np.array([2023, 2024, 2025, 2026, 2027]).reshape(-1, 1)
        predicted_population = model.predict(future_years)
        s = f"Your Given Country '{country_name}''s\n Prediction Based On data From Year 1958 to 2014 is \n This prediction is for year 2023 to 2027\n {predicted_population}"
        self.text_browser.insertPlainText(s)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = YoungPopulationApp()
    main_app.show()
    sys.exit(app.exec_())
