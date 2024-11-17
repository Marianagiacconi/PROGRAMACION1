import { Component, OnInit } from '@angular/core';
import { UsersService } from 'src/app/services/users.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User } from 'src/app/models/user'; // Asegúrate de tener esta interfaz

@Component({
  selector: 'app-abm-usuario',
  templateUrl: './abm-usuario.component.html',
  styleUrls: ['./abm-usuario.component.css'],
})
export class AbmUsuarioComponent implements OnInit {
  users: User[] = [];
  selectedUser: User | null = null;
  userForm!: FormGroup;
  errorMessage: string | null = null;
  isEditing: boolean = false;

  constructor(
    private usersService: UsersService,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.fetchUsers();
    this.initializeForm();
  }

  fetchUsers(): void {
    this.usersService.getAllUsers().subscribe(
      (data) => {
        this.users = data;
      },
      (error) => {
        console.error('Error al cargar usuarios:', error);
        this.errorMessage = 'Error al cargar usuarios.';
      }
    );
  }

  initializeForm(): void {
    this.userForm = this.formBuilder.group({
      firstname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      admin: [false],
    });
  }

  selectUser(user: User): void {
    this.selectedUser = user;
    this.isEditing = true;
    this.userForm.patchValue({
      firstname: user.firstname,
      email: user.email,
      admin: user.admin,
    });
  }

  createUser(): void {
    if (this.userForm.valid) {
      const newUser: Partial<User> = {
        firstname: this.userForm.value.firstname,
        email: this.userForm.value.email,
        password: 'defaultPassword', // Considera manejar contraseñas de manera segura
        admin: this.userForm.value.admin,
      };

      this.usersService.createUser(newUser).subscribe(
        (response) => {
          console.log('Usuario creado:', response);
          this.fetchUsers();
          this.userForm.reset({ admin: false });
        },
        (error) => {
          console.error('Error al crear usuario:', error);
          this.errorMessage = 'Error al crear usuario.';
        }
      );
    }
  }

  updateUser(): void {
    if (this.selectedUser && this.userForm.valid) {
      const updatedUser: Partial<User> = {
        firstname: this.userForm.value.firstname,
        email: this.userForm.value.email,
        admin: this.userForm.value.admin,
      };

      this.usersService.updateUser(this.selectedUser.id.toString(), updatedUser).subscribe(
        (response) => {
          console.log('Usuario actualizado:', response);
          this.fetchUsers();
          this.cancelEdit();
        },
        (error) => {
          console.error('Error al actualizar usuario:', error);
          this.errorMessage = 'Error al actualizar usuario.';
        }
      );
    }
  }

  deleteUser(userId: number): void {
    if (confirm('¿Estás seguro de eliminar este usuario?')) {
      this.usersService.deleteUser(userId.toString()).subscribe(
        (response) => {
          console.log('Usuario eliminado:', response);
          this.fetchUsers();
        },
        (error) => {
          console.error('Error al eliminar usuario:', error);
          this.errorMessage = 'Error al eliminar usuario.';
        }
      );
    }
  }

  cancelEdit(): void {
    this.selectedUser = null;
    this.isEditing = false;
    this.userForm.reset({ admin: false });
  }
}
