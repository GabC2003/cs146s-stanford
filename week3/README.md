# Week 3 - MCP Massive Stocks Server

A Model Context Protocol (MCP) server that provides access to financial market data through the Massive API. This server exposes stock information, treasury yields, inflation data, and stock news as MCP tools that can be used by AI assistants like Claude Desktop or Cursor.

## Features

- **Stock Information**: Retrieve previous day's trading data, dividends, and corporate actions for any stock ticker
- **Treasury Yields**: Access US Treasury Yields data with customizable sorting
- **Inflation Data**: Get US Inflation data (CPI, PCE) in CSV format
- **Inflation Expectations**: Retrieve US Inflation Expectations data
- **Stock News**: Fetch recent news articles for stock tickers with sentiment analysis
- **Robust Error Handling**: Automatic retry with exponential backoff for rate limits and network errors
- **CSV Output**: All data is formatted as CSV for easy consumption

## Prerequisites

- Python 3.11 or higher
- A Massive API key (get one at [massive.com](https://massive.com))
- MCP client (Claude Desktop, Cursor, or another MCP-compatible client)

## Installation

1. Navigate to the week3 directory:

```bash
cd week3
```

2. Install dependencies using uv (recommended) or pip:

```bash
# Using uv
uv sync

# Or using pip
pip install -r requirements.txt  # if available
```

3. Set up your environment variables. Create a `.env` file in the `week3/` directory:

```bash
MASSIVE_API_KEY=your_api_key_here
```

## Running the Server

### Local STDIO Mode (Recommended)

Run the server using stdio transport:

```bash
cd week3
uv run python server/main.py
```

Or if using pip:

```bash
python server/main.py
```

The server will communicate via stdin/stdout, which is the standard way MCP servers work with clients.

## MCP Client Configuration

### Claude Desktop

Add the following to your Claude Desktop configuration file (location varies by OS):

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "massive-stocks": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/modern-software-dev-assignments/week3",
        "run",
        "python",
        "server/main.py"
      ],
      "env": {
        "MASSIVE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Note**: Replace `/path/to/modern-software-dev-assignments/week3` with your actual project path.

### Cursor

Cursor should automatically detect MCP servers. Ensure your `.env` file is in the `week3/` directory with the `MASSIVE_API_KEY` set.

## Available Tools

### 1. `get_stock_info`

Retrieve previous day's aggregate trading data and recent corporate actions for a stock.

**Parameters:**

- `ticker` (string, required): Stock ticker symbol (e.g., "AAPL", "GOOGL", "MSFT")

**Returns:**
CSV-formatted data including:

- Previous Close: Previous day's trading aggregates
- Recent Dividends: Latest dividend information
- Corporate Actions: Recent corporate events (up to 3)

**Example:**

```
get_stock_info(ticker="AAPL")
```

### 2. `list_treasury_yields`

Get US Treasury Yields data in CSV format.

**Parameters:**

- `limit` (integer, optional): Number of records to return (default: 10)
- `sort` (string, optional): Sort field and direction in format "field.direction" (default: "date.desc")
  - Examples: "date.desc", "date.asc", "yield.desc"

**Returns:**
CSV-formatted treasury yields data

**Example:**

```
list_treasury_yields(limit=20, sort="date.desc")
```

### 3. `list_inflation`

Get US Inflation data (CPI, PCE) in CSV format.

**Parameters:**

- `limit` (integer, optional): Number of records to return (default: 10)
- `sort` (string, optional): Sort field (default: "date.desc")

**Returns:**
CSV-formatted inflation data

**Example:**

```
list_inflation(limit=12, sort="date.desc")
```

### 4. `list_inflation_expectations`

Get US Inflation Expectations data in CSV format.

**Parameters:**

- `limit` (integer, optional): Number of records to return (default: 10)
- `sort` (string, optional): Sort field (default: "date.desc")

**Returns:**
CSV-formatted inflation expectations data

**Example:**

```
list_inflation_expectations(limit=10)
```

### 5. `list_ticker_news`

Get recent news articles for a stock ticker with sentiment analysis.

**Parameters:**

- `ticker` (string, optional): Stock ticker symbol (e.g., "GOOGL", "AAPL")
- `published_utc` (string/datetime/date, optional): Filter by publication date
- `limit` (integer, optional): Number of articles to return (default: 10)
- `sort` (string, optional): Sort field
- `order` (string, optional): Sort order ("asc" or "desc")
- `params` (dict, optional): Additional query parameters

**Returns:**
CSV-formatted news data including:

- Article metadata (title, author, publisher, publication date)
- Article URL and description
- Related tickers
- Sentiment analysis with reasoning

**Example:**

```
list_ticker_news(ticker="GOOGL", limit=10)
```

## Error Handling

The server implements robust error handling with automatic retry logic:

- **Rate Limiting (429)**: Automatically retries with exponential backoff (up to 3 attempts)
- **Not Found (404)**: Returns a clear error message
- **Timeouts**: Retries with exponential backoff
- **Other Errors**: Returns descriptive error messages

All errors are returned as user-friendly messages in Chinese, indicating the type of error and suggested actions.

## Project Structure

```
week3/
├── server/
│   ├── main.py          # MCP server implementation
│   └── formatters.py    # JSON to CSV conversion utilities
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Example Usage Flow

1. **Start the MCP server** (if running manually):

   ```bash
   cd week3
   uv run python server/main.py
   ```

2. **In your MCP client** (Claude Desktop, Cursor, etc.), you can now:

   - Ask: "Get me the latest news about Google stock"
   - Ask: "What's the current inflation rate?"
   - Ask: "Show me Apple's stock information"
   - Ask: "Get the latest treasury yields"

3. **The AI assistant** will automatically call the appropriate MCP tools and return formatted CSV data.

## Dependencies

- `mcp[cli]>=1.25.0`: Model Context Protocol framework
- `massive>=2.0.3`: Massive API client
- `python-dotenv>=1.2.1`: Environment variable management
- `httpx>=0.28.1`: HTTP client library

## Notes

- All API responses are converted to CSV format for consistency
- The server uses stdio transport, which is the standard for local MCP servers
- User-Agent headers are automatically set to identify the MCP client
- The server handles nested JSON structures by flattening them in CSV output

## Troubleshooting

**Issue**: "name 'json' is not defined"

- **Solution**: Ensure `formatters.py` has all required imports. This should be fixed in the current version.

**Issue**: "API 速率限制已达到 (429)"

- **Solution**: The server will automatically retry. Wait a moment and try again, or check your API rate limits.

**Issue**: Server not detected by client

- **Solution**:
  - Verify the path in your MCP client configuration is correct
  - Ensure the server is executable and dependencies are installed
  - Check that `MASSIVE_API_KEY` is set in your environment or `.env` file

## License

This project is part of a course assignment and is for educational purposes.
