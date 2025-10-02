"""
Tests unitaires pour la classe RotationFactory.

Ce module contient tous les tests unitaires pour la classe RotationFactory.
"""

import pytest

from src.baobab_tree.balanced.rotations.rotation_factory import RotationFactory
from src.baobab_tree.balanced.rotations.left_rotation import LeftRotation
from src.baobab_tree.balanced.rotations.right_rotation import RightRotation
from src.baobab_tree.balanced.rotations.left_right_rotation import LeftRightRotation
from src.baobab_tree.balanced.rotations.right_left_rotation import RightLeftRotation
from src.baobab_tree.balanced.rotations.tree_rotation import TreeRotation
from src.baobab_tree.core.exceptions import InvalidRotationError


class TestRotationFactory:
    """Tests pour la classe RotationFactory."""

    def test_create_rotation_left(self):
        """Test de création de rotation gauche."""
        rotation = RotationFactory.create_rotation("left")
        assert isinstance(rotation, LeftRotation)
        assert rotation.rotation_type == "left"

    def test_create_rotation_right(self):
        """Test de création de rotation droite."""
        rotation = RotationFactory.create_rotation("right")
        assert isinstance(rotation, RightRotation)
        assert rotation.rotation_type == "right"

    def test_create_rotation_left_right(self):
        """Test de création de rotation gauche-droite."""
        rotation = RotationFactory.create_rotation("left_right")
        assert isinstance(rotation, LeftRightRotation)
        assert rotation.rotation_type == "left_right"

    def test_create_rotation_right_left(self):
        """Test de création de rotation droite-gauche."""
        rotation = RotationFactory.create_rotation("right_left")
        assert isinstance(rotation, RightLeftRotation)
        assert rotation.rotation_type == "right_left"

    def test_create_rotation_case_insensitive(self):
        """Test de création de rotation insensible à la casse."""
        rotation = RotationFactory.create_rotation("LEFT")
        assert isinstance(rotation, LeftRotation)
        
        rotation = RotationFactory.create_rotation("Right")
        assert isinstance(rotation, RightRotation)

    def test_create_rotation_with_whitespace(self):
        """Test de création de rotation avec espaces."""
        rotation = RotationFactory.create_rotation(" left ")
        assert isinstance(rotation, LeftRotation)
        
        rotation = RotationFactory.create_rotation("  right  ")
        assert isinstance(rotation, RightRotation)

    def test_create_rotation_invalid_type(self):
        """Test de création de rotation avec type invalide."""
        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.create_rotation("invalid")
        
        assert "Unknown rotation type 'invalid'" in str(exc_info.value)

    def test_create_rotation_none_type(self):
        """Test de création de rotation avec type None."""
        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.create_rotation(None)
        
        assert "Rotation type must be a string" in str(exc_info.value)

    def test_create_rotation_non_string_type(self):
        """Test de création de rotation avec type non-string."""
        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.create_rotation(123)
        
        assert "Rotation type must be a string" in str(exc_info.value)

    def test_get_available_types(self):
        """Test de récupération des types disponibles."""
        types = RotationFactory.get_available_types()
        expected_types = ["left", "right", "left_right", "right_left"]
        
        assert len(types) == len(expected_types)
        for expected_type in expected_types:
            assert expected_type in types

    def test_is_valid_type_valid(self):
        """Test de validation de type valide."""
        assert RotationFactory.is_valid_type("left") is True
        assert RotationFactory.is_valid_type("right") is True
        assert RotationFactory.is_valid_type("left_right") is True
        assert RotationFactory.is_valid_type("right_left") is True

    def test_is_valid_type_case_insensitive(self):
        """Test de validation de type insensible à la casse."""
        assert RotationFactory.is_valid_type("LEFT") is True
        assert RotationFactory.is_valid_type("Right") is True

    def test_is_valid_type_with_whitespace(self):
        """Test de validation de type avec espaces."""
        assert RotationFactory.is_valid_type(" left ") is True
        assert RotationFactory.is_valid_type("  right  ") is True

    def test_is_valid_type_invalid(self):
        """Test de validation de type invalide."""
        assert RotationFactory.is_valid_type("invalid") is False
        assert RotationFactory.is_valid_type("") is False

    def test_is_valid_type_non_string(self):
        """Test de validation de type non-string."""
        assert RotationFactory.is_valid_type(None) is False
        assert RotationFactory.is_valid_type(123) is False

    def test_register_rotation_type(self):
        """Test d'enregistrement de nouveau type de rotation."""
        class CustomRotation(TreeRotation):
            def __init__(self):
                super().__init__("custom")
            
            def rotate(self, node):
                return node
            
            def can_rotate(self, node):
                return True
            
            def get_description(self):
                return "Custom rotation"

        # Enregistrer le nouveau type
        RotationFactory.register_rotation_type("custom", CustomRotation)
        
        # Vérifier qu'il est disponible
        assert RotationFactory.is_valid_type("custom") is True
        
        # Créer une instance
        rotation = RotationFactory.create_rotation("custom")
        assert isinstance(rotation, CustomRotation)

    def test_register_rotation_type_invalid_type(self):
        """Test d'enregistrement avec type invalide."""
        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.register_rotation_type(None, LeftRotation)
        
        assert "Rotation type must be a string" in str(exc_info.value)

    def test_register_rotation_type_invalid_class(self):
        """Test d'enregistrement avec classe invalide."""
        class InvalidClass:
            pass

        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.register_rotation_type("invalid", InvalidClass)
        
        assert "Rotation class must inherit from TreeRotation" in str(exc_info.value)

    def test_unregister_rotation_type(self):
        """Test de désenregistrement de type de rotation."""
        # Enregistrer un type personnalisé
        class CustomRotation(TreeRotation):
            def __init__(self):
                super().__init__("custom")
            
            def rotate(self, node):
                return node
            
            def can_rotate(self, node):
                return True
            
            def get_description(self):
                return "Custom rotation"

        RotationFactory.register_rotation_type("custom", CustomRotation)
        assert RotationFactory.is_valid_type("custom") is True
        
        # Désenregistrer le type
        result = RotationFactory.unregister_rotation_type("custom")
        assert result is True
        assert RotationFactory.is_valid_type("custom") is False

    def test_unregister_rotation_type_nonexistent(self):
        """Test de désenregistrement de type inexistant."""
        result = RotationFactory.unregister_rotation_type("nonexistent")
        assert result is False

    def test_unregister_rotation_type_invalid_type(self):
        """Test de désenregistrement avec type invalide."""
        result = RotationFactory.unregister_rotation_type(None)
        assert result is False

    def test_create_all_rotations(self):
        """Test de création de toutes les rotations."""
        rotations = RotationFactory.create_all_rotations()
        
        assert len(rotations) == 4
        assert "left" in rotations
        assert "right" in rotations
        assert "left_right" in rotations
        assert "right_left" in rotations
        
        assert isinstance(rotations["left"], LeftRotation)
        assert isinstance(rotations["right"], RightRotation)
        assert isinstance(rotations["left_right"], LeftRightRotation)
        assert isinstance(rotations["right_left"], RightLeftRotation)

    def test_get_rotation_info(self):
        """Test de récupération d'informations sur une rotation."""
        info = RotationFactory.get_rotation_info("left")
        
        assert info["type"] == "left"
        assert info["class_name"] == "LeftRotation"
        assert "Rotation gauche" in info["description"]
        assert "left_rotation" in info["module"]

    def test_get_rotation_info_invalid_type(self):
        """Test de récupération d'informations avec type invalide."""
        with pytest.raises(InvalidRotationError) as exc_info:
            RotationFactory.get_rotation_info("invalid")
        
        assert "Unknown rotation type 'invalid'" in str(exc_info.value)

    def test_get_all_rotations_info(self):
        """Test de récupération d'informations sur toutes les rotations."""
        all_info = RotationFactory.get_all_rotations_info()
        
        assert len(all_info) == 4
        assert "left" in all_info
        assert "right" in all_info
        assert "left_right" in all_info
        assert "right_left" in all_info
        
        for rotation_type, info in all_info.items():
            assert "type" in info
            assert "class_name" in info
            assert "description" in info
            assert "module" in info
            assert info["type"] == rotation_type

    def test_str_representation(self):
        """Test de la représentation string."""
        factory = RotationFactory()
        str_repr = str(factory)
        assert "RotationFactory" in str_repr
        assert "available_types=4" in str_repr

    def test_repr_representation(self):
        """Test de la représentation détaillée."""
        factory = RotationFactory()
        repr_str = repr(factory)
        assert "RotationFactory" in repr_str
        assert "types=" in repr_str
        assert "left" in repr_str
        assert "right" in repr_str