import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


def get_ssh_config_data():
    """Parse SSH config manually to avoid circular import"""
    config_path = os.path.expanduser("~/.ssh/config")
    if not os.path.isfile(config_path):
        raise Exception("SSH config is not present")
    
    hosts = []
    current_host = None
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.lower().startswith('host '):
                # Save previous host
                if current_host:
                    hosts.append(current_host)
                
                # Start new host
                host_name = line[5:].strip()
                current_host = {
                    "name": host_name,
                    "config": {}
                }
            elif current_host and line:
                # Parse config line
                parts = line.split(None, 1)
                if len(parts) == 2:
                    key, value = parts
                    current_host["config"][key] = value
        
        # Don't forget the last host
        if current_host:
            hosts.append(current_host)
    
    return hosts


def export_to_json(output_file: Optional[str] = None) -> str:
    """Export SSH config to JSON format"""
    hosts = get_ssh_config_data()
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "hosts": hosts
    }
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ssh_config_export_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    return output_file


def export_to_yaml(output_file: Optional[str] = None) -> str:
    """Export SSH config to YAML format"""
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
    
    hosts = get_ssh_config_data()
    
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "hosts": hosts
    }
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ssh_config_export_{timestamp}.yaml"
    
    with open(output_file, 'w') as f:
        yaml.dump(export_data, f, default_flow_style=False, indent=2)  # type: ignore
    
    return output_file


def export_raw_config(output_file: Optional[str] = None) -> str:
    """Export raw SSH config file with backup timestamp"""
    config_path = os.path.expanduser("~/.ssh/config")
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"ssh_config_backup_{timestamp}"
    
    with open(config_path, 'r') as src:
        with open(output_file, 'w') as dst:
            dst.write(f"# SSH Config backup created on {datetime.now().isoformat()}\n")
            dst.write(f"# Original file: {config_path}\n\n")
            dst.write(src.read())
    
    return output_file


def export_summary() -> Dict[str, Any]:
    """Generate a summary of the SSH configuration"""
    hosts = get_ssh_config_data()
    
    summary = {
        "total_hosts": len(hosts),
        "hosts_by_user": {},
        "identity_files": set(),
        "unique_hostnames": set(),
        "config_parameters": set()
    }
    
    for host in hosts:
        user = None
        hostname = None
        
        for key, value in host["config"].items():
            summary["config_parameters"].add(key)
            
            if key.lower() == "user":
                user = value
            elif key.lower() == "hostname":
                hostname = value
                summary["unique_hostnames"].add(value)
            elif key.lower() == "identityfile":
                summary["identity_files"].add(value)
        
        if user:
            summary["hosts_by_user"][user] = summary["hosts_by_user"].get(user, 0) + 1
    
    # Convert sets to lists for JSON serialization
    summary["identity_files"] = list(summary["identity_files"])
    summary["unique_hostnames"] = list(summary["unique_hostnames"])
    summary["config_parameters"] = list(summary["config_parameters"])
    
    return summary


def export_config(format_type: str = "json", output_file: Optional[str] = None, include_summary: bool = False) -> str:
    """Main export function supporting multiple formats"""
    
    if format_type.lower() == "json":
        exported_file = export_to_json(output_file)
    elif format_type.lower() == "yaml":
        exported_file = export_to_yaml(output_file)
    elif format_type.lower() == "raw":
        exported_file = export_raw_config(output_file)
    else:
        raise ValueError("Supported formats: json, yaml, raw")
    
    print(f"SSH config exported to: {exported_file}")
    
    if include_summary:
        summary = export_summary()
        summary_file = exported_file.replace('.', '_summary.')
        if not '.' in summary_file:
            summary_file += "_summary.json"
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Summary exported to: {summary_file}")
        print(f"Total hosts: {summary['total_hosts']}")
        print(f"Unique hostnames: {len(summary['unique_hostnames'])}")
        print(f"Identity files: {len(summary['identity_files'])}")
    
    return exported_file