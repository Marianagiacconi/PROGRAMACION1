import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService } from 'src/app/services/login.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  
loginForm!: FormGroup;

  constructor(
    private loginService: LoginService,
    private formBuilder: FormBuilder,
    private router: Router
  ) {}
  pass = '';
  email = '';

  onEmail(event: any) {
    this.email = event.target.value ;
  }
  onPass(event: any) {
    this.pass = event.target.value;
  }
  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      email: ['', Validators.required],
      password: ['', Validators.required],
    });
  }
  
    iniciarSession(): void {   
      const { email, password } = this.loginForm.value;
      this.loginService.login({ email, password }).subscribe(
        (data: any) => {
          console.log('Login exitoso:', data);
          sessionStorage.setItem('token', data.token); // Guarda el token
          sessionStorage.setItem('email', data.email);
          sessionStorage.setItem('id', data.id);
  
          this.router.navigate(['/home']); // Redirige después de iniciar sesión
        },
        (error) => {
          console.error('Error en el inicio de sesión:', error);
          alert('Error en el inicio de sesión. Verifica tus credenciales.');
        }
      );
    }
  
    submit(): void {
      if (this.loginForm.valid) {
        this.iniciarSession();
      } else {
        alert('Formulario inválido. Completa todos los campos.');
      }
    }
  
    cerrarSesion(): void {
      this.loginService.logout();
    }
  }

