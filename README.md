# hikari-gitbot

A bot for managing GitHub issues and PRs on Discord.

## Usage

Set the `TOKEN` environment variable to a valid Discord token, then run the bot:

```sh
docker compose up -d
```

## Development

Download [uv](https://docs.astral.sh/uv/), then run the following command to sync all dependencies:

```sh
uv sync --dev
```

A new venv will be created in the project root, and all dependencies will be installed.

To activate the venv, run:

```sh
source .venv/bin/activate
```

In addition, to check if the code is formatted correctly and passes all the type checks, run:

```sh
uv run nox
```

## License

This project is licensed under the GPL-v3 License - see the [LICENSE](LICENSE) file for details.
