import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';
import {jwtDecode } from 'jwt-decode'; 

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  url = 'http://127.0.0.1:5000/auth';

  constructor(private httpClient: HttpClient, private router: Router) {}

  login(credentials: { email: string; password: string }) {  
    return this.httpClient.post(`${this.url}/login`, credentials).pipe(  
      tap((response: any) => {
        const token = response.access_token;  // Suponiendo que tu backend envía el token como 'access_token'
        sessionStorage.setItem('token', token);
    
        // Decodificar el token para obtener los claims (ejemplo usando jwt-decode)
        const decodedToken: any = jwtDecode(token);
        const userData = {
            id: decodedToken.id,
            admin: decodedToken.admin,
            email: decodedToken.email
        };
        sessionStorage.setItem('user', JSON.stringify(userData));
    })
    
    );  
}

  // Método para cerrar sesión
  logout(): void {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('email');
    sessionStorage.removeItem('id');
    this.router.navigate(['/home']);
  }

  // Verificar si el usuario está autenticado
  isAuthenticated(): boolean {
    return !!sessionStorage.getItem('token');
  }
  // Obtener el token
  getToken(): string | null {
    return sessionStorage.getItem('token');
  }

  isAdmin(): boolean {
    const user = JSON.parse(sessionStorage.getItem('user') || '{}');
    return user.admin === true;  
}


}
