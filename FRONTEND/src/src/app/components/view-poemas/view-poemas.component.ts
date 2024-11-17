import { Component, OnInit } from '@angular/core';
import { PoemsService } from 'src/app/services/poems.service';

@Component({
  selector: 'app-view-poemas',
  templateUrl: './view-poemas.component.html',
  styleUrls: ['./view-poemas.component.css']
})
export class ViewPoemasComponent implements OnInit {
  arrayPoemas:any

  constructor(private PoemsService: PoemsService) {
   }

  ngOnInit(): void {
    this.PoemsService.getPoems().subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.arrayPoemas = data.poems;
    })

}
}
