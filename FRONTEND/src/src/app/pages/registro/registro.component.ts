import { Token } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-registro',
  templateUrl: './registro.component.html',
  styleUrls: ['./registro.component.css'],
})
export class RegistroComponent implements OnInit {
  private subscription: Subscription | null = null;
  registerForm!: FormGroup;

  constructor(
    private UsersService: UsersService,
    private formBuider: FormBuilder,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registerForm = this.formBuider.group({
      firstname: ['', Validators.required],
      email: ['', Validators.required],
      password: ['', Validators.required],
      repeatpassword: ['', Validators.required],
    });
  }

  register(data: any): void {
    // Asigna la suscripción
    this.subscription = this.UsersService.register(data).subscribe({
      next: response => {
        console.log('Registro exitoso:', response);
      },
      error: error => {
        console.error('Error en el registro:', error);
      }
    });
  }

  submit() {
    if (this.registerForm.valid) {
      let firstname = this.registerForm.value.firstname;
      let email = this.registerForm.value.email;
      let password = this.registerForm.value.password;
      let repeatpassword = this.registerForm.value.repeatpassword;

      if (password != repeatpassword) {
        alert('Formulario invalido');
      } else {
        this.register({
          firstname: firstname,
          email: email,
          password: password,
          admin: 0,
        });
      }
    } else {
      alert('Formulario invalido');
    }
  }
}