import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { LoginComponent } from './pages/login/login.component';
import { RegistroComponent } from './pages/registro/registro.component';
import { DefaultComponent } from './pages/default/default.component';
import { PoemaComponent } from './pages/poema/poema.component';
import { AuthsessionGuard } from './guards/authsession.guard';
import { UpdatePoemComponent } from './pages/update-poem/update-poem.component';
import { HeaderComponent } from './components/header/header.component';
import { AbmUsuarioComponent } from './components/abm-usuario/abm-usuario.component';


const routes: Routes = [
  { path:'', component: HomeComponent},
  { path:'home', component: HomeComponent},
  { path:'login', component: LoginComponent},
  { path:'registro', component: RegistroComponent},
  { path:'header', component: HeaderComponent, canActivate:[AuthsessionGuard] },
  { path: 'update-poem', component: UpdatePoemComponent },
  { path: 'usuarios', component: AbmUsuarioComponent },
  { path:'poema', component: PoemaComponent},
  { path: '**', component: DefaultComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 