#!/usr/bin/env python3
"""
Knowledge Base Article Generator
Quickly create new KB articles with proper formatting
"""

import os
import markdown
from datetime import datetime

def get_html_template():
    """Returns the HTML template for KB articles"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f7fa;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 25px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        pre code {{
            color: #ecf0f1;
            background: transparent;
        }}
        ul, ol {{
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}
        em {{
            color: #555;
            font-style: italic;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding: 10px 20px;
            margin: 20px 0;
            background: #f8f9fa;
            color: #555;
        }}
        .warning {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .info {{
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p><em>Last Updated: {date} | Category: {category}</em></p>
        </div>
    </div>
</body>
</html>
"""

def create_article_interactive():
    """Interactive article creator"""
    print("\n" + "=" * 60)
    print("📝 Knowledge Base Article Generator")
    print("=" * 60 + "\n")
    
    # Get client
    print("Available clients in Knowledge_Base/:")
    kb_dir = "Knowledge_Base"
    if os.path.exists(kb_dir):
        clients = [d for d in os.listdir(kb_dir) if os.path.isdir(os.path.join(kb_dir, d))]
        for i, client in enumerate(clients, 1):
            print(f"  {i}. {client}")
    else:
        print("  (No Knowledge_Base directory found)")
        clients = []
    
    print(f"  {len(clients) + 1}. Create new client folder")
    
    choice = input("\nSelect client (number or name): ").strip()
    
    if choice.isdigit() and int(choice) <= len(clients):
        client = clients[int(choice) - 1]
    elif choice.isdigit():
        client = input("Enter new client name: ").strip()
        os.makedirs(os.path.join(kb_dir, client), exist_ok=True)
        print(f"✓ Created folder: Knowledge_Base/{client}")
    else:
        client = choice
        os.makedirs(os.path.join(kb_dir, client), exist_ok=True)
    
    # Get article details
    print("\n" + "-" * 60)
    title = input("Article title: ").strip()
    category = input("Category (e.g., Security, Returns, Billing): ").strip()
    
    print("\nArticle content (type or paste, end with empty line + 'END'):")
    print("(Use markdown format: ## for headings, - for bullets, etc.)")
    print("-" * 60)
    
    content_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END" and (not content_lines or not content_lines[-1].strip()):
            break
        content_lines.append(line)
    
    # Remove trailing empty lines and END
    while content_lines and not content_lines[-1].strip():
        content_lines.pop()
    
    markdown_content = "# " + title + "\n\n" + "\n".join(content_lines)
    
    # Generate filename
    filename = title.replace(" ", "_").replace("/", "_").replace("\\", "_")
    filename = "".join(c for c in filename if c.isalnum() or c in "_-")
    
    md_path = os.path.join(kb_dir, client, filename + ".md")
    html_path = os.path.join(kb_dir, client, filename + ".html")
    
    # Add metadata
    markdown_content += f"\n\n---\n*Last Updated: {datetime.now().strftime('%Y-%m-%d')} | Category: {category}*\n"
    
    # Save markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"\n✓ Saved: {md_path}")
    
    # Convert to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra', 'nl2br', 'tables'])
    
    full_html = get_html_template().format(
        title=title,
        content=html_content,
        date=datetime.now().strftime('%Y-%m-%d'),
        category=category
    )
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✓ Saved: {html_path}")
    
    print("\n" + "=" * 60)
    print("✅ Article created successfully!")
    print(f"   Client: {client}")
    print(f"   Title: {title}")
    print(f"   Files: {filename}.md and {filename}.html")
    print("=" * 60)
    print("\n💡 Tip: Test it by searching for keywords from the title in the app!")

def batch_convert_existing():
    """Convert all existing .md files to HTML"""
    print("\n" + "=" * 60)
    print("🔄 Batch Convert Markdown to HTML")
    print("=" * 60 + "\n")
    
    kb_dir = "Knowledge_Base"
    if not os.path.exists(kb_dir):
        print("❌ Knowledge_Base directory not found")
        return
    
    converted = 0
    for root, dirs, files in os.walk(kb_dir):
        for file in files:
            if file.endswith('.md'):
                md_path = os.path.join(root, file)
                html_path = md_path.replace('.md', '.html')
                
                # Read markdown
                with open(md_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # Extract title (first # line)
                title = file.replace('.md', '').replace('_', ' ')
                for line in md_content.split('\n'):
                    if line.startswith('# '):
                        title = line[2:].strip()
                        break
                
                # Extract category from footer
                category = "General"
                if "Category:" in md_content:
                    try:
                        category = md_content.split("Category:")[-1].split("*")[0].strip()
                    except:
                        pass
                
                # Convert
                html_content = markdown.markdown(md_content, extensions=['extra', 'nl2br', 'tables'])
                
                full_html = get_html_template().format(
                    title=title,
                    content=html_content,
                    date=datetime.now().strftime('%Y-%m-%d'),
                    category=category
                )
                
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                print(f"✓ {md_path} → {html_path}")
                converted += 1
    
    print(f"\n✅ Converted {converted} files")
    print("=" * 60)

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "convert":
        batch_convert_existing()
    else:
        print("\nKnowledge Base Article Generator")
        print("1. Create new article (interactive)")
        print("2. Batch convert existing .md files to HTML")
        
        choice = input("\nSelect option (1 or 2): ").strip()
        
        if choice == "1":
            create_article_interactive()
        elif choice == "2":
            batch_convert_existing()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
