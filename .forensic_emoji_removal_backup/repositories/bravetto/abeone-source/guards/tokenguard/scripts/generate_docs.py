from typing import Any
#!/usr/bin/env python3
"""
Generate API documentation from OpenAPI schema.

This script extracts the OpenAPI schema from the running service
and generates documentation in various formats.
"""

import argparse
import json
import sys
import requests
from pathlib import Path


def fetch_openapi_schema(base_url: str) -> dict:
    """Fetch OpenAPI schema from the running service."""
    try:
        url = f"{base_url.rstrip('/')}/openapi.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching OpenAPI schema: {e}")
        sys.exit(1)


def generate_markdown_docs(schema: dict, output_path: Path) -> Any:
    """Generate Markdown documentation from OpenAPI schema."""
    with open(output_path, 'w') as f:
        info = schema.get('info', {})
        f.write(f"# {info.get('title', 'API Documentation')}\n\n")
        f.write(f"{info.get('description', '')}\n\n")
        f.write(f"**Version:** {info.get('version', 'unknown')}\n\n")
        
        # Endpoints
        f.write("## Endpoints\n\n")
        paths = schema.get('paths', {})
        
        for path, methods in paths.items():
            f.write(f"### {path}\n\n")
            
            for method, details in methods.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                    f.write(f"#### {method.upper()}\n\n")
                    f.write(f"{details.get('summary', '')}\n\n")
                    
                    if 'description' in details:
                        f.write(f"{details['description']}\n\n")
                    
                    # Parameters
                    if 'parameters' in details:
                        f.write("**Parameters:**\n\n")
                        for param in details['parameters']:
                            f.write(f"- `{param.get('name')}` ({param.get('in')}) - {param.get('description', '')}\n")
                        f.write("\n")
                    
                    # Request body
                    if 'requestBody' in details:
                        f.write("**Request Body:**\n\n")
                        content = details['requestBody'].get('content', {})
                        for content_type, content_details in content.items():
                            f.write(f"Content-Type: `{content_type}`\n\n")
                            if 'schema' in content_details:
                                f.write("```json\n")
                                f.write(json.dumps(content_details['schema'].get('example', {}), indent=2))
                                f.write("\n```\n\n")
                    
                    # Responses
                    if 'responses' in details:
                        f.write("**Responses:**\n\n")
                        for code, response in details['responses'].items():
                            f.write(f"- `{code}`: {response.get('description', '')}\n")
                        f.write("\n")
                    
                    f.write("---\n\n")


def main() -> Any:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate API documentation")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the service"
    )
    parser.add_argument(
        "--output",
        default="API_DOCS.md",
        help="Output file path"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    print(f"Fetching OpenAPI schema from {args.url}...")
    schema = fetch_openapi_schema(args.url)
    
    output_path = Path(args.output)
    
    if args.format == "markdown":
        print(f"Generating Markdown documentation to {output_path}...")
        generate_markdown_docs(schema, output_path)
    elif args.format == "json":
        print(f"Saving OpenAPI schema to {output_path}...")
        with open(output_path, 'w') as f:
            json.dump(schema, f, indent=2)
    
    print("✅ Documentation generated successfully!")


if __name__ == "__main__":
    main()