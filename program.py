import argparse
import json
import os
import xml.etree.ElementTree as ET
import yaml


def convert_xml_to_json(input_path, output_path):
    tree = ET.parse(input_path)
    root = tree.getroot()
    data = xml_to_dict(root)
    json_data = json.dumps(data, indent=4)
    with open(output_path, 'w') as json_file:
        json_file.write(json_data)


def xml_to_dict(element):
    result = {}
    if element.attrib:
        result.update(element.attrib)
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    return result


def convert_json_to_xml(input_path, output_path):
    with open(input_path, 'r') as json_file:
        json_data = json.load(json_file)
        root = dict_to_xml(json_data)
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)


def dict_to_xml(data):
    if isinstance(data, dict):
        items = data.items()
    else:
        items = enumerate(data)
    root = ET.Element('root')
    for key, value in items:
        if isinstance(value, dict):
            element = dict_to_xml(value)
        elif isinstance(value, list):
            element = ET.Element(key)
            for item in value:
                sub_element = dict_to_xml(item)
                element.append(sub_element)
        else:
            element = ET.Element(key)
            element.text = str(value)
        root.append(element)
    return root


def convert_yaml_to_json(input_path, output_path):
    with open(input_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        json_data = json.dumps(yaml_data, indent=4)
        with open(output_path, 'w') as json_file:
            json_file.write(json_data)


def convert_json_to_yaml(input_path, output_path):
    with open(input_path, 'r') as json_file:
        json_data = json.load(json_file)
        yaml_data = yaml.safe_dump(json_data, default_flow_style=False)
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
