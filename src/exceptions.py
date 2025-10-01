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
