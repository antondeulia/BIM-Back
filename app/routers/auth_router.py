from fastapi import APIRouter, Depends, HTTPException, Response, Security
import httpx

from app.config.settings import settings
from app.config.di import get_refresh_token_repository, get_user_repository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import SignInRequest, SignUpRequest, GoogleAuthRequest
from app.services.auth_service import AuthService
from app.utils.auth import get_current_user

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repo: RefreshTokenRepository = Depends(get_refresh_token_repository)
):
    return AuthService(
        user_repository,
        refresh_token_repo
    )

router = APIRouter(prefix="/auth")

@router.post("/sign-up")
def sign_up(
    req: SignUpRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.sign_up(req.email, req.password)

@router.post("/sign-in")
def sign_in(
    req: SignInRequest,
    service: AuthService = Depends(get_auth_service)
):
    return service.sign_in(req.email, req.password)

@router.post("/google")
def google_auth(
    req: GoogleAuthRequest,
    service: AuthService = Depends(get_auth_service)
): 
    print("hallo")
    return service.google_auth(
        email=req.email,
        google_sub=req.google_sub
    )

@router.get("/me")
def me(
    current_user = Security(get_current_user)
):
    return current_user

@router.post("/refresh")
def refresh(
    token: str,
    service: AuthService = Depends(get_auth_service)
):
    return service.refresh(token)

@router.delete("/logout")
def logout(
    response: Response,
    token: str,
    service: AuthService = Depends(get_auth_service)
):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
    )

    return service.logout(token)