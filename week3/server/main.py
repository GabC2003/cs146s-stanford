import os
import time
from typing import Any, Optional, Union, Dict
from datetime import datetime, date
from mcp.server.fastmcp import FastMCP
from massive import RESTClient
from importlib.metadata import version, PackageNotFoundError
from dotenv import load_dotenv
from formatters import json_to_csv
from functools import wraps
import json
# Load environment variables
load_dotenv()

MASSIVE_API_KEY = os.environ.get("MASSIVE_API_KEY", "")
massive_client = RESTClient(MASSIVE_API_KEY)


version_number = "MCP-Massive/unknown"
try:
    version_number = f"MCP-Massive/{version('mcp_massive')}"
except PackageNotFoundError:
    pass

if "User-Agent" not in massive_client.headers:
    massive_client.headers["User-Agent"] = version_number
else:
    massive_client.headers["User-Agent"] += f" {version_number}"

mcp = FastMCP("massive")

def safe_massive_call(func):
    """
    装饰器：增加重试机制和错误捕获。
    注意：使用 @wraps 保留原函数的元数据（如文档字符串），这对 MCP 工具生成很重要。
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_retries = 3
        backoff_factor = 1
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                msg = str(e).lower()
                
                # 429 Rate Limiting
                if "429" in msg or "too many requests" in msg:
                    if attempt < max_retries - 1:
                        sleep_time = backoff_factor * (2 ** attempt)
                        # 因为这是同步函数，使用 time.sleep 是安全的（在线程池中运行）
                        time.sleep(sleep_time)
                        continue
                    return "⚠️ API 速率限制已达到 (429)。请稍后重试。"
                
                # 404 Not Found
                if "404" in msg or "not found" in msg:
                    return f"❌ 未找到请求的数据 (404)。"
                
                # Timeouts
                if "timeout" in msg or "timed out" in msg:
                     # 可以在这里增加重试逻辑，或者直接返回
                     if attempt < max_retries - 1:
                         continue
                     return "⏱️ 请求超时。请检查网络连接或稍后重试。"

                # 其他错误，非最后一次尝试则继续，否则返回错误
                if attempt == max_retries - 1:
                    return f"❌ API 请求失败: {str(e)}"
        return "❌ 请求失败，已达到最大重试次数。"
    return wrapper

@mcp.tool()
@safe_massive_call
def get_stock_info(ticker: str) -> str:
    """
    Retrieve previous day's aggregate trading data and recent corporate actions.
    """
    ticker_norm = ticker.upper()
    sections = []
    
    # 1. Previous Day Aggregates
    try:
        resp = massive_client.get_previous_close_agg(ticker_norm, adjusted="true", raw=True)
        # 假设 resp.data 是 bytes，需要 decode
        sections.append(f"### Previous Close\n{json_to_csv(resp.data.decode('utf-8'))}")
    except Exception as e:
        sections.append(f"### Previous Close\nData not available or Error: {e}")
    
    # 2. Recent Dividends
    try:
        resp = massive_client.list_dividends(ticker=ticker_norm, limit=1, raw=True)
        sections.append(f"### Recent Dividends\n{json_to_csv(resp.data.decode('utf-8'))}")
    except Exception:
        pass # 忽略非关键错误

    # 3. Corporate Actions
    try:
        resp = massive_client.get_ticker_events(ticker=ticker_norm, limit=3, raw=True)
        sections.append(f"### Corporate Actions\n{json_to_csv(resp.data.decode('utf-8'))}")
    except Exception:
        pass

    return "\n\n".join(sections)

@mcp.tool()
@safe_massive_call
def list_treasury_yields(
    limit: Optional[int] = 10,
    sort: Optional[str] = "date.desc"
) -> str:
    """Get US Treasury Yields data in CSV format."""
    
    # 更安全的分割逻辑
    field = "date"
    direction = "desc"
    if sort and "." in sort:
        field, direction = sort.split(".", 1)
    elif sort:
        field = sort # 假设用户只传了字段名
            
    resp = massive_client.list_treasury_yields(
        limit=limit,
        sort=field,
        order=direction,
        raw=True
    )
    return json_to_csv(resp.data.decode("utf-8"))

@mcp.tool()
@safe_massive_call
def list_inflation(
    limit: Optional[int] = 10,
    sort: Optional[str] = "date.desc"
) -> str:
    """Get US Inflation data (CPI, PCE) in CSV format."""
    resp = massive_client.list_inflation(
        limit=limit,
        sort=sort,
        raw=True
    )
    return json_to_csv(resp.data.decode("utf-8"))

@mcp.tool()
@safe_massive_call
def list_inflation_expectations(
    limit: Optional[int] = 10,
    sort: Optional[str] = "date.desc"
) -> str:
    """Get US Inflation Expectations data in CSV format."""
    resp = massive_client.list_inflation_expectations(
        limit=limit,
        sort=sort,
        raw=True
    )
    return json_to_csv(resp.data.decode("utf-8"))

@mcp.tool()
@safe_massive_call
def list_ticker_news(
    ticker: Optional[str] = None,
    published_utc: Optional[Union[str, datetime, date]] = None,
    limit: Optional[int] = 10,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    """Get recent news articles for a stock ticker."""
    results = massive_client.list_ticker_news(
        ticker=ticker,
        published_utc=published_utc,
        limit=limit,
        sort=sort,
        order=order,
        params=params,
        raw=True,
    )
    return json_to_csv(results.data.decode("utf-8"))

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()