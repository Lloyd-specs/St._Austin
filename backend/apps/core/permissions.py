from rest_framework import permissions


class RoleBasedPermission(permissions.BasePermission):
    """
    Check against custom permission codenames assigned to the user's role.

    Usage on views:
        permission_classes = [IsAuthenticated, RoleBasedPermission]
        required_permissions = ['patients.add_patient']
    """
    def has_permission(self, request, view):
        required = getattr(view, 'required_permissions', [])
        if not required:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        user_perms = set(
            request.user.role.permissions.values_list('codename', flat=True)
        )
        return all(p.split('.')[-1] in user_perms for p in required)


class IsAdminSystem(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            and request.user.role.name == 'admin_systeme'
        )


class IsDirecteur(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            and request.user.role.name == 'directeur'
        )


class IsPharmacien(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            and request.user.role.name == 'pharmacien'
        )


class IsMedecin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role
            and request.user.role.name == 'medecin'
        )
