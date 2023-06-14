import argparse
import json
import os
import xmltodict
import yaml


def convert_xml_to_json(input_path, output_path):
    with open(input_path, 'r') as xml_file:
        xml_data = xml_file.read()
        json_data = json.dumps(xmltodict.parse(xml_data), indent=4)
        with open(output_path, 'w') as json_file:
            json_file.write(json_data)


def convert_json_to_xml(input_path, output_path):
    with open(input_path, 'r') as json_file:
        json_data = json_file.read()
        xml_data = xmltodict.unparse(json.loads(json_data), pretty=True)
        with open(output_path, 'w') as xml_file:
            xml_file.write(xml_data)


def convert_yaml_to_json(input_path, output_path):
    with open(input_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        json_data = json.dumps(yaml_data, indent=4)
        with open(output_path, 'w') as json_file:
            json_file.write(json_data)


def convert_json_to_yaml(input_path, output_path):
    with open(input_path, 'r') as json_file:
        json_data = json_file.read()
        yaml_data = yaml.safe_dump(json.loads(json_data), default_flow_style=False)
        with open(output_path, 'w') as yaml_file:
            yaml_file.write(yaml_data)


def convert_files(input_path, output_path):
    _, input_extension = os.path.splitext(input_path)
    _, output_extension = os.path.splitext(output_path)

    if input_extension == '.xml' and output_extension == '.json':
        convert_xml_to_json(input_path, output_path)
    elif input_extension == '.json' and output_extension == '.xml':
        convert_json_to_xml(input_path, output_path)
    elif input_extension == '.yaml' and output_extension == '.json':
        convert_yaml_to_json(input_path, output_path)
    elif input_extension == '.json' and output_extension == '.yaml':
        convert_json_to_yaml(input_path, output_path)
    else:
        print('Nieprawidłowe rozszerzenia plików. Wspierane są tylko .xml, .json i .yaml.')


def main():
    parser = argparse.ArgumentParser(description='Program do konwersji danych w różnych formatach.')
    parser.add_argument('input_path', type=str, help='Ścieżka do pliku wejściowego.')
    parser.add_argument('output_path', type=str, help='Ścieżka do pliku wyjściowego.')
    args = parser.parse_args()

    convert_files(args.input_path, args.output_path)


if __name__ == '__main__':
    main()

