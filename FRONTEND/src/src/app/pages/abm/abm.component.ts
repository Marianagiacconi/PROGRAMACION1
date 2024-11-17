import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UsersService } from 'src/app/services/users.service';

@Component({
  selector: 'app-abm',
  templateUrl: './abm.component.html',
  styleUrls: ['./abm.component.css'],
})
export class AbmComponent implements OnInit {
  @Input() user_id!: string;
  @Input() tipoOperacion!: string;

  user: any = {};

  constructor(public router: Router, private UsersService: UsersService) {}

  ngOnInit(): void {
    if (this.user_id) {
      this.UsersService.getUser(this.user_id).subscribe((data: any) => {
        this.user = data;
      });
    }
  }

  alta(): void {
    this.UsersService.postUsers(this.user).subscribe(() => {
      alert('Usuario creado exitosamente.');
      this.router.navigate(['/usuarios']);
    });
  }

  editar(): void {
    const admin = this.user.admin ? 0 : 1;
    this.UsersService.putUser(this.user_id, { admin }).subscribe(() => {
      alert('Permisos actualizados.');
      this.router.navigate(['/usuarios']);
    });
  }

  eliminar(): void {
    this.UsersService.delUser(this.user_id).subscribe(() => {
      alert('Usuario eliminado.');
      this.router.navigate(['/usuarios']);
    });
  }
}
