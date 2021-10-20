import yaml

from src.commands import BaseCommand


def read_yaml_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)


def main():
    config = read_yaml_config()
    base_command = BaseCommand(api_token=config['auth_token'],
                               base_url=config['base_url'],
                               timeout=config['timeout_seconds'],
                               max_retries=config['max_retries'])

    instruments = base_command.get_instruments()
    print(instruments)


if __name__ == "__main__":
    main()
