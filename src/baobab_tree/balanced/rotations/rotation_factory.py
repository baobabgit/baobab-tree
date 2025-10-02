"""
Factory pour créer des instances de rotations d'arbres.

Ce module implémente la classe RotationFactory qui permet de créer des instances
de rotations selon le type spécifié.
"""

from typing import Dict, Type, TYPE_CHECKING

from ...core.exceptions import InvalidRotationError
from .left_rotation import LeftRotation
from .left_right_rotation import LeftRightRotation
from .right_left_rotation import RightLeftRotation
from .right_rotation import RightRotation
from .tree_rotation import TreeRotation

if TYPE_CHECKING:
    from ...binary.binary_tree_node import BinaryTreeNode


class RotationFactory:
    """
    Factory pour créer des instances de rotations.

    Cette classe fournit des méthodes statiques pour créer des instances de rotations
    selon le type spécifié. Elle maintient un registre des types de rotations
    disponibles et valide les types demandés.

    Types de rotations supportés :
    - "left" : LeftRotation
    - "right" : RightRotation
    - "left_right" : LeftRightRotation
    - "right_left" : RightLeftRotation
    """

    # Registre des types de rotations disponibles
    _ROTATION_TYPES: Dict[str, Type[TreeRotation]] = {
        "left": LeftRotation,
        "right": RightRotation,
        "left_right": LeftRightRotation,
        "right_left": RightLeftRotation,
    }

    @classmethod
    def create_rotation(cls, rotation_type: str) -> TreeRotation:
        """
        Crée une rotation selon le type spécifié.

        Cette méthode crée une nouvelle instance de rotation selon le type
        spécifié. Elle valide le type et retourne l'instance appropriée.

        :param rotation_type: Type de rotation à créer
        :type rotation_type: str
        :return: Instance de rotation créée
        :rtype: TreeRotation
        :raises InvalidRotationError: Si le type de rotation est invalide
        """
        if not isinstance(rotation_type, str):
            raise InvalidRotationError(
                f"Rotation type must be a string, got {type(rotation_type).__name__}",
                str(rotation_type),
            )

        rotation_type = rotation_type.lower().strip()

        if rotation_type not in cls._ROTATION_TYPES:
            available_types = ", ".join(cls._ROTATION_TYPES.keys())
            raise InvalidRotationError(
                f"Unknown rotation type '{rotation_type}'. Available types: {available_types}",
                rotation_type,
            )

        rotation_class = cls._ROTATION_TYPES[rotation_type]
        return rotation_class()

    @classmethod
    def get_available_types(cls) -> list:
        """
        Retourne la liste des types de rotations disponibles.

        :return: Liste des types de rotations disponibles
        :rtype: list
        """
        return list(cls._ROTATION_TYPES.keys())

    @classmethod
    def is_valid_type(cls, rotation_type: str) -> bool:
        """
        Vérifie si un type de rotation est valide.

        :param rotation_type: Type de rotation à vérifier
        :type rotation_type: str
        :return: True si le type est valide, False sinon
        :rtype: bool
        """
        if not isinstance(rotation_type, str):
            return False

        return rotation_type.lower().strip() in cls._ROTATION_TYPES

    @classmethod
    def register_rotation_type(cls, rotation_type: str, rotation_class: Type[TreeRotation]) -> None:
        """
        Enregistre un nouveau type de rotation.

        Cette méthode permet d'enregistrer un nouveau type de rotation dans le factory.
        Utile pour l'extensibilité et les rotations personnalisées.

        :param rotation_type: Nom du type de rotation
        :type rotation_type: str
        :param rotation_class: Classe de rotation à enregistrer
        :type rotation_class: Type[TreeRotation]
        :raises InvalidRotationError: Si le type ou la classe est invalide
        """
        if not isinstance(rotation_type, str):
            raise InvalidRotationError(
                f"Rotation type must be a string, got {type(rotation_type).__name__}",
                str(rotation_type),
            )

        if not issubclass(rotation_class, TreeRotation):
            raise InvalidRotationError(
                f"Rotation class must inherit from TreeRotation, got {rotation_class.__name__}",
                rotation_type,
            )

        cls._ROTATION_TYPES[rotation_type.lower().strip()] = rotation_class

    @classmethod
    def unregister_rotation_type(cls, rotation_type: str) -> bool:
        """
        Désenregistre un type de rotation.

        Cette méthode permet de supprimer un type de rotation du factory.

        :param rotation_type: Nom du type de rotation à supprimer
        :type rotation_type: str
        :return: True si le type a été supprimé, False s'il n'existait pas
        :rtype: bool
        """
        if not isinstance(rotation_type, str):
            return False

        rotation_type = rotation_type.lower().strip()
        if rotation_type in cls._ROTATION_TYPES:
            del cls._ROTATION_TYPES[rotation_type]
            return True

        return False

    @classmethod
    def create_all_rotations(cls) -> Dict[str, TreeRotation]:
        """
        Crée toutes les rotations disponibles.

        Cette méthode crée une instance de chaque type de rotation disponible
        et retourne un dictionnaire associant les types aux instances.

        :return: Dictionnaire des rotations créées
        :rtype: Dict[str, TreeRotation]
        """
        rotations = {}
        for rotation_type in cls._ROTATION_TYPES:
            rotations[rotation_type] = cls.create_rotation(rotation_type)

        return rotations

    @classmethod
    def get_rotation_info(cls, rotation_type: str) -> Dict[str, str]:
        """
        Retourne les informations sur un type de rotation.

        :param rotation_type: Type de rotation
        :type rotation_type: str
        :return: Informations sur la rotation
        :rtype: Dict[str, str]
        :raises InvalidRotationError: Si le type de rotation est invalide
        """
        if not cls.is_valid_type(rotation_type):
            raise InvalidRotationError(
                f"Unknown rotation type '{rotation_type}'", rotation_type
            )

        rotation_type = rotation_type.lower().strip()
        rotation_class = cls._ROTATION_TYPES[rotation_type]
        rotation_instance = rotation_class()

        return {
            "type": rotation_type,
            "class_name": rotation_class.__name__,
            "description": rotation_instance.get_description(),
            "module": rotation_class.__module__,
        }

    @classmethod
    def get_all_rotations_info(cls) -> Dict[str, Dict[str, str]]:
        """
        Retourne les informations sur tous les types de rotations.

        :return: Dictionnaire des informations sur toutes les rotations
        :rtype: Dict[str, Dict[str, str]]
        """
        info = {}
        for rotation_type in cls._ROTATION_TYPES:
            info[rotation_type] = cls.get_rotation_info(rotation_type)

        return info

    def __str__(self) -> str:
        """
        Retourne la représentation string du factory.

        :return: Représentation string
        :rtype: str
        """
        return f"RotationFactory(available_types={len(self._ROTATION_TYPES)})"

    def __repr__(self) -> str:
        """
        Retourne la représentation détaillée du factory.

        :return: Représentation détaillée
        :rtype: str
        """
        return f"RotationFactory(types={list(self._ROTATION_TYPES.keys())})"