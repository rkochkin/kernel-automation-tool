#!/usr/bin/env python3
import os
import sys
import argparse
from src.config import ConfigLoader
from src.builder import KernelBuilder

def main():
    parser = argparse.ArgumentParser(description='Kernel Builder')
    parser.add_argument('--config', '-c', 
                       default='config/default.yaml',
                       help='Path to configuration file')
    parser.add_argument('--clean', action='store_true',
                       help='Clean build artifacts')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = ConfigLoader.load(args.config)
        
        # Create builder
        builder = KernelBuilder(config)
        
        if args.clean:
            builder.clean()
            print("Clean completed")
            return
        
        # Build kernel
        success = builder.build()
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
