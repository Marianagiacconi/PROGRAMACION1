import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user'; // Asegúrate de que la ruta sea correcta

@Injectable({
  providedIn: 'root',
})
export class UsersService {
  private baseUrl = 'http://localhost:5000/auth'; // URL base del backend

  constructor(private httpClient: HttpClient) {}

  /**
   * Obtener usuario desde sessionStorage.
   */
  getUserFromSessionStorage(): any {
    const user = sessionStorage.getItem('user');
    try {
      return user ? JSON.parse(user) : null;
    } catch (error) {
      console.error('Error parsing user from sessionStorage:', error);
      return null;
    }
  }

  /**
   * Obtener el ID del usuario actual almacenado en sessionStorage.
   */
  getCurrentUserId(): string | null {
    const user = this.getUserFromSessionStorage();
    return user ? user.id : null;
  }

  /**
   * Obtener todos los usuarios (solo para administradores).
   */
  getAllUsers(): Observable<User[]> {
    return this.httpClient.get<User[]>(`${this.baseUrl}/users`);
  }

  /**
   * Obtener detalles de un usuario por su ID.
   * @param id ID del usuario.
   */
  getUser(id: string): Observable<User> {
    return this.httpClient.get<User>(`${this.baseUrl}/user/${id}`);
  }

  /**
   * Crear un nuevo usuario.
   * @param body Datos del nuevo usuario.
   */
  createUser(body: Partial<User>): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/register`, body, {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  /**
   * Actualizar datos de un usuario.
   * @param id ID del usuario.
   * @param body Datos actualizados.
   */
  updateUser(id: string, body: Partial<User>): Observable<any> {
    return this.httpClient.put(`${this.baseUrl}/user/${id}`, body, {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  /**
   * Eliminar un usuario.
   * @param id ID del usuario a eliminar.
   */
  deleteUser(id: string): Observable<any> {
    return this.httpClient.delete(`${this.baseUrl}/user/${id}`);
  }

  /**
   * Iniciar sesión.
   * @param data Credenciales de inicio de sesión.
   */
  login(data: any): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/login`, data, {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  /**
   * Registrar un usuario.
   * @param data Datos de registro del usuario.
   */
  register(data: any): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/register`, data, {
      headers: { 'Content-Type': 'application/json' },
    });
  }

  /**
   * Verificar si el usuario actual está autenticado.
   */
  isAuthenticated(): boolean {
    const user = this.getUserFromSessionStorage();
    return !!user;
  }
  isAdmin(user: User): boolean {  
    return user.admin;
  } 

  /**
   * Cerrar sesión.
   */
  logout(): void {
    sessionStorage.removeItem('user');
    alert('Sesión cerrada exitosamente');
  }
}
