import os
import sys
import importlib.util

def run_migrations():
    """Run all migration scripts in the migrations directory."""
    migrations_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all Python files in the migrations directory
    migration_files = [f for f in os.listdir(migrations_dir) 
                      if f.endswith('.py') and f != '__init__.py' and f != 'run_migrations.py']
    
    # Sort them to ensure they run in a consistent order
    migration_files.sort()
    
    print(f"Found {len(migration_files)} migration files")
    
    for migration_file in migration_files:
        print(f"Running migration: {migration_file}")
        
        # Import the migration module
        module_name = os.path.splitext(migration_file)[0]
        file_path = os.path.join(migrations_dir, migration_file)
        
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Run the migration
        if hasattr(module, 'run_migration'):
            module.run_migration()
        else:
            print(f"Warning: {migration_file} does not have a run_migration function")

if __name__ == "__main__":
    run_migrations() 