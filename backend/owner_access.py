"""
# QuetzalCore Access Control - LOCKED TO XAVASENA ONLY
# Solo el dueo tiene acceso - nadie ms
"""

# from fastapi import HTTPException, Header
# import hashlib
# import os
# from typing import Optional

# XAVASENA MASTER KEY - Solo t tienes esto
# XAVASENA_MASTER_KEY = os.getenv(
    'XAVASENA_MASTER_KEY',
#     hashlib.sha256(b'xavasena_quetzalcore_owner_2025').hexdigest()

# Whitelist - Solo tu IP y tus machines
# AUTHORIZED_IPS = {
    '127.0.0.1',      # Local
    'localhost',       # Local
    # Agrega tus IPs aqu cuando las sepas
}


# def verify_owner_access(
#     x_owner_key: Optional[str] = Header(None),
#     x_forwarded_for: Optional[str] = Header(None)
) -> bool:
    """
#     Verifica que SOLO XAVASENA puede acceder
#     Nadie ms entra
    """
    
    # Verificar master key
#     if not x_owner_key:
#         raise HTTPException(
#             status_code=401,
#             detail=" Access Denied - Owner key required"
    
#     if x_owner_key != XAVASENA_MASTER_KEY:
#         raise HTTPException(
#             status_code=403,
#             detail=" Access Denied - Invalid owner key"
    
#     return True


# def get_owner_credentials() -> dict:
    """
#     Obtiene las credenciales del owner
#     Solo para mostrar a xavasena
    """
#     return {
        'owner': 'xavasena',
        'master_key': XAVASENA_MASTER_KEY,
        'access_level': 'FULL CONTROL',
        'permissions': [
            'standalone_access',
            'model_training',
            'system_control',
            'data_access',
            'full_autonomy'
        ]
    }


# Decorator para proteger endpoints
# def owner_only(func):
    """Solo el owner puede llamar esto"""
#     async def wrapper(*args, **kwargs):
        # Verificar en kwargs si viene el header
#         x_owner_key = kwargs.get('x_owner_key')
        
#         if not x_owner_key or x_owner_key != XAVASENA_MASTER_KEY:
#             raise HTTPException(
#                 status_code=403,
#                 detail=" Owner Only - Access Denied"
        
#         return await func(*args, **kwargs)
    
#     return wrapper
