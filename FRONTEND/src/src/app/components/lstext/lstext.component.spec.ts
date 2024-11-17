import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LstextComponent } from './lstext.component';

describe('LstextComponent', () => {
  let component: LstextComponent;
  let fixture: ComponentFixture<LstextComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LstextComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LstextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
