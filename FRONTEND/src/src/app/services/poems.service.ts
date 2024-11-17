import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PoemsService {
  private baseUrl = 'http://localhost:5000';  // URL base del backend

  constructor(private httpClient: HttpClient) { }

  getPoems(): Observable<any> {
    return this.httpClient.get(`${this.baseUrl}/poems`);
  }
  // Obtiene la cantidad de poemas subidos por el usuario
  getUserPoemCount(userId: string | null): Observable<number> {
    return this.httpClient.get<number>(`${this.baseUrl}/users/${userId}/poem-count`);
  }

  getPoem(id: number): Observable<any> {
    return this.httpClient.get(`${this.baseUrl}/poem/${id}`);
  }

  postPoem(body: any): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/poems`, body);
  }

  canUploadPoem(): Observable<{ canUpload: boolean }> {  
    return this.httpClient.get<{ canUpload: boolean }>(`${this.baseUrl}/can_upload`);  
  }  

  putPoem(id: string, body: any): Observable<any> {
    return this.httpClient.put(`${this.baseUrl}/poem/${id}`, body);
  }

  delPoem(id: string): Observable<any> {
    return this.httpClient.delete(`${this.baseUrl}/poem/${id}`);
  }
}
