#!/usr/bin/env python3
"""
Script pour convertir les assertions pytest en assertions unittest.
"""

import re

def fix_assertions(content):
    """Convertit les assertions pytest en assertions unittest."""
    
    # Remplacer assert statements simples - plus précis
    content = re.sub(r'assert\s+([^=!<>]+)\s*==\s*([^,\n]+)', r'self.assertEqual(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s*!=\s*([^,\n]+)', r'self.assertNotEqual(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s*>\s*([^,\n]+)', r'self.assertGreater(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s*>=\s*([^,\n]+)', r'self.assertGreaterEqual(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s*<\s*([^,\n]+)', r'self.assertLess(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s*<=\s*([^,\n]+)', r'self.assertLessEqual(\1, \2)', content)
    
    # Remplacer assert is/is not
    content = re.sub(r'assert\s+([^=!<>]+)\s+is\s+None', r'self.assertIsNone(\1)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s+is\s+not\s+None', r'self.assertIsNotNone(\1)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s+is\s+([^,]+)', r'self.assertIs(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s+is\s+not\s+([^,]+)', r'self.assertIsNot(\1, \2)', content)
    
    # Remplacer assert in/not in
    content = re.sub(r'assert\s+([^=!<>]+)\s+in\s+([^,]+)', r'self.assertIn(\1, \2)', content)
    content = re.sub(r'assert\s+([^=!<>]+)\s+not\s+in\s+([^,]+)', r'self.assertNotIn(\1, \2)', content)
    
    # Remplacer assert True/False
    content = re.sub(r'assert\s+([^=!<>]+)', r'self.assertTrue(\1)', content)
    
    # Remplacer assert not
    content = re.sub(r'assert\s+not\s+([^,]+)', r'self.assertFalse(\1)', content)
    
    return content

def main():
    """Fonction principale."""
    with open('/workspace/tests/test_binary_search_tree.py', 'r') as f:
        content = f.read()
    
    # Appliquer les corrections
    content = fix_assertions(content)
    
    with open('/workspace/tests/test_binary_search_tree.py', 'w') as f:
        f.write(content)
    
    print("Tests corrigés avec succès!")

if __name__ == "__main__":
    main()