# SSJ (SSH Toolkit)

A command-line tool to simplify management of your `~/.ssh/config` file.

## Features

- **List Hosts:** View your SSH hosts in a clean table, simple list, or JSON format.
- **Add Hosts:** Easily add new host configurations.
- **Edit Hosts:** Modify existing host configurations.
- **Copy Hosts:** Duplicate host configurations.
- **Remove Hosts:** Delete hosts from your configuration.
- **Connect:**
    - Interactive connection from a numbered list.
    - Direct connection by host alias.
    - Fuzzy find and connect using `fzf`.

## Installation

See [INSTALL.md](INSTALL.md) for installation instructions.

## Usage

### List Hosts

```bash
# Display hosts in a table (default)
ssj list

# Display a simple list of host names
ssj list --ls

# Display hosts in JSON format
ssj list --json
```

### Add a Host

```bash
ssj add <hostname> [-n <name>] [-i <identity_file>]
```

-   `<hostname>`: The hostname or user@hostname.
-   `-n, --name`: (Optional) The alias for the host.
-   `-i, --identity`: (Optional) Path to the identity file.

### Edit a Host

```bash
# Select a host to edit from a list
ssj edit

# Edit a specific host
ssj edit <host_alias>
```

### Copy a Host

```bash
ssj copy <source_host> <new_host_name>
```

### Remove a Host

```bash
# Select a host to remove from a list
ssj remove

# Remove a specific host
ssj remove <host_alias>
```

### Connect to a Host

```bash
# Select a host to connect to from a numbered list
ssj

# Connect to a host using fzf for fuzzy finding
ssj --fzf

# Connect directly to a host
ssj connect <host_alias>
```

