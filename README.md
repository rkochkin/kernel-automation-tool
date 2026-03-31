# kernel-automation-tool
A minimalist universal kernel builder

## Implementation Features
* Versatility: Can work with any Git kernel repositories
* Flexible Configuration: YAML configs support various architectures and settings
* Patch Support: Automatically applies patches before building
* DeviceTree Build: Supports compiling multiple .dts files
* Modular Architecture: Easy to extend and modify
* Tests: Unit tests cover key components

## Project launch
### Installing dependencies:
```bash
pip install -r requirements.txt
```

### Running tests:
```bash
python -m pytest tests/ -v
```

### Building the kernel:
```bash
python main.py --config config/default.yaml
```

### Cleaning:
```bash
python main.py --clean
```
