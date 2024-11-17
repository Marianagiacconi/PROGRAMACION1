import { Component, OnInit } from '@angular/core';
import { UsersService } from '../../services/users.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(
    private UsersService:UsersService
  ) { }

  ngOnInit(): void {
  }

  get isToken(){
    return sessionStorage.getItem('token') || undefined;
  }

  cerrarSesion(){
    this.UsersService.logout()
  }
}