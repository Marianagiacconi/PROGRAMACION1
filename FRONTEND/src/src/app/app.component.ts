import { Component } from '@angular/core';
import { PoemsService } from './services/poems.service';
import { UsersService } from './services/users.service';
import { LoginService } from './services/login.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'src';

constructor (
  private UsersService: UsersService,
  private LoginService : LoginService,
  private PoemsService: PoemsService
){} 
}