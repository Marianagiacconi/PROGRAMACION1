import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PagComponent } from './pag.component';

describe('PagComponent', () => {
  let component: PagComponent;
  let fixture: ComponentFixture<PagComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PagComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PagComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
