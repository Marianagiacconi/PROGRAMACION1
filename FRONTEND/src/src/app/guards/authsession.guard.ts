import { Injectable, Inject, PLATFORM_ID } from '@angular/core';  
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';  
import { Observable } from 'rxjs';  
import { isPlatformBrowser } from '@angular/common';  

@Injectable({  
  providedIn: 'root'  
})  
export class AuthsessionGuard implements CanActivate {  
  
  constructor(private router: Router, @Inject(PLATFORM_ID) private platformId: Object) {}  

  canActivate(  
    route: ActivatedRouteSnapshot,  
    state: RouterStateSnapshot  
  ): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {  
    
    if (isPlatformBrowser(this.platformId)) {  
      const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');  
      if (!token) {  
        this.router.navigate(['/home']);  
        return false;  
      }  
    }  
    
    return true;  
  }  
}