"""
Exceptions personnalisées pour la librairie d'arbres.

Ce module définit toutes les exceptions spécifiques utilisées dans la librairie
d'arbres pour une gestion d'erreurs robuste et informative.
"""


class TreeNodeError(Exception):
    """
    Exception de base pour toutes les erreurs liées aux nœuds d'arbres.

    Cette exception sert de classe de base pour toutes les erreurs spécifiques
    aux nœuds d'arbres, permettant une gestion d'erreurs hiérarchique.

    :param message: Message d'erreur descriptif
    :type message: str
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: TreeNode, optional
    """

    def __init__(self, message: str, node=None):
        """
        Initialise l'exception TreeNodeError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: TreeNode, optional
        """
        super().__init__(message)
        self.message = message
        self.node = node

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur le nœud si disponible
        :rtype: str
        """
        if self.node is not None:
            return f"{self.message} (Node: {self.node})"
        return self.message


class InvalidNodeOperationError(TreeNodeError):
    """
    Exception levée lors d'une opération invalide sur un nœud.

    Cette exception est levée quand une opération est tentée sur un nœud
    dans un état qui ne permet pas cette opération.

    :param message: Message d'erreur descriptif
    :type message: str
    :param operation: Nom de l'opération invalide
    :type operation: str
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: TreeNode, optional
    """

    def __init__(self, message: str, operation: str, node=None):
        """
        Initialise l'exception InvalidNodeOperationError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param operation: Nom de l'opération invalide
        :type operation: str
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: TreeNode, optional
        """
        super().__init__(message, node)
        self.operation = operation

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur l'opération
        :rtype: str
        """
        base_msg = super().__str__()
        return f"{base_msg} (Operation: {self.operation})"


class CircularReferenceError(TreeNodeError):
    """
    Exception levée lors de la détection d'une référence circulaire.

    Cette exception est levée quand une opération créerait une référence
    circulaire dans la structure d'arbre, ce qui est interdit.

    :param message: Message d'erreur descriptif
    :type message: str
    :param node1: Premier nœud impliqué dans la référence circulaire
    :type node1: TreeNode
    :param node2: Deuxième nœud impliqué dans la référence circulaire
    :type node2: TreeNode
    """

    def __init__(self, message: str, node1, node2):
        """
        Initialise l'exception CircularReferenceError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param node1: Premier nœud impliqué dans la référence circulaire
        :type node1: TreeNode
        :param node2: Deuxième nœud impliqué dans la référence circulaire
        :type node2: TreeNode
        """
        super().__init__(message, node1)
        self.node1 = node1
        self.node2 = node2

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur les nœuds impliqués
        :rtype: str
        """
        return f"{self.message} (Node1: {self.node1}, Node2: {self.node2})"


class NodeValidationError(TreeNodeError):
    """
    Exception levée lors de l'échec de validation d'un nœud.

    Cette exception est levée quand un nœud ne passe pas les validations
    de ses propriétés ou de son état.

    :param message: Message d'erreur descriptif
    :type message: str
    :param validation_rule: Règle de validation qui a échoué
    :type validation_rule: str
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: TreeNode, optional
    """

    def __init__(self, message: str, validation_rule: str, node=None):
        """
        Initialise l'exception NodeValidationError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param validation_rule: Règle de validation qui a échoué
        :type validation_rule: str
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: TreeNode, optional
        """
        super().__init__(message, node)
        self.validation_rule = validation_rule

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur la règle de validation
        :rtype: str
        """
        base_msg = super().__str__()
        return f"{base_msg} (Validation rule: {self.validation_rule})"


class BSTError(Exception):
    """
    Exception de base pour toutes les erreurs liées aux arbres binaires de recherche.

    Cette exception sert de classe de base pour toutes les erreurs spécifiques
    aux BST, permettant une gestion d'erreurs hiérarchique.

    :param message: Message d'erreur descriptif
    :type message: str
    :param operation: Opération qui a causé l'erreur (optionnel)
    :type operation: str, optional
    """

    def __init__(self, message: str, operation: str = None):
        """
        Initialise l'exception BSTError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param operation: Opération qui a causé l'erreur (optionnel)
        :type operation: str, optional
        """
        super().__init__(message)
        self.message = message
        self.operation = operation

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur l'opération si disponible
        :rtype: str
        """
        if self.operation is not None:
            return f"{self.message} (Operation: {self.operation})"
        return self.message


class DuplicateValueError(BSTError):
    """
    Exception levée lors de la tentative d'insertion d'une valeur dupliquée.

    Cette exception est levée quand on tente d'insérer une valeur qui existe
    déjà dans l'arbre binaire de recherche.

    :param message: Message d'erreur descriptif
    :type message: str
    :param value: Valeur dupliquée
    :type value: Any
    :param operation: Opération qui a causé l'erreur
    :type operation: str
    """

    def __init__(self, message: str, value, operation: str = "insert"):
        """
        Initialise l'exception DuplicateValueError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param value: Valeur dupliquée
        :type value: Any
        :param operation: Opération qui a causé l'erreur
        :type operation: str
        """
        super().__init__(message, operation)
        self.value = value

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur la valeur dupliquée
        :rtype: str
        """
        return f"{self.message} (Value: {self.value})"


class ValueNotFoundError(BSTError):
    """
    Exception levée lors de la recherche d'une valeur inexistante.

    Cette exception est levée quand on tente d'effectuer une opération
    sur une valeur qui n'existe pas dans l'arbre binaire de recherche.

    :param message: Message d'erreur descriptif
    :type message: str
    :param value: Valeur non trouvée
    :type value: Any
    :param operation: Opération qui a causé l'erreur
    :type operation: str
    """

    def __init__(self, message: str, value, operation: str = "search"):
        """
        Initialise l'exception ValueNotFoundError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param value: Valeur non trouvée
        :type value: Any
        :param operation: Opération qui a causé l'erreur
        :type operation: str
        """
        super().__init__(message, operation)
        self.value = value

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur la valeur non trouvée
        :rtype: str
        """
        return f"{self.message} (Value: {self.value})"


class InvalidOperationError(BSTError):
    """
    Exception levée lors d'une opération invalide sur un BST.

    Cette exception est levée quand une opération est tentée sur un BST
    dans un état qui ne permet pas cette opération.

    :param message: Message d'erreur descriptif
    :type message: str
    :param operation: Opération invalide
    :type operation: str
    """

    def __init__(self, message: str, operation: str):
        """
        Initialise l'exception InvalidOperationError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param operation: Opération invalide
        :type operation: str
        """
        super().__init__(message, operation)


class AVLError(Exception):
    """
    Exception de base pour toutes les erreurs liées aux arbres AVL.

    Cette exception sert de classe de base pour toutes les erreurs spécifiques
    aux arbres AVL, permettant une gestion d'erreurs hiérarchique.

    :param message: Message d'erreur descriptif
    :type message: str
    :param operation: Opération qui a causé l'erreur (optionnel)
    :type operation: str, optional
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(self, message: str, operation: str = None, node=None):
        """
        Initialise l'exception AVLError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param operation: Opération qui a causé l'erreur (optionnel)
        :type operation: str, optional
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message)
        self.message = message
        self.operation = operation
        self.node = node

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur l'opération et le nœud si disponibles
        :rtype: str
        """
        result = self.message
        if self.operation is not None:
            result += f" (Operation: {self.operation})"
        if self.node is not None:
            result += f" (Node: {self.node})"
        return result


class InvalidBalanceFactorError(AVLError):
    """
    Exception levée lors d'un facteur d'équilibre invalide.

    Cette exception est levée quand le facteur d'équilibre d'un nœud AVL
    n'est pas dans la plage valide [-1, 0, 1].

    :param message: Message d'erreur descriptif
    :type message: str
    :param balance_factor: Facteur d'équilibre invalide
    :type balance_factor: int
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(self, message: str, balance_factor: int, node=None):
        """
        Initialise l'exception InvalidBalanceFactorError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param balance_factor: Facteur d'équilibre invalide
        :type balance_factor: int
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message, "balance_factor_validation", node)
        self.balance_factor = balance_factor

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur le facteur d'équilibre
        :rtype: str
        """
        base_msg = super().__str__()
        return f"{base_msg} (Balance factor: {self.balance_factor})"


class RotationError(AVLError):
    """
    Exception levée lors d'une erreur de rotation AVL.

    Cette exception est levée quand une rotation ne peut pas être effectuée
    ou quand elle produit un résultat invalide.

    :param message: Message d'erreur descriptif
    :type message: str
    :param rotation_type: Type de rotation qui a échoué
    :type rotation_type: str
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(self, message: str, rotation_type: str, node=None):
        """
        Initialise l'exception RotationError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param rotation_type: Type de rotation qui a échoué
        :type rotation_type: str
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message, "rotation", node)
        self.rotation_type = rotation_type

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur le type de rotation
        :rtype: str
        """
        base_msg = super().__str__()
        return f"{base_msg} (Rotation type: {self.rotation_type})"


class HeightMismatchError(AVLError):
    """
    Exception levée lors d'une incohérence de hauteur.

    Cette exception est levée quand la hauteur calculée ne correspond pas
    à la hauteur mise en cache ou quand il y a une incohérence dans les
    calculs de hauteur.

    :param message: Message d'erreur descriptif
    :type message: str
    :param calculated_height: Hauteur calculée
    :type calculated_height: int
    :param cached_height: Hauteur mise en cache
    :type cached_height: int
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(
        self, message: str, calculated_height: int, cached_height: int, node=None
    ):
        """
        Initialise l'exception HeightMismatchError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param calculated_height: Hauteur calculée
        :type calculated_height: int
        :param cached_height: Hauteur mise en cache
        :type cached_height: int
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message, "height_validation", node)
        self.calculated_height = calculated_height
        self.cached_height = cached_height

    def __str__(self) -> str:
        """
        Retourne la représentation string de l'exception.

        :return: Message d'erreur avec informations sur les hauteurs
        :rtype: str
        """
        base_msg = super().__str__()
        return f"{base_msg} (Calculated: {self.calculated_height}, Cached: {self.cached_height})"


class AVLNodeError(AVLError):
    """
    Exception de base pour toutes les erreurs liées aux nœuds AVL.

    Cette exception sert de classe de base pour toutes les erreurs spécifiques
    aux nœuds AVL, permettant une gestion d'erreurs hiérarchique.

    :param message: Message d'erreur descriptif
    :type message: str
    :param operation: Opération qui a causé l'erreur (optionnel)
    :type operation: str, optional
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(self, message: str, operation: str = None, node=None):
        """
        Initialise l'exception AVLNodeError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param operation: Opération qui a causé l'erreur (optionnel)
        :type operation: str, optional
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message, operation, node)


class HeightCalculationError(AVLNodeError):
    """
    Exception levée lors d'une erreur de calcul de hauteur.

    Cette exception est levée quand il y a une erreur dans le calcul
    de la hauteur d'un nœud AVL ou de ses sous-arbres.

    :param message: Message d'erreur descriptif
    :type message: str
    :param node: Nœud concerné par l'erreur (optionnel)
    :type node: AVLNode, optional
    """

    def __init__(self, message: str, node=None):
        """
        Initialise l'exception HeightCalculationError.

        :param message: Message d'erreur descriptif
        :type message: str
        :param node: Nœud concerné par l'erreur (optionnel)
        :type node: AVLNode, optional
        """
        super().__init__(message, "height_calculation", node)
