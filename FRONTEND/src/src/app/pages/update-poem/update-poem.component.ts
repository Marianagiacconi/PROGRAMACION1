import { Component, OnInit } from '@angular/core';  
import { FormBuilder, FormGroup, Validators } from '@angular/forms';  
import { ActivatedRoute, Router } from '@angular/router';  
import { PoemsService } from '../../services/poems.service';  
import { UsersService } from '../../services/users.service';  

@Component({  
  selector: 'app-update-poem',  
  templateUrl: './update-poem.component.html',  
})  
export class UpdatePoemComponent implements OnInit {  
  
  poemForm: FormGroup;  
  poemId: number | undefined;  
  userId: string | null = null;  
  canUpload: boolean = false;  

  constructor(  
    private formBuilder: FormBuilder,  
    private route: ActivatedRoute,  
    private router: Router,  
    private poemsService: PoemsService,  
    private usersService: UsersService  
  ) {  
    // Inicializa el formulario con validadores de título y contenido  
    this.poemForm = this.formBuilder.group({  
      title: ['', Validators.required],  
      content: ['', Validators.required],  
    });  
  }  

  ngOnInit(): void {  
    this.userId = this.usersService.getCurrentUserId(); // Llama a la función que ahora busca en sessionStorage  
    console.log('ID de usuario:', this.userId); // Esto debe mostrar el ID correcto  
    if (!this.userId) {  
        console.error('Usuario no autenticado');  
        this.router.navigate(['/login']); // Redirigir a login si no hay usuario  
        return;  
    }  
  }  

  // Verifica si el usuario puede subir o actualizar un poema
  checkCanUploadPoem() {  
    this.poemsService.getUserPoemCount(this.userId).subscribe(
      (poemCount) => {
        // Si el usuario no ha subido ningún poema antes, se permite automáticamente.
        if (poemCount === 0) {
          this.canUpload = true;
        } else {
          // Si ya tiene poemas subidos, verifica la condición de calificación
          this.poemsService.canUploadPoem().subscribe(  
            (result) => {  
              this.canUpload = result.canUpload; // True si ha calificado suficiente
            },  
            (error) => {  
              console.error('Error al verificar si se puede subir un poema:', error);  
            }  
          );  
        }
      },
      (error) => {
        console.error('Error al obtener la cantidad de poemas del usuario:', error);
      }
    );
   
  }  

  // Cargar los datos del poema en el formulario  
  loadPoemData() {  
    if (this.poemId) {  
      this.poemsService.getPoem(this.poemId).subscribe({  
        next: (poem) => {  
          this.poemForm.patchValue(poem); // Carga los datos en el formulario  
        },  
        error: (error) => {  
          console.error('Error al cargar el poema:', error);  
        }  
      });  
    }  
  }  

  // Método para actualizar el poema si se cumplen los requisitos
  updatePoem() {  
    if (this.poemForm.valid && this.poemId !== undefined) {  
      if (this.canUpload) {  // Usa la propiedad canUpload ya verificada  
        const poemData = this.poemForm.value;  
        this.poemsService.putPoem(this.poemId.toString(), poemData).subscribe({  
          next: (response) => {  
            console.log('Poema actualizado:', response);  
            this.router.navigate(['/poems']);  // Redirige después de actualizar  
          },  
          error: (error) => {  
            alert('Ocurrió un error al actualizar el poema. Por favor, intenta nuevamente.');  
            console.error('Error al actualizar el poema:', error);  
          }  
        });  
      } else {  
        alert('No puedes subir un nuevo poema hasta que califiques al menos 5 poemas.');  
      }  
    } else {  
      console.error('Formulario no válido o ID inválido:', this.poemId);  
    }  
  }  

  // Método para cancelar la actualización y redirigir a la lista de poemas
  onCancel(): void {  
    this.router.navigate(['/poems']);  
  }  
}
