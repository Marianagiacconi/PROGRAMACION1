import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewPoemasComponent } from './view-poemas.component';

describe('ViewPoemasComponent', () => {
  let component: ViewPoemasComponent;
  let fixture: ComponentFixture<ViewPoemasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewPoemasComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewPoemasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
