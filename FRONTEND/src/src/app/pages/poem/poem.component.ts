import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-poem',
  templateUrl: './poem.component.html',
  styleUrls: ['./poem.component.css'],
})
export class PoemComponent implements OnInit {
  usuario_id!: string;
  tipo_op!: string;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.usuario_id = this.route.snapshot.paramMap.get('id') || '';
    this.tipo_op = this.route.snapshot.paramMap.get('tipo_op') || '';
  }
}
