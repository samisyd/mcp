# MCP Multi-Server Demo (Math + Weather)

A small Python project that demonstrates using a LangChain agent with multiple MCP servers via `MultiServerMCPClient`.

- `mathserver.py` exposes math tools over MCP using `stdio` transport.
- `weather.py` exposes a weather tool over MCP using `streamable-http` transport.
- `client.py` connects to both servers, builds an agent, and asks sample questions.

## Project Structure

- `client.py` - MCP client + LangChain agent
- `mathserver.py` - local math MCP server (`add`, `subtract`, `multiply`)
- `weather.py` - weather MCP server (`get_weather`)
- `main.py` - basic placeholder entry script

## Requirements

- Python 3.13+
- API key for at least one model provider used by the client
	- `OPENAI_API_KEY` (currently used by the agent)
	- `GROQ_API_KEY` (initialized in code, but not currently passed to the agent)

Install dependencies:

```bash
pip install -r requirements.txt
```

If you get an error for missing dotenv support, install:

```bash
pip install python-dotenv
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

## How It Works

`client.py` configures two MCP endpoints:

- `math`: starts `mathserver.py` as a subprocess using `stdio`
- `weather`: connects to `http://localhost:8000/mcp` using `streamable-http`

The client retrieves tools from both servers and uses a LangChain agent to answer:

1. `What is (3 + 5) and then multiply by 12?`
2. `What is the weather in California?`

## Run the Project

### 1) Start the weather MCP server

In terminal A:

```bash
python weather.py
```

### 2) Run the client

In terminal B:

```bash
python client.py
```

You should see output similar to:

```text
Math response: ...
Weather response: ...
```

## Notes

- `mathserver.py` is launched automatically by `client.py`.
- `weather.py` must be running before starting `client.py`.
- `main.py` is independent and currently only prints a hello message.

## Troubleshooting

- **Tool loading fails**: confirm `weather.py` is running and reachable at `http://localhost:8000/mcp`.
- **Auth/model errors**: check `.env` values for API keys.
- **Module not found**: reinstall dependencies from `requirements.txt`.
