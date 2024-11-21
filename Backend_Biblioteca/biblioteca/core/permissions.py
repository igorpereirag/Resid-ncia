from rest_framework import permissions

class IsColecionadorOrReadOnly(permissions.BasePermission):
    

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  

       
        colecao = view.get_object()  
        return colecao.colecionador == request.user  
