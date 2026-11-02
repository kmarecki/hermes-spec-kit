# Spec-kit project .gitignore
# This is a starting point for new spec-kit projects.
# Spec artifacts (specs/) are documentation and SHOULD be committed.
# Add project-specific ignores below.

# spec-kit: the MCP server derives state from the files and persists nothing;
# a legacy state.json here is ignored and only causes merge conflicts.
specs/.spec-kit/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Node
node_modules/
dist/
.next/

# Go
/bin/

# Rust
/target/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
