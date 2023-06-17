import sys
import json
import yaml
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QMessageBox


class ConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Konwerter danych")
        self.setGeometry(100, 100, 400, 200)

        self.input_file = ""
        self.output_file = ""

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)

        self.input_label = QLabel("Plik wejściowy:", self)
        layout.addWidget(self.input_label)

        self.input_line_edit = QLineEdit(self)
        layout.addWidget(self.input_line_edit)

        self.input_button = QPushButton("Wybierz plik", self)
        self.input_button.clicked.connect(self.select_input_file)
        layout.addWidget(self.input_button)

        self.output_label = QLabel("Plik wyjściowy:", self)
        layout.addWidget(self.output_label)

        self.output_line_edit = QLineEdit(self)
        layout.addWidget(self.output_line_edit)

        self.output_button = QPushButton("Wybierz plik", self)
        self.output_button.clicked.connect(self.select_output_file)
        layout.addWidget(self.output_button)

        convert_button = QPushButton("Konwertuj", self)
        convert_button.clicked.connect(self.convert_data)
        layout.addWidget(convert_button)

    def select_input_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("XML files (*.xml);;JSON files (*.json);;YAML files (*.yaml)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.input_file = selected_files[0]
            self.input_line_edit.setText(self.input_file)

    def select_output_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("XML files (*.xml);;JSON files (*.json);;YAML files (*.yaml)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.output_file = selected_files[0]
            self.output_line_edit.setText(self.output_file)

    def convert_data(self):
        if not self.input_file or not self.output_file:
            QMessageBox.warning(self, "Błąd", "Wybierz plik wejściowy i plik wyjściowy.")
            return

        input_extension = self.input_file.split('.')[-1]
        output_extension = self.output_file.split('.')[-1]

        if input_extension == "json":
            data = self.load_json(self.input_file)

            if output_extension == "json":
                self.save_json(data, self.output_file)
            elif output_extension == "yaml":
                self.save_yaml(data, self.output_file)
            elif output_extension == "xml":
                root = ET.Element("data")
                self.convert_json_to_xml(data, root)
                self.save_xml(root, self.output_file)
            else:
                QMessageBox.warning(self, "Błąd", "Nieobsługiwany format pliku wyjściowego.")

        elif input_extension in ["yaml", "yml"]:
            data = self.load_yaml(self.input_file)

            if output_extension == "json":
                self.save_json(data, self.output_file)
            elif output_extension in ["yaml", "yml"]:
                self.save_yaml(data, self.output_file)
            elif output_extension == "xml":
                root = ET.Element("data")
                self.convert_yaml_to_xml(data, root)
                self.save_xml(root, self.output_file)
            else:
                QMessageBox.warning(self, "Błąd", "Nieobsługiwany format pliku wyjściowego.")

        elif input_extension == "xml":
            root = self.load_xml(self.input_file)

            if output_extension == "xml":
                self.save_xml(root, self.output_file)
            elif output_extension == "json":
                data = self.convert_xml_to_json(root)
                self.save_json(data, self.output_file)
            elif output_extension in ["yaml", "yml"]:
                data = self.convert_xml_to_yaml(root)
                self.save_yaml(data, self.output_file)
            else:
                QMessageBox.warning(self, "Błąd", "Nieobsługiwany format pliku wyjściowego.")

        else:
            QMessageBox.warning(self, "Błąd", "Nieobsługiwany format pliku wejściowego.")

        QMessageBox.information(self, "Sukces", "Konwertowanie danych zakończone powodzeniem.")

    def load_json(self, input_file):
        with open(input_file, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                QMessageBox.warning(self, "Błąd", f"Błąd w składni pliku JSON: {str(e)}")

    def save_json(self, data, output_file):
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)

    def load_yaml(self, input_file):
        with open(input_file, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                QMessageBox.warning(self, "Błąd", f"Błąd w składni pliku YAML: {str(e)}")

    def save_yaml(self, data, output_file):
        with open(output_file, 'w') as file:
            yaml.dump(data, file)

    def load_xml(self, input_file):
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            QMessageBox.warning(self, "Błąd", f"Błąd w składni pliku XML: {str(e)}")

    def save_xml(self, root, output_file):
        xml_string = ET.tostring(root, encoding='utf-8')
        with open(output_file, 'wb') as file:
            file.write(xml_string)

    def convert_json_to_xml(self, json_data, parent):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                element = ET.SubElement(parent, key)
                self.convert_json_to_xml(value, element)
        elif isinstance(json_data, list):
            for item in json_data:
                self.convert_json_to_xml(item, parent)
        else:
            parent.text = str(json_data)

    def convert_xml_to_json(self, root):
        json_data = {}
        for element in root:
            if element.text:
                json_data[element.tag] = element.text
            else:
                json_data[element.tag] = self.convert_xml_to_json(element)
        return json_data

    def convert_yaml_to_xml(self, yaml_data, parent):
        if isinstance(yaml_data, dict):
            for key, value in yaml_data.items():
                element = ET.SubElement(parent, key)
                self.convert_yaml_to_xml(value, element)
        elif isinstance(yaml_data, list):
            for item in yaml_data:
                self.convert_yaml_to_xml(item, parent)
        else:
            parent.text = str(yaml_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter_window = ConverterWindow()
    converter_window.show()
    sys.exit(app.exec_())
